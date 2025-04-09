# Blueprint

{% if is_saas() %}
!!! Info
    This feature is only available on the Business plan and above. Please check out our [pricing page](https://spacelift.io/pricing){: rel="nofollow"} for more information.
{% endif %}

There are multiple ways to create [stacks](../stack/README.md) in Spacelift. Our recommended way is to use [our Terraform provider](../../vendors/terraform/terraform-provider.md) and programmatically create stacks using an [administrative](../stack/stack-settings.md#administrative) stack.

However, some users might not be comfortable using Terraform code to create stacks, this is where Blueprints come in handy.

## What is a Blueprint?

A Blueprint is a template for a stack and its configuration. The template can contain variables that can be filled in by providing inputs when creating a stack from the Blueprint. The template can also contain a list of other resources that will be created when the stack is created.

You can configure the following resources in a Blueprint:

- All [stack settings](../stack/stack-settings.md) including:
    - Name, description, labels, [Space](../spaces/README.md)
    - Behavioral settings: administrative, auto-apply, auto-destroy, hooks, runner image etc.
- [VCS configuration](../../integrations/source-control/README.md)
    - Both default and Space-level VCS integrations
- Vendor configuration for your IaaC provider
- [Environment variables](../configuration/environment.md#environment-variables), both non-sensitive and sensitive
- [Mounted files](../configuration/environment.md#mounted-files)
- Attaching [Contexts](../configuration/context.md)
- Attaching [Policies](../policy/README.md)
{% if is_saas() %}
- Attaching [AWS](../../integrations/cloud-providers/aws.md), [GCP](../../integrations/cloud-providers/gcp.md) and [Azure](../../integrations/cloud-providers/azure.md) integrations
{% else %}
- Attaching [AWS](../../integrations/cloud-providers/aws.md) integrations
{% endif %}
- Schedules:
    - [Drift detection](../stack/drift-detection.md)
    - [Task](../stack/scheduling.md#scheduled-task)
    - [Delete](../stack/scheduling.md#scheduled-delete-stack-ttl)

## Blueprint states

There are two states: draft and published. Draft is the default state, it means that the blueprint "development" is in progress and not meant to be used. You cannot create a stack from a draft blueprint.

Published means that the blueprint is ready to be used. You can publish a blueprint by clicking the `Publish` button in the UI.

A published blueprint cannot be moved back to draft state. You need to clone the blueprint, edit it and publish it.

You can share published blueprints with other users in your organization. They can create stacks from the blueprint as long as they have the necessary permissions. To share a blueprint, click on the Share button in the published blueprint view to generate a link. When users navigate to the link, they will be presented with the full screen template form without the blueprint editor.

<p align="center" >
    <img src="../../assets/screenshots/blueprints/blueprint-shared.png">
</p>
<figure markdown> <!-- markdownlint-disable-line MD033 -->
  <figcaption>Shared blueprint</figcaption> <!-- markdownlint-disable-line MD033 -->
</figure>

## Permissions

Blueprints permissions are managed by [Spaces](../spaces/README.md). You can only create, update and delete a blueprint in a Space you have **admin** access to but can be read by anyone with **read** access to the Space.

Once the blueprint is published and you want to create a stack from it, the **read** access will be enough as long as you have **admin** access to the Space where the stack will be created.

## How to create a Blueprint

Choose `Blueprints` on the left menu and click on `Create blueprint`. As of now, we only support YAML format. The template engine will be familiar for those who used GitHub Actions before.

The absolute minimum you'll need to provide is `name`, `space`, `vcs` and `vendor`; all others are optional. Here's a small working example:

{% raw %}

```yaml
inputs:
  - id: stack_name
    name: Stack name
stack:
  name: ${{ inputs.stack_name }}
  space: root
  vcs:
    branch: main
    repository: my-repository
    provider: GITHUB
  vendor:
    terraform:
      manage_state: true
      version: "1.3.0"
```

{% endraw %}

<p align="center" >
    <img src="../../assets/screenshots/blueprint_preview.png">
</p>
<figure markdown> <!-- markdownlint-disable-line MD033 -->
  <figcaption>Preview of a Blueprint</figcaption> <!-- markdownlint-disable-line MD033 -->
</figure>

The `Create a stack` button is inactive because the blueprint is in draft state. You can publish it by clicking the `Publish` button. After that, you can create a stack from the blueprint.

Now, let's look at a massive example that covers all the available configuration options:

!!! info
    Multiple stacks can be created using a single blueprint if `stacks` array is used instead of `stack` object. See the full schema below for more information.

<details> <!-- markdownlint-disable-line MD033 -->
<summary>Click to expand</summary> <!-- markdownlint-disable-line MD033 -->

{% raw %}

```yaml
inputs:
  - id: environment
    name: Environment to deploy to
    # type is not mandatory, defaults to short_text
  - id: app
    name: App name (used for naming convention)
    type: short_text
  - id: description
    name: Description of the stack
    type: long_text
    # long_text means you'll have a bigger text area in the UI
  - id: connstring
    name: Connection string to the database
    type: secret
    # secret means the input will be masked in the UI
  - id: tf_version
    name: Terraform version of the stack
    type: select
    options:
      - "1.3.0"
      - "1.4.6"
      - "1.5.0"
  - id: manage_state
    name: Should Spacelift manage the state of Terraform
    default: true
    type: boolean
  - id: destroy_task_epoch
    name: Epoch timestamp of when to destroy the resources
    type: number
options:
  # If true, a tracked run will be triggered right after the stack is created
  trigger_run: true
  # If true, stack will not be created, useful when using inputs and multi stacks in a single template. 
  do_not_create: false 
stack:
  name: ${{ inputs.app }}-{{ inputs.environment }}-stack
  space: root
  # The single-quote is needed to avoid YAML parsing errors since the question mark
  # and the colon is a reserved character in YAML.
  description: '${{ inputs.environment == "prod" ? "Production stack" : "Non-production stack" }}. Stack created at ${{ string(context.time) }}.'
  is_disabled: ${{ inputs.environment != 'prod' }}
  labels:
    - Environment/${{ inputs.environment }}
    - Vendor/Terraform
    - Owner/${{ context.user.login }}
    - Blueprint/${{ context.blueprint.name }}
    - Space/${{ context.blueprint.space }}
  administrative: false
  allow_promotion: false
  auto_deploy: false
  auto_retry: false
  local_preview_enabled: true
  secret_masking_enabled: true
  protect_from_deletion: false
  runner_image: public.ecr.aws/mycorp/spacelift-runner:latest
  worker_pool: 01GQ29K8SYXKZVHPZ4HG00BK2E
  attachments:
    contexts:
      - id: my-first-context-vnfq2
        priority: 1
    clouds:
      aws:
        id: 01GQ29K8SYXKZVHPZ4HG00BK2E
        read: true
        write: true
      azure:
        id: 01GQ29K8SYXKZVHPZ4HG00BK2E
        read: true
        write: true
        subscription_id: 12345678-1234-1234-1234-123456789012
    policies:
      - my-push-policy-1
      - my-approval-policy-1
  environment:
    variables:
      - name: MY_ENV_VAR
        value: my-env-var-value
        description: This is my non-encrypted env var
      - name: TF_VAR_CONNECTION_STRING
        value: ${{ inputs.connstring }}
        description: The connection string to the database
        secret: true
    mounted_files:
      - path: a.json
        content: |
          {
            "a": "b"
          }
        description: This is the configuration of x feature
        secret: true
  hooks:
    apply:
      before: ["sh", "-c", "echo 'before apply'"]
      after: ["sh", "-c", "echo 'after apply'"]
    init:
      before: ["sh", "-c", "echo 'before init'"]
      after: ["sh", "-c", "echo 'after init'"]
    plan:
      before: ["sh", "-c", "echo 'before plan'"]
      after: ["sh", "-c", "echo 'after plan'"]
    perform:
      before: ["sh", "-c", "echo 'before perform'"]
      after: ["sh", "-c", "echo 'after perform'"]
    destroy:
      before: ["sh", "-c", "echo 'before destroy'"]
      after: ["sh", "-c", "echo 'after destroy'"]
    run:
      # There is no before hook for run
      after: ["sh", "-c", "echo 'after run'"]
  schedules:
    drift:
      cron:
        - "0 0 * * *"
        - "5 5 * * 0"
      reconcile: true
      ignore_state: true # If true, the schedule will run even if the stack is in a failed state
      timezone: UTC
    tasks:
      # You need to provide either a cron or a timestamp_unix
      - command: "terraform apply -auto-approve"
        cron:
          - "0 0 * * *"
      - command: "terraform apply -auto-approve"
        timestamp_unix: ${{ int(timestamp('2024-01-01T10:00:20.021-05:00')) }}
    delete:
      delete_resources: ${{ inputs.environment == 'prod' }}
      timestamp_unix: ${{ inputs.destroy_task_epoch - 86400 }}
  vcs:
    id: "github-for-my-org" # Optional, only needed if you want to use a Space-level VCS integration. Use the "Copy ID" button to get the ID.
    branch: main
    project_root: modules/apps/${{ inputs.app }}
    project_globs:
      - "terraform/**"
      - "k8s/**"
    namespace: "my-namespace" # The VCS organization name or project namespace
    # Note that this is just the name of the repository, not the full URL
    repository: my-repository
    provider: GITHUB_ENTERPRISE # Possible values: GITHUB, GITLAB, BITBUCKET_DATACENTER, BITBUCKET_CLOUD, GITHUB_ENTERPRISE, AZURE_DEVOPS, RAW_GIT
    repository_url: "https://github.com/my-namespace/my-repository" # This is only needed for RAW_GIT provider
  vendor:
    terraform:
      manage_state: ${{ inputs.manage_state }}
      version: ${{ inputs.tf_version }}
      workspace: workspace-${{ inputs.environment }}
      use_smart_sanitization: ${{ inputs.environment != 'prod' }}
      workflow_tool: OPEN_TOFU # Could be TERRAFORM_FOSS, OPEN_TOFU or CUSTOM
    ansible:
      playbook: playbook.yml
    cloudformation:
      entry_template_file: cf/main.yml
      template_bucket: template_bucket
      stack_name: ${{ inputs.app }}-${{ inputs.environment }}
      region: '${{ inputs.environment.contains("prod") ? "us-east-1" : "us-east-2" }}'
    kubernetes:
      namespace: ${{ inputs.app }}
    pulumi:
      stack_name: ${{ inputs.app }}-${{ inputs.environment }}
      login_url: https://app.pulumi.com
    terragrunt:
      use_smart_sanitization: true
      terraform_version: "1.5.7"
      terragrunt_version: "0.55.0"
      use_run_all: true
      terragrunt_tool: OPEN_TOFU # Could be OPEN_TOFU, TERRAFORM_FOSS or MANUALLY_PROVISIONED
```

{% endraw %}

</details>

As you noticed if we attach an existing resource to the stack (such as Worker Pool, Cloud integration, Policy or Context) we use the unique identifier of the resource. Typically, there is a button for it in the UI but you can also find it in the URL of the resource.

<p align="center" >
    <img src="../../assets/screenshots/resource_ids.jpg">
</p>
<figure markdown> <!-- markdownlint-disable-line MD033 -->
  <figcaption>Example of resource IDs</figcaption> <!-- markdownlint-disable-line MD033 -->
</figure>

### Attaching a VCS

We have the following VCS systems available:

- `AZURE_DEVOPS`
- `BITBUCKET_CLOUD`
- `BITBUCKET_DATACENTER`
- `GITHUB` - this is the built-in GitHub integration that is used for SSO as well
- `GITHUB_ENTERPRISE` - unlike the name suggests, it's not only for GitHub Enterprise, but for any additional GitHub installation
- `GITLAB`
- `RAW_GIT` - enables you to use any public Git repository. When using this, you need to provide the full URL for the repository by setting the `repository_url` field.

{% raw %}

The `vcs` section is mandatory and you need to provide the `branch`, `repository` and `provider`. Additionally, if your VCS is anything other than `GITHUB` or `RAW_GIT`, you need to provide `namespace` as well. In GitHub, that's the organization name, in GitLab it's the group name, and in Bitbucket and Azure it's the project name.

If the VCS is `RAW_GIT`, you need to provide the `repository_url` instead of the `namespace` and `repository`.

The `id` is optional and only needed if you want to use a non-default integration. You can find the ID by clicking the `Copy ID` button in the VCS integration settings.

```yaml
  vcs:
    id: "github-for-my-org" # Optional, only needed if you want to use a non-default VCS integration. Use the "Copy ID" button to get the ID.
    branch: main
    project_root: modules/networking
    project_globs: # Project globs do not mount the files or directories in your project root. They are used primarily for triggering your stack when for example there are changes to a module outside of the project root.
      - "terraform/**"
      - "k8s/**"
    namespace: "my-namespace" # The VCS organization name or project namespace.
    repository: my-repository # Name of the repository.
    repository_url: "https://www.github.com/my-namespace/my-repository" # This is only needed for RAW_GIT
    provider: GITHUB_ENTERPRISE # Possible values: AZURE_DEVOPS, BITBUCKET_CLOUD, BITBUCKET_DATACENTER, GITHUB, GITHUB_ENTERPRISE, GITLAB, RAW_GIT
```

{% endraw %}

## Template engine

We built our own variable substitution engine based on [Google CEL](https://github.com/google/cel-spec){: rel="nofollow"}. The library is available on [GitHub](https://github.com/spacelift-io/celplate/){: rel="nofollow"}.

### Functions, objects

In the giant example above, you might have noticed something interesting: inline functions! CEL supports a couple of functions, such as: `contains`, `startsWith`, `endsWith`, `matches`, `size` and a bunch of others. You can find the full list in the [language definition](https://github.com/google/cel-spec/blob/v0.7.1/doc/langdef.md){: rel="nofollow"}. It also supports some basic operators, such as: `*`, `/`, `-`, `+`, relations (`==`, `!=`, `<`, `<=`, `>`, `>=`), `&&`, `||`, `!`, `?:` (yes, it supports the ternary operator 🎉) and `in`.

Other than the built-in operators and functions, we also added the [string extensions](https://github.com/google/cel-go/blob/v0.21.0/ext/strings.go){: rel="nofollow"} to the evaluator, which include `.replace()`, `.lowerAscii()`, `.split()` and other methods. Example:

{% raw %}

```yaml
stack:
  name: ${{ inputs.app_name.replace(" ", "-") }}
```

{% endraw %}

!!! hint
    It could be useful to look into [the unit tests](https://github.com/google/cel-go/blob/v0.13.0/cel/cel_test.go){: rel="nofollow"} of the library. Look for the invocations of `interpret` function.

There is one caveat to keep in mind: keep the YAML syntax valid.

### YAML syntax validity

There are reserved characters in YAML, such as `>` (multiline string) `|` (multiline string), `:` (key-value pair marker), `?` (mapping key) [etc](https://www.tutorialspoint.com/yaml/yaml_syntax_characters.htm). If you use these characters as part of a CEL expression, you'll need to use quotes around the expression to escape it. For example:

Invalid template:

{% raw %}

```yaml
stack:
  name: ${{ 2 > 1 ? "yes" : "no" }}-my-stack
```

{% endraw %}

See how the syntax highlighter is confused?

Valid template:

{% raw %}

```yaml
stack:
  name: '${{ 2 > 1 ? "yes" : "no" }}-my-stack'
```

{% endraw %}

Results in:

```yaml
stack:
  name: 'yes-my-stack'
```

### Interaction with Terraform `templatefile`

When using the Terraform [`templatefile`](https://developer.hashicorp.com/terraform/language/functions/templatefile){: rel="nofollow"} function to generate a Blueprint template body, you can run into issues because the Blueprint template engine and `templatefile` both use `$` as template delimiters. This can result in error messages like the following:

{% raw %}

```shell
│ Error: Error in function call
│
│   on main.tf line 2, in output "content":
│    2:   value = templatefile("${path.module}/test.tftpl", {
│    3:     SPACE = "root"
│    4:   })
│     ├────────────────
│     │ path.module is "."
│
│ Call to function "templatefile" failed: ./test.tftpl:5,31-32: Missing key/value separator; Expected an equals
│ sign ("=") to mark the beginning of the attribute value.
```

To solve this you can use `$${}` to indicate that `templatefile` should not attempt to replace a certain piece of text.

In the following example, `$${{ inputs.stack_name }}` is escaped, whereas `${SPACE}` is not:

```yaml
inputs:
  - id: stack_name
    name: Stack name
stack:
  name: $${{ inputs.stack_name }}
  space: ${SPACE}
  vcs:
    branch: main
    repository: my-repository
    provider: GITHUB
  vendor:
    terraform:
      manage_state: true
      version: "1.3.0"
```

{% endraw %}

We can then use a call to `templatefile` like the following to render this template:

{% raw %}

```terraform
templatefile("${path.module}/test.tftpl", {
  SPACE = "root"
})
```

{% endraw %}

This results in the following output when the template is rendered:

{% raw %}

```yaml
inputs:
  - id: stack_name
    name: Stack name
stack:
  name: ${{ inputs.stack_name }}
  space: root
  vcs:
    branch: main
    repository: my-repository
    provider: GITHUB
  vendor:
    terraform:
      manage_state: true
      version: "1.3.0"
```

{% endraw %}

## Variables

Since you probably don't want to create stacks with the exact same name and configuration, you'll use variables.

### Inputs

{% raw %}
Inputs are defined in the `inputs` section of the template. You can use them in the template by prefixing them with `${{ inputs.` and suffixing them with `}}`. For example, `${{ inputs.environment }}` will be replaced with the value of the `environment` input. You can use these variables in CEL functions as well. For example, `trigger_run: ${{ inputs.environment == 'prod' }}` will be replaced with `trigger_run: true` or `trigger_run: false` depending on the value of the `environment` input. To ensure an input variable is always recognized as a string, you can enclose the value in quotes `"${{ inputs.environment }}"`.
{% endraw %}

The input object has `id`, `name`, `description`, `type`, `default` and `options` fields. The mandatory fields are `id` and `name`.

The `id` is used to refer to the input in the template. The `name` and the `description` are just helper fields for the user in the Stack creation tab. The `type` is the [type of the input](#input-types). The `default` is an optional default value of the input. The `options` is a list of options for the `select` input type.

Example:

{% raw %}

```yaml
inputs:
  - id: app_name
    name: The name of the app
stack:
  name: ${{ inputs.app_name }}-my-stack
```

{% endraw %}

#### Input types

If the input `type` is not provided, it defaults to `short_text`. Other options are:

| Type         | Description                                                                      |
| ------------ | -------------------------------------------------------------------------------- |
| `short_text` | A short text input.                                                              |
| `long_text`  | A long text input. Typically used for multiline strings.                         |
| `secret`     | A secret input. The value of the input will be masked in the UI.                 |
| `number`     | An integer input.                                                                |
| `boolean`    | A boolean input.                                                                 |
| `select`     | A multi option input. In case of `select`, it is mandatory to provide `options`. |
| `float`      | A float input.                                                                   |

An example including all the types:

```yaml
inputs:
  - id: app_name
    name: The name of the stack
    # No type provided, defaults to short_text
  - id: description
    name: The description of the stack
    type: long_text
  - id: connstring
    name: Connection string to the database
    type: secret
  - id: number_of_instances
    name: The number of instances
    type: number
  - id: delete_protection
    name: Is delete protection enabled?
    type: boolean
  - id: environment
    name: The environment to deploy to
    type: select
    options:
      - prod
      - staging
      - dev
  - id: scale_factor
    name: The scale factor of the app
    type: float
    # You can optionally provide a default value
    default: 1.5
```

#### Maps

Maps is an additional object which can be included in the template. The structure of maps is key-value pairs where the value is another map.
Using maps you can preconfigure specific values in the template and allow users to set them in a determenistic way.
Maps cannot be used in the `inputs` section, neither can `inputs` be used in the `maps` section.

Example of using maps:

{% raw %}

```yaml
inputs:
  - id: env
    name: Env
    # This type can also be a regular free text input (string)
    type: select 
    options:
      - prod
      - dev

maps:
  prod:
   stack_name: prod-stack 
   descripiton: This is stack is in production
   manage_state: true
  dev:
   stack_name: dev-stack 
   descripiton: This is a development stack 
   manage_state: false

stacks:
  - key: mystack
    name: ${{ maps[inputs.env].stack_name }}
    space: root
    description: >
      ${{ maps[inputs.env].descripiton }}
    vcs:
      branch: master
      repository: empty
      provider: GITHUB
    vendor:
      terraform:
        manage_state: ${{ maps[inputs.env].manage_state }} 
        version: "1.3.0"
```

{% endraw %}

### Context

We also provide an input object called `context`. It contains the following properties:

| Property                 | Type                        | Description                                                                                        |
| ------------------------ | --------------------------- | -------------------------------------------------------------------------------------------------- |
| `time`                   | `google.protobuf.Timestamp` | UTC time of the evaluation of the template.                                                        |
| `random_string`          | `string`                    | A random string of 6 characters (numbers and letters, no special characters).                      |
| `random_number`          | `int`                       | A random number between 0 and 1000000.                                                             |
| `random_uuid`            | `string`                    | A random UUID.                                                                                     |
| `user.login`             | `string`                    | The login of the person who triggered the blueprint creation; as provided by the SSO provider.     |
| `user.name`              | `string`                    | The full name of the person who triggered the blueprint creation; as provided by the SSO provider. |
| `user.account`           | `string`                    | The account subdomain of the user who triggered the blueprint creation.                            |
| `blueprint.name`         | `string`                    | The name of the blueprint that was used to create the stack.                                       |
| `blueprint.space`        | `string`                    | The space ID of the blueprint that was used to create the stack.                                   |
| `blueprint.created_at`   | `google.protobuf.Timestamp` | The time when the blueprint was created.                                                           |
| `blueprint.updated_at`   | `google.protobuf.Timestamp` | The time when the blueprint was last updated.                                                      |
| `blueprint.published_at` | `google.protobuf.Timestamp` | The time when the blueprint was published.                                                         |
| `blueprint.labels`       | `list(string)`              | The labels of the blueprint.                                                                       |

Here is an example of using a few of them:

{% raw %}

```yaml
stack:
  name: integration-tests-${{ inputs.app }}-${{ context.random_string }}
  description: |
    Temporary integration test stack for ${{ inputs.app }}. Deployed in ${{ context.time.getFullYear() }}.
    The base blueprint was created at ${{ string(context.blueprint.created_at) }}.
  labels:
    - owner/${{ context.user.login }}
    - blueprints/${{ context.blueprint.name }}
  environment:
    variables:
      - name: DEPLOYMENT_ID
        value: "${{ context.random_uuid }}"
  schedules:
    delete:
      delete_resources: ${{ context.random_number % 2 == 0 }} # Russian roulette
      timestamp_unix: ${{ int(context.time) + duration("30m").getSeconds() }} # Delete the stack in 30 minutes
```

{% endraw %}

Results in:

```yaml
stack:
  name: integration-tests-my-app-vG3j3a
  description: |
    Temporary integration test stack for my-app. Deployed in 2023.
    The base blueprint was created at 2020-01-01T10:00:20.021-05:00.
  labels:
    - owner/johndoe
    - blueprints/my-blueprint
  environment:
    variables:
      - name: DEPLOYMENT_ID
        value: 6c9c4e3e-6b5d-4b3a-9c9c-4e3e6b5d4b3a
  schedules:
    delete:
      delete_resources: true # Russian roulette
      timestamp_unix: 1674139424 # Delete the stack in 30 minutes
```

Note that this is not a working example as it misses a few things (`inputs` section, `vcs` etc.), but it should give you an idea of what you can do.

!!! tip
    What can you do with `google.protobuf.Timestamp` and `google.protobuf.Duration`? Check out the [language definition](https://github.com/google/cel-spec/blob/v0.7.1/doc/langdef.md#list-of-standard-definitions){: rel="nofollow"}, it contains all the methods and type conversions available.

## Validation

We do not validate drafted blueprints, you can do whatever you want with them. However, if you publish your blueprint, we'll make sure it includes the required fields and you'll get an error if it doesn't.

**One caveat**: we cannot validate fields that have variables because we don't know the value of the variable. On the other hand, if you try to create a stack from the blueprint and supply the inputs to the template, we'll be able to do the full validation. Let's say:

{% raw %}

```yaml
inputs:
  - id: timestamp
    name: Delete timestamp of the stack
    type: number
stack:
  schedules:
    delete:
      timestamp_unix: ${{ inputs.timestamp }}
```

{% endraw %}

We cannot make sure that the input variable is indeed a proper 10 digit epoch timestamp, we will only find out once you supply the actual input.

### Schema

The up-to-date schema of a Blueprint is available through a [GraphQL query](../../integrations/api.md) for authenticated users:

```graphql
{
  blueprintSchema
}
```

!!! tip
    Remember that there are multiple ways to interact with Spacelift. You can use the [GraphQL API](../../integrations/api.md), the [CLI](https://github.com/spacelift-io/spacectl){: rel="nofollow"}, the [Terraform Provider](https://registry.terraform.io/providers/spacelift-io/spacelift/latest/docs){: rel="nofollow"} or the web UI itself if you're feeling fancy.

For simplicity, here is the current schema, but it might change in the future:

<details> <!-- markdownlint-disable-line MD033 -->
<summary>Click to expand</summary> <!-- markdownlint-disable-line MD033 -->

```json
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Blueprint",
    "type": "object",
    "properties": {
        "inputs": {
            "$ref": "#/definitions/inputs"
        },
        "options": {
            "$ref": "#/definitions/options"
        },
        "maps": {
            "$ref": "#/definitions/maps"
        },
        "stack": {
            "$ref": "#/definitions/stack"
        },
        "stacks": {
            "type": "array",
            "maxItems": 5,
            "items": {
                "$ref": "#/definitions/stackWithKey"
            }
        }
    },
    "additionalProperties": false,
    "allOf": [
        {
            "oneOf": [
                {
                    "required": [
                        "stack"
                    ]
                },
                {
                    "required": [
                        "stacks"
                    ]
                }
            ]
        },
        {
            "if": {
                "required": [
                    "stack"
                ]
            },
            "then": {
                "not": {
                    "required": [
                        "stacks"
                    ]
                }
            }
        },
        {
            "if": {
                "required": [
                    "stacks"
                ]
            },
            "then": {
                "not": {
                    "required": [
                        "stack"
                    ]
                }
            }
        }
    ],
    "definitions": {
        "maps": {
            "type": "object",
            "additionalProperties": {
                "type": "object",
                "additionalProperties": {
                    "oneOf": [
                        {
                            "type": "string"
                        },
                        {
                            "type": "number"
                        },
                        {
                            "type": "boolean"
                        }
                    ]
                }
            }
        },
        "inputs": {
            "type": "array",
            "items": {
                "$ref": "#/definitions/input"
            }
        },
        "input": {
            "type": "object",
            "oneOf": [
                {
                    "additionalProperties": false,
                    "required": [
                        "id",
                        "name"
                    ],
                    "properties": {
                        "id": {
                            "type": "string"
                        },
                        "name": {
                            "type": "string"
                        },
                        "description": {
                            "type": "string"
                        },
                        "default": {
                            "oneOf": [
                                {
                                    "type": "string"
                                },
                                {
                                    "type": "number"
                                },
                                {
                                    "type": "boolean"
                                }
                            ]
                        },
                        "type": {
                            "type": "string",
                            "enum": [
                                "short_text",
                                "long_text",
                                "secret",
                                "boolean",
                                "number",
                                "float"
                            ]
                        }
                    }
                },
                {
                    "additionalProperties": false,
                    "required": [
                        "id",
                        "name",
                        "type",
                        "options"
                    ],
                    "properties": {
                        "id": {
                            "type": "string"
                        },
                        "name": {
                            "type": "string"
                        },
                        "description": {
                            "type": "string"
                        },
                        "default": {
                            "oneOf": [
                                {
                                    "type": "string"
                                },
                                {
                                    "type": "number"
                                },
                                {
                                    "type": "boolean"
                                }
                            ]
                        },
                        "type": {
                            "type": "string",
                            "enum": [
                                "select"
                            ]
                        },
                        "options": {
                            "type": "array",
                            "minItems": 1,
                            "items": {
                                "type": "string"
                            }
                        }
                    }
                }
            ]
        },
        "stack": {
            "type": "object",
            "additionalProperties": false,
            "required": [
                "name",
                "space",
                "vcs",
                "vendor"
            ],
            "properties": {
                "name": {
                    "type": "string",
                    "minLength": 1
                },
                "description": {
                    "type": "string"
                },
                "labels": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                },
                "administrative": {
                    "type": "boolean"
                },
                "allow_promotion": {
                    "type": "boolean"
                },
                "auto_deploy": {
                    "type": "boolean"
                },
                "auto_retry": {
                    "type": "boolean"
                },
                "is_disabled": {
                    "type": "boolean"
                },
                "local_preview_enabled": {
                    "type": "boolean"
                },
                "protect_from_deletion": {
                    "type": "boolean"
                },
                "runner_image": {
                    "type": "string"
                },
                "secret_masking_enabled": {
                    "type": "boolean"
                },
                "space": {
                    "type": "string",
                    "minLength": 1
                },
                "worker_pool": {
                    "type": "string"
                },
                "attachments": {
                    "$ref": "#/definitions/attachment"
                },
                "environment": {
                    "type": "object",
                    "additionalProperties": false,
                    "properties": {
                        "mounted_files": {
                            "type": "array",
                            "items": {
                                "$ref": "#/definitions/mounted_file"
                            }
                        },
                        "variables": {
                            "type": "array",
                            "items": {
                                "$ref": "#/definitions/variable"
                            }
                        },
                        "stack_dependency_references": {
                            "type": "array",
                            "items": {
                                "$ref": "#/definitions/dependency_reference"
                            }
                        }
                    }
                },
                "hooks": {
                    "type": "object",
                    "additionalProperties": false,
                    "properties": {
                        "apply": {
                            "$ref": "#/definitions/before_after_hook"
                        },
                        "init": {
                            "$ref": "#/definitions/before_after_hook"
                        },
                        "plan": {
                            "$ref": "#/definitions/before_after_hook"
                        },
                        "perform": {
                            "$ref": "#/definitions/before_after_hook"
                        },
                        "destroy": {
                            "$ref": "#/definitions/before_after_hook"
                        },
                        "run": {
                            "$ref": "#/definitions/after_hook"
                        }
                    }
                },
                "schedules": {
                    "type": "object",
                    "additionalProperties": false,
                    "properties": {
                        "drift": {
                            "$ref": "#/definitions/drift_detection_schedule"
                        },
                        "tasks": {
                            "type": "array",
                            "items": {
                                "$ref": "#/definitions/task_schedule"
                            }
                        },
                        "delete": {
                            "$ref": "#/definitions/delete_schedule"
                        }
                    }
                },
                "vcs": {
                    "type": "object",
                    "oneOf": [
                        {
                            "additionalProperties": false,
                            "required": [
                                "branch",
                                "provider",
                                "repository"
                            ],
                            "properties": {
                                "branch": {
                                    "type": "string",
                                    "minLength": 1
                                },
                                "project_root": {
                                    "type": "string"
                                },
                                "project_globs": {
                                    "type": "array",
                                    "items": {
                                        "type": "string"
                                    }
                                },
                                "provider": {
                                    "type": "string",
                                    "enum": [
                                        "GITHUB",
                                        "GITLAB",
                                        "BITBUCKET_DATACENTER",
                                        "BITBUCKET_CLOUD",
                                        "GITHUB_ENTERPRISE",
                                        "SHOWCASE",
                                        "AZURE_DEVOPS"
                                    ]
                                },
                                "id": {
                                    "type": "string",
                                    "description": "The id of the VCS provider."
                                },
                                "namespace": {
                                    "type": "string"
                                },
                                "repository": {
                                    "type": "string",
                                    "minLength": 1,
                                    "description": "The name of the repository."
                                }
                            }
                        },
                        {
                            "additionalProperties": false,
                            "required": [
                                "branch",
                                "provider",
                                "repository_url"
                            ],
                            "properties": {
                                "branch": {
                                    "type": "string",
                                    "minLength": 1
                                },
                                "project_root": {
                                    "type": "string"
                                },
                                "project_globs": {
                                    "type": "array",
                                    "items": {
                                        "type": "string"
                                    }
                                },
                                "provider": {
                                    "type": "string",
                                    "enum": [
                                        "RAW_GIT"
                                    ]
                                },
                                "repository": {
                                    "type": "string",
                                    "description": "The name of the repository. If not provided, it'll be extracted from the repository_url."
                                },
                                "namespace": {
                                    "type": "string",
                                    "description": "The namespace of the repository. If not provided, it'll be extracted from the repository_url."
                                },
                                "repository_url": {
                                    "type": "string",
                                    "minLength": 1,
                                    "description": "The URL of the repository. This is only used for the 'GIT' provider."
                                }
                            }
                        }
                    ]
                },
                "vendor": {
                    "type": "object",
                    "additionalProperties": false,
                    "properties": {
                        "ansible": {
                            "$ref": "#/definitions/ansible_vendor"
                        },
                        "cloudformation": {
                            "$ref": "#/definitions/cloudformation_vendor"
                        },
                        "kubernetes": {
                            "$ref": "#/definitions/kubernetes_vendor"
                        },
                        "pulumi": {
                            "$ref": "#/definitions/pulumi_vendor"
                        },
                        "terraform": {
                            "$ref": "#/definitions/terraform_vendor"
                        },
                        "terragrunt": {
                            "$ref": "#/definitions/terragrunt_vendor"
                        }
                    }
                },
                "options": {
                    "$ref": "#/definitions/options"
                },
                "depends_on": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "minLength": 1
                    }
                },
                "key": {
                    "type": "string"
                }
            }
        },
        "stackWithKey": {
            "allOf": [
                {
                    "$ref": "#/definitions/stack"
                },
                {
                    "type": "object",
                    "required": [
                        "key"
                    ]
                }
            ]
        },
        "attachment": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "contexts": {
                    "type": "array",
                    "items": {
                        "$ref": "#/definitions/context"
                    }
                },
                "clouds": {
                    "type": "object",
                    "additionalProperties": false,
                    "properties": {
                        "aws": {
                            "$ref": "#/definitions/aws_attachment"
                        },
                        "azure": {
                            "$ref": "#/definitions/azure_attachment"
                        }
                    }
                },
                "policies": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                }
            }
        },
        "aws_attachment": {
            "type": "object",
            "additionalProperties": false,
            "required": [
                "id",
                "read",
                "write"
            ],
            "properties": {
                "id": {
                    "type": "string"
                },
                "read": {
                    "type": "boolean"
                },
                "write": {
                    "type": "boolean"
                }
            }
        },
        "azure_attachment": {
            "type": "object",
            "additionalProperties": false,
            "required": [
                "id",
                "read",
                "write",
                "subscription_id"
            ],
            "properties": {
                "id": {
                    "type": "string"
                },
                "read": {
                    "type": "boolean"
                },
                "write": {
                    "type": "boolean"
                },
                "subscription_id": {
                    "type": "string"
                }
            }
        },
        "context": {
            "type": "object",
            "additionalProperties": false,
            "required": [
                "id"
            ],
            "properties": {
                "id": {
                    "type": "string"
                },
                "priority": {
                    "type": "integer",
                    "minimum": 0
                }
            }
        },
        "mounted_file": {
            "type": "object",
            "additionalProperties": false,
            "required": [
                "path",
                "content"
            ],
            "properties": {
                "path": {
                    "type": "string"
                },
                "content": {
                    "type": "string"
                },
                "description": {
                    "type": "string"
                },
                "secret": {
                    "type": "boolean"
                }
            }
        },
        "dependency_reference": {
            "type": "object",
            "additionalProperties": false,
            "required": [
                "name",
                "from_stack",
                "output"
            ],
            "properties": {
                "name": {
                    "type": "string"
                },
                "from_stack": {
                    "type": "string"
                },
                "output": {
                    "type": "string"
                },
                "trigger_always": {
                    "type": "boolean"
                }
            }
        },
        "variable": {
            "type": "object",
            "additionalProperties": false,
            "required": [
                "name",
                "value"
            ],
            "properties": {
                "name": {
                    "type": "string"
                },
                "value": {
                    "type": "string"
                },
                "description": {
                    "type": "string"
                },
                "secret": {
                    "type": "boolean"
                }
            }
        },
        "after_hook": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "after": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "minLength": 1
                }
            }
        },
        "before_after_hook": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "before": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "minLength": 1
                },
                "after": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "minLength": 1
                }
            }
        },
        "drift_detection_schedule": {
            "type": "object",
            "additionalProperties": false,
            "required": [
                "cron",
                "reconcile"
            ],
            "properties": {
                "cron": {
                    "type": "array",
                    "items": {
                        "$ref": "#/definitions/cron_schedule",
                        "maxLength": 1
                    }
                },
                "reconcile": {
                    "type": "boolean"
                },
                "ignore_state": {
                    "type": "boolean"
                },
                "timezone": {
                    "type": "string"
                }
            }
        },
        "task_schedule": {
            "type": "object",
            "additionalProperties": false,
            "required": [
                "command"
            ],
            "oneOf": [
                {
                    "required": [
                        "command",
                        "cron"
                    ]
                },
                {
                    "required": [
                        "command",
                        "timestamp_unix"
                    ]
                }
            ],
            "properties": {
                "command": {
                    "type": "string",
                    "minLength": 1
                },
                "cron": {
                    "type": "array",
                    "items": {
                        "$ref": "#/definitions/cron_schedule",
                        "minLength": 1
                    }
                },
                "timestamp_unix": {
                    "type": "number",
                    "minimum": 1600000000
                },
                "timezone": {
                    "type": "string"
                }
            }
        },
        "cron_schedule": {
            "type": "string",
            "pattern": "^(\\*|\\d+|\\d+-\\d+|\\d+\\/\\d+)(\\s+(\\*|\\d+|\\d+-\\d+|\\d+\\/\\d+)){4}$"
        },
        "delete_schedule": {
            "type": "object",
            "additionalProperties": false,
            "required": [
                "timestamp_unix"
            ],
            "properties": {
                "delete_resources": {
                    "type": "boolean"
                },
                "timestamp_unix": {
                    "type": "number",
                    "minimum": 1600000000
                }
            }
        },
        "ansible_vendor": {
            "type": "object",
            "additionalProperties": false,
            "required": [
                "playbook"
            ],
            "properties": {
                "playbook": {
                    "type": "string",
                    "minLength": 1
                }
            }
        },
        "cloudformation_vendor": {
            "type": "object",
            "additionalProperties": false,
            "required": [
                "entry_template_file",
                "template_bucket",
                "stack_name",
                "region"
            ],
            "properties": {
                "entry_template_file": {
                    "type": "string",
                    "minLength": 1
                },
                "template_bucket": {
                    "type": "string",
                    "minLength": 1
                },
                "stack_name": {
                    "type": "string",
                    "minLength": 1
                },
                "region": {
                    "type": "string",
                    "minLength": 1
                }
            }
        },
        "kubernetes_vendor": {
            "type": "object",
            "additionalProperties": false,
            "required": [
                "namespace"
            ],
            "properties": {
                "namespace": {
                    "type": "string",
                    "minLength": 1
                }
            }
        },
        "pulumi_vendor": {
            "type": "object",
            "additionalProperties": false,
            "required": [
                "stack_name",
                "login_url"
            ],
            "properties": {
                "stack_name": {
                    "type": "string",
                    "minLength": 1
                },
                "login_url": {
                    "type": "string",
                    "minLength": 1
                }
            }
        },
        "terraform_vendor": {
            "type": "object",
            "additionalProperties": false,
            "required": [
                "manage_state"
            ],
            "properties": {
                "version": {
                    "type": "string"
                },
                "workspace": {
                    "type": "string"
                },
                "use_smart_sanitization": {
                    "type": "boolean"
                },
                "manage_state": {
                    "type": "boolean"
                },
                "workflow_tool": {
                    "type": "string",
                    "enum": [
                        "TERRAFORM_FOSS",
                        "CUSTOM",
                        "OPEN_TOFU"
                    ]
                }
            }
        },
        "terragrunt_vendor": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "terraform_version": {
                    "type": "string"
                },
                "terragrunt_version": {
                    "type": "string"
                },
                "use_run_all": {
                    "type": "boolean"
                },
                "use_smart_sanitization": {
                    "type": "boolean"
                },
                "terragrunt_tool": {
                    "type": "string",
                    "enum": [
                        "TERRAFORM_FOSS",
                        "OPEN_TOFU",
                        "MANUALLY_PROVISIONED"
                    ]
                }
            }
        },
        "options": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "trigger_run": {
                    "type": "boolean"
                },
                "do_not_create": {
                    "type": "boolean"
                }
            }
        }
    }
}
```

</details>
