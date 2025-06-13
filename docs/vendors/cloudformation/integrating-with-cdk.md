# Integrating with AWS Cloud Development Kit (CDK)

To use [AWS Cloud Development Kit](https://docs.aws.amazon.com/cdk/v2/guide/home.html){: rel="nofollow"} in an AWS CloudFormation stack you'll need to do two things: create a Docker image with AWS CDK and invoke it in `before_plan` hooks.

## Preparing the image

Since our base image doesn't support AWS CDK, you will have to build your image that includes it as well as any tooling needed to run whatever language your infrastructure declaration is written in.

The example below shows a Dockerfile with attached `cdk` and `go`:

```docker
FROM public.ecr.aws/spacelift/runner-terraform:latest
USER root

# Install packages
RUN apk update && apk add --update --no-cache npm
# Update NPM
RUN npm update -g
# Install cdk
RUN npm install -g aws-cdk
RUN cdk --version

# Add Go
COPY --from=golang:1.21-alpine /usr/local/go/ /usr/local/go/

ENV PATH="/usr/local/go/bin:${PATH}"
RUN go version
```

You should build it, push it to a repository, and set it as the [Runner Image](../../concepts/stack/stack-settings.md#runner-image) of your Stack.

## Adding `before_plan` hooks

For the AWS CDK code to be properly interpreted by Spacelift, you have to customize the default stack workflow by [enriching them with hooks](https://docs.spacelift.io/concepts/configuration/runtime-configuration#before_-and-after_-hooks).
To create a CloudFormation template that can be interpreted by Spacelift, you will have to add these hooks to the `before_plan` stage:

- `cdk bootstrap` - to bootstrap your AWS CDK project.
- `cdk synth` - to create a CloudFormation template.

## Limitations

### Multiple template AWS CDK definition

The default CloudFormation integration in Spacelift uses a single CloudFormation template.
That means that AWS CDK definitions that generate multiple templates will only have a single template picked up for further processing.
To mitigate this, consider unifying the AWS CDK definition to generate a single template file.

### Deploying Lambdas

Our integration doesn't use `cdk deploy`, but rather uses template definitions created by `cdk synth`.

`cdk deploy` deploys Lambda assets to S3 which are used to deploy Lambdas by CloudFormation.
Our process won't upload assets, so deploying Lambdas via a Spacelift stack configured to handle AWS CDK will result in errors.
