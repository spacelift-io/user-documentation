# Runtime configuration

The runtime configuration is an optional setup applied to individual runs instead of being global to the stack. It's defined in `.spacelift/config.yml` YAML file at the root of your repository. A single file is used to define settings for all stacks associated with its host Git repository, so the file structure looks like this:

```yaml title=".spacelift/config.yml"
version: "1"

stack_defaults:
    runner_image: your/first:runner
    # Note that tflint is not installed by
    # default - this example assumes that your
    # runner image has this available.
    before_init:
        - echo "checking formatting"
        - terraform fmt -diff
        - tflint

# Note that every field in the configuration is
# optional, and has a reasonable default. This file
# allows you to override those defaults, and you can
# merely override individual fields.
stacks:
    # The key of is the immutable slug of your stack
    # which you will find in the URL.
    babys-first-stack: &shared
        before_apply:
            - hostname
        project_root: infra
        terraform_version: 0.12.4
    babys-second-stack:
        <<: *shared
        terraform_version: 0.13.0
        environment:
            AWS_REGION: eu-west-1

```

The top level of the file contains three keys - `version` which in practice is currently ignored but may be useful in the future, `stacks` containing a mapping of immutable [stack id](../../stack/README.md#name-and-description) to the [stack configuration block](#stacks-configuration-block) and `stack_defaults`, containing the defaults common to all stacks using this source code repository. Note that corresponding stack-specific settings will override any stack defaults.

Considering the precedence of settings, below is the order that will be followed, starting from the most important to the least important:

1. The configuration for a specified stack defined in config.yml
2. The stack configuration set in the Spacelift UI.
3. The stack defaults defined config.yml

In cases where there is no stack slug defined in the config, only the first two sources are considered:

1. The stack configuration set in the Spacelift UI
2. The stack defaults defined in config.yml

!!! info
    Since we adopted everyone's favorite data serialization format, you can use all the YAML shenanigans you can think of - things like anchors and inline JSON can keep your config DRY and neat.

## Purpose of runtime configuration

The whole concept of runtime configuration may initially sound unnecessary, but it ultimately allows flexibility that would otherwise be hard to achieve. In general, its purpose is to **preview effects of changes not related to the source code** (eg. Terraform or Pulumi version upgrades, variable changes etc.), before they become an established part of your infra.

While stack environment applies both to tracked and non-tracked branches, a runtime configuration change can be pushed to a feature branch, which triggers [proposed runs](../../run/README.md#where-do-runs-come-from) allowing you to preview the changes before they have a chance to affect your state.

!!! info
    If the runtime configuration file is not present or does not contain your stack, default values are used - refer to each setting for its respective default.

## `Stacks` configuration block

### `before_` and `after_` hooks

!!! info
    Each collection defaults to an **empty array**.

These scripts allow customizing the Spacelift workflow - see the relevant documentation [here](../../stack/stack-settings.md#customizing-workflow). The following are available:

- `before_init`
- `after_init`
- `before_plan`
- `after_plan`
- `before_apply`
- `after_apply`
- `before_perform`
- `after_perform`
- `before_destroy`
- `after_destroy`
- `after_run`

### `environment` map

!!! info
    Defaults to an **empty map**.

The environment allows you to declaratively pass some environment variables to the runtime configuration of the Stack. In case of a conflict, these variables will override both the ones passed via attached [Contexts](../context.md) and those directly set in Stack's [environment](../environment.md).

### `project_root` setting

!!! info
    Defaults to an **empty string**, pointing to the working directory for the run.

Project root is the path of your project directory inside the Hub repository. You can use this setting to point Spacelift to the right place if the repo contains source code for multiple stacks in various folders or serves multiple purposes like those increasingly popular _monorepos_ combining infrastructure definitions with source code, potentially even for multiple applications.

### `runner_image` setting

!!! info
    Defaults to [**`public.ecr.aws/spacelift/runner-terraform:latest`**](https://gallery.ecr.aws/spacelift/runner-terraform){: rel="nofollow"}. See [this section](../../../integrations/docker.md) for more details.

The runner image is the Docker image used to run your workloads. By making it a runtime setting, Spacelift allows testing the image before it modifies your infrastructure.

### `terraform_version` setting

!!! info
    Defaults to the **latest known supported Terraform version.**

This setting is only valid on Terraform stacks and specifies the Terraform version that the run will use. The main use case is testing a newer version of Terraform before you use it to change the state since the way back is very hard. This version can only be equal to or higher than the one already used to apply state changes. For more details on Terraform version management, please refer to its [dedicated help section](../../../vendors/terraform/version-management.md).

### `opentofu_version` setting

!!! info
    Defaults to the **latest known supported OpenTofu version**.

This setting specifies the OpenTofu version to be used during the run and is only applicable to Terraform stacks. It is considered when `terraform_workflow_tool` is set to `OPEN_TOFU`. To specify a version, ensure it aligns with those officially supported and tested by Spacelift.

Example: `opentofu_version: "1.6.2"`

### `terraform_workflow_tool` setting

This setting determines the Terraform implementation used in the workflow. Choose based on your project needs and the specific features or support each option offers:

- `TERRAFORM_FOSS` (default) - Utilizes the official Terraform by HashiCorp. Best for standard Terraform operations and official provider support.
- `OPEN_TOFU` - An open-source Terraform fork. Choose this for enhanced features or modifications not available in the official version.
- `CUSTOM` - Enables the use of [Custom Workflows](https://spacelift.io/blog/introducing-custom-workflows) for highly customized or unique deployment processes.

Pulumi version management is based on [Docker images](../../../integrations/docker.md).
