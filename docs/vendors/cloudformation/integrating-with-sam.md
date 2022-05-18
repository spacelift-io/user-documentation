# Integrating with SAM

In order to use [SAM](https://aws.amazon.com/serverless/sam/){: rel="nofollow"} in a CloudFormation Stack you'll need to do two things: create a Docker image with SAM included and invoke SAM in `before_init` hooks.

The first one can be done using a Dockerfile akin to this one:

```docker
FROM public.ecr.aws/spacelift/runner-terraform
USER root
WORKDIR /home/spacelift
RUN apk add --update --no-cache curl py-pip
RUN apk -v --no-cache --update add \
        musl-dev \
        gcc \
        python3 \
        python3-dev
RUN python3 -m ensurepip --upgrade \
        && pip3 install --upgrade pip
RUN pip3 install --upgrade awscli aws-sam-cli
RUN pip3 uninstall --yes pip \
        && apk del python3-dev gcc musl-dev
RUN sam --version
USER spacelift
```

You should build it, push it to a repository and set it as the [Runner Image](../../concepts/stack/stack-settings.md#runner-image) of your Stack.

You'll also have to invoke SAM in order to generate raw CloudFormation files and upload Lambda artifacts to S3. You can do this by adding the following to your before initialization hooks:

```bash
sam package --region ${CF_METADATA_REGION} --s3-bucket ${CF_METADATA_TEMPLATE_BUCKET} --s3-prefix sam-artifacts --output-template-file ${CF_METADATA_ENTRY_TEMPLATE_FILE}
```
