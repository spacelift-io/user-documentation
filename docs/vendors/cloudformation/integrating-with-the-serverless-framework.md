# Integrating with the serverless framework

In order to use the [serverless framework](https://www.serverless.com) in a CloudFormation Stack you'll need to do a few things: create a Docker image with the serverless framework included, invoke the serverless CLI in `before_init` hook, sync your artifacts with S3, and make sure the serverless config has your [template bucket](reference.md#stack-settings) configured as the artifact location.

The first one can be done using a Dockerfile akin to this one:

```docker
FROM public.ecr.aws/spacelift/runner-terraform
USER root
WORKDIR /home/spacelift
RUN apk add --update --no-cache curl nodejs npm
RUN npm install -g serverless
RUN serverless --version
USER spacelift
```

You should build it, push it to a repository and set it as the [Runner Image](https://docs.spacelift.io/concepts/stack/stack-settings#runner-image) of your Stack.

You'll also have to invoke the serverless CLI in order to generate raw CloudFormation files. You can do this by adding the following to your before initialization hooks:

`serverless package --region ${CF_METADATA_REGION}`

You can add the following script as a mounted file:

```bash
#!/bin/bash

set -eu
set o pipefile

STATE_FILE=.serverless/serverless-state.json
S3_PREFIX=$(jq -r '.package.artifactDirectoryName' < "$STATE_FILE")
ARTIFACT=$(jq -r '.package.artifact' < "$STATE_FILE")

aws s3 cp .serverless/$ARTIFACT s3://$CF_METADATA_TEMPLATE_BUCKET/$S3_PREFIX/$ARTIFACT
```

and invoke it in your before initialization hooks: `sh sync.sh`

Finally, specify the S3 bucket for artifacts in your serverless.yml configuration file:

```yaml
provider:
  deploymentBucket: your-s3-bucket
```
