# Integrating with AWS Serverless Application Model (SAM)

In order to use [AWS Serverless Application Model (SAM)](https://aws.amazon.com/serverless/sam/){: rel="nofollow"} in an AWS CloudFormation Stack you'll need to do two things: create a Docker image with SAM included and invoke SAM in `before_init` hooks.

The first one can be done using a Dockerfile akin to this one:

```docker
FROM public.ecr.aws/spacelift/runner-terraform
USER root
WORKDIR /home/spacelift
RUN apk -v --update --no-cache add curl
RUN python3 -m venv /home/spacelift/.venv && \
    source /home/spacelift/.venv/bin/activate && \
    python3 -m ensurepip --upgrade && \
    pip3 install --upgrade pip && \
    pip3 install --upgrade awscli aws-sam-cli && \
    pip3 uninstall --yes pip
RUN source /home/spacelift/.venv/bin/activate && sam --version
USER spacelift
```

You should build it, push it to a repository and set it as the [Runner Image](../../concepts/stack/stack-settings.md#runner-image) of your Stack.

You'll also have to invoke SAM in order to generate raw CloudFormation files and upload Lambda artifacts to S3. You can do this by adding the following to your before initialization hooks:

```bash
source /home/spacelift/.venv/bin/activate && sam package --region ${CF_METADATA_REGION} --s3-bucket ${CF_METADATA_TEMPLATE_BUCKET} --s3-prefix sam-artifacts --output-template-file ${CF_METADATA_ENTRY_TEMPLATE_FILE}
```
