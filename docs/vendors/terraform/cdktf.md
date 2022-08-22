# Cloud Development Kit for Terraform (CDKTF)

The [Cloud Development Kit for Terraform (CDKTF)](https://www.terraform.io/cdktf){: rel="nofollow"} generates JSON Terraform configuration from code in C#, Python, TypeScript, Java, or Go. Spacelift fully supports CDKTF.

## Building a custom runner image

CDKTF requires packages and tools that are not included in the default Terraform runner. These dependencies are different for each supported programming language.

Luckily, extending the default runner Docker image to include these dependencies is easy. You will need to:

- Create a `Dockerfile` file that installs the required tools and packages for the specific programming language you want to use (see below).
- Build and publish the Docker image.
- Configure the runner image to use in the [stack settings](../../concepts/stack/stack-settings.md#runner-image).

=== "TypeScript"

    ```docker
    FROM public.ecr.aws/spacelift/runner-terraform:latest

    USER root
    RUN apk add --no-cache nodejs npm
    RUN npm install --global cdktf-cli@latest
    USER spacelift
    ```

=== "Python"

    ```docker
    FROM public.ecr.aws/spacelift/runner-terraform:latest

    USER root
    RUN apk add --no-cache nodejs npm python3
    RUN npm install --global cdktf-cli@latest
    RUN python3 -m ensurepip \
      && python3 -m pip install --upgrade pip setuptools

    USER spacelift
    RUN pip3 install --user pipenv
    ENV PATH="/home/spacelift/.local/bin:$PATH"
    ```

## Synthesizing Terraform code

Before Terraform can plan and apply changes to your infrastructure, CDKTF must turn your C#, Python, TypeScript, Java, or Go code into Terraform configuration code. That process is called synthesizing.

This step needs to happen before the [Initializing phase](../../concepts/run/README.md#initializing) of a run. This can be easily done by adding a few [`before_init` hooks](../../concepts/stack/stack-settings.md#customizing-workflow):

=== "TypeScript"

    - `npm install`
    - `cdktf synth`
    - `cp cdktf.out/stacks/<STACK NAME>/cdk.tf.json .` (Make sure to replace `<STACK NAME>` with the name of the stack)

=== "Python"

    - `pipenv install`
    - `cdktf synth`
    - `cp cdktf.out/stacks/<STACK NAME>/cdk.tf.json .` (Make sure to replace `<STACK NAME>` with the name of the stack)

!!! warning
    If the [Terraform state](./state-management.md) is managed by Spacelift, make sure to disable the local backend that CDKTF automatically adds if none is configured.

    === "TypeScript"

        ```typescript
        class ExampleStack extends TerraformStack {
          constructor(scope: Construct, name: string) {
            super(scope, name);

            // This is required if Spacelift manages the state as CDKTF defaults to
            // the local backend if none is configured, which conflicts with Spacelift's backend
            this.addOverride("terraform.backend.local", null);

            // Other code
          }
        }
        ```

    === "Python"
        Add the following command after the hooks mentioned above:

        `cat <<< $(jq '.terraform.backend.local = null' cdk.tf.json) > cdk.tf.json`
