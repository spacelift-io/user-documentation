# Template Configuration

This document provides comprehensive reference for writing template YAML configurations. Templates use a YAML-based configuration format that defines infrastructure, inputs, and deployment behavior.

## Template Body Structure

The template body uses YAML format with the **blueprintV2Schema**. Here's a minimal example:

{% raw %}

```yaml
inputs:
  - id: environment
    name: Environment
    type: select
    options:
      - dev
      - staging
      - prod
  - id: app_name
    name: Application Name
    type: short_text

stacks:
  - key: main
    name: ${{ inputs.app_name }}-${{ inputs.environment }}
    vcs:
      reference:
        value: main
        type: branch
      repository: my-infrastructure
      provider: GITHUB
    vendor:
      terraform:
        manage_state: true
        version: "1.5.0"
```

{% endraw %}

!!! important
    Templates use the **blueprintV2Schema** which requires the `stacks` array format (not a single `stack` object). Each stack must have a unique `key` field, and VCS configuration uses the `reference` structure with `value` and `type` fields.

    **Note:** The `space` field is NOT allowed in v2 schema stack definitions. Space assignment is handled at the template deployment level, not in the blueprint YAML.

!!! warning "Templating Restrictions"
    {% raw %}The following fields **cannot** use template expressions (`${{ }}`):{% endraw %}

    - **Stack keys** (`/stacks/*/key`) - Must be static strings
    - **Stack dependencies** (`/stacks/*/depends_on/*`) - Must be static references
    - **All VCS fields** (`/stacks/*/vcs/**`) - Including `repository`, `provider`, `namespace`, `reference.value`, `reference.type`, etc.
    - **Input definitions** (`/inputs/**`) - Including `id`, `name`, `type`, `options`, `default`, etc.

    Templating **is allowed** in fields like `name`, `description`, `labels`, `autodeploy`, `environment` variables, vendor configuration, and most other stack settings.

## Input Types

Templates support various input types to collect information from users:

| Type | Description | Use Case |
|------|-------------|----------|
| `short_text` | Single-line text input | Names, identifiers, short values |
| `long_text` | Multi-line text area | Descriptions, configurations, scripts |
| `secret` | Masked sensitive input | Passwords, API keys, tokens |
| `number` | Integer input | Counts, port numbers, limits |
| `float` | Decimal number input | Percentages, ratios, measurements |
| `boolean` | Checkbox | Feature toggles, flags |
| `select` | Dropdown with options | Predefined choices like environments |

## Input Definition

Each input is defined with the following properties:

{% raw %}

```yaml
inputs:
  - id: app_name              # Unique identifier for this input
    name: Application Name     # Display name shown to users
    description: The name of your application  # Optional help text
    type: short_text          # Input type
    default: my-app           # Optional default value
    validations:              # Optional validation rules
      required: true
      min_length: 3
      max_length: 20
      pattern: "^[a-zA-Z0-9-]+$"
```

{% endraw %}

### Input Properties

- **id** (required): Unique identifier used to reference the input in template expressions
- **name** (required): Human-readable display name shown in the deployment form
- **description** (optional): Help text explaining what the input is for
- **type** (required): Input type (see table above)
- **default** (optional): Default value if user doesn't provide one
- **validations** (optional): Validation rules to enforce
- **options** (required for select): Array of allowed values for select inputs

## Input Validations

Templates support validation rules to ensure users provide valid data:

### String Validation

```yaml
validations:
  required: true              # Field must be filled
  min_length: 3              # Minimum character count
  max_length: 50             # Maximum character count
  length_equal: 10           # Exact character count required
  pattern: "^[a-z-]+$"       # Regular expression pattern
```

### Number Validation

```yaml
validations:
  required: true              # Field must be filled
  greater_than: 0            # Value must be greater than
  greater_than_or_equal: 1   # Value must be >=
  less_than: 100             # Value must be less than
  less_than_or_equal: 99     # Value must be <=
  not_equal: 50              # Value cannot equal
  step: 2                    # Increment step (for integers)
```

### Boolean Validation

```yaml
validations:
  required: true              # Field must be filled (cannot be null)
```

### Select Validation

```yaml
type: select
options:                      # List of allowed values
  - dev
  - staging
  - prod
validations:
  required: true              # User must select a value
```

## Using Template Variables

{% raw %}

Template variables can be referenced throughout your configuration using the `${{ }}` syntax:

{% endraw %}

{% raw %}

```yaml
inputs:
  - id: environment
    name: Environment
    type: select
    options:
      - dev
      - prod

stacks:
  - key: main
    name: app-${{ inputs.environment }}
    description: '${{ inputs.environment == "prod" ? "Production" : "Development" }} environment'
    labels:
      - Environment/${{ inputs.environment }}
    vcs:
      reference:
        value: main
        type: branch
      repository: my-repo
      provider: GITHUB
    vendor:
      terraform:
        manage_state: true
        version: "1.5.0"
    environment:
      variables:
        - name: ENV
          value: ${{ inputs.environment }}
        - name: DEBUG
          value: '${{ inputs.environment == "dev" }}'
```

{% endraw %}

### Variable Syntax

{% raw %}

- Reference inputs: `${{ inputs.input_id }}`
- Use context variables: `${{ context.property }}`
- Use maps: `${{ maps[inputs.env].property }}`
- Apply CEL expressions: `${{ inputs.name.lowerAscii() }}`

{% endraw %}

### Templating Restrictions

!!! warning
    {% raw %}Not all fields support templating. The following paths **cannot** use `${{ }}` expressions:{% endraw %}

    **Structural Fields (must be static):**
    - `stacks.*.key` - Stack identifiers must be deterministic
    - `stacks.*.depends_on.*` - Dependencies must be known at parse time

    **VCS Configuration (must be static):**
    - `stacks.*.vcs.repository` - Repository name
    - `stacks.*.vcs.provider` - Provider type (GITHUB, GITLAB, etc.)
    - `stacks.*.vcs.namespace` - Organization/namespace
    - `stacks.*.vcs.reference.value` - Branch/tag/SHA value
    - `stacks.*.vcs.reference.type` - Reference type (branch/tag/sha)
    - `stacks.*.vcs.project_root` - Project root path

    **Input Definitions (must be static):**
    - `inputs.*.id` - Input identifiers
    - `inputs.*.name` - Input display names
    - `inputs.*.type` - Input types
    - `inputs.*.options` - Select options
    - `inputs.*.default` - Default values
    - `inputs.*.validations` - Validation rules

    **Why these restrictions?** These fields define the template's structure and must be deterministic at parse time. VCS fields determine which repository to use, so they cannot depend on runtime inputs.

    **What CAN be templated?** Most other fields including `name`, `description`, `labels`, `autodeploy`, `autoretry`, `administrative`, `environment` variables, vendor settings, hooks, schedules, and attachments.

## Context Variables

Templates provide built-in context variables for dynamic values:

{% raw %}

```yaml
stacks:
  - key: main
    name: app-${{ context.random_string }}
    description: Created at ${{ string(context.time) }}
    labels:
      - owner/${{ context.user.login }}
    vcs:
      reference:
        value: main
        type: branch
      repository: my-repo
      provider: GITHUB
    vendor:
      terraform:
        manage_state: true
        version: "1.5.0"
    environment:
      variables:
        - name: DEPLOYMENT_ID
          value: "${{ context.random_uuid }}"
```

{% endraw %}

### Available Context Properties

| Property | Type | Description |
|----------|------|-------------|
| `context.deployment.created_at` | Timestamp | Creation date of deployment |
| `context.deployment.name` | String | Name of deployment |
| `context.deployment.slug` | String | Slug of deployment |
| `context.time` | Timestamp | UTC time of deployment |
| `context.random_string` | String | Random 6-character string |
| `context.random_number` | Number | Random number (0-1000000) |
| `context.random_uuid` | String | Random UUID |
| `context.user.login` | String | User's login name |
| `context.user.name` | String | User's full name |
| `context.user.account` | String | Account subdomain |

## Stack Configuration

Templates can configure all stack settings using the blueprintV2Schema:

{% raw %}

```yaml
stacks:
  - key: main
    name: ${{ inputs.stack_name }}
    description: My application stack
    labels:
      - app/${{ inputs.app_name }}
      - env/${{ inputs.environment }}

    # Behavioral settings
    administrative: false
    autodeploy: true
    autoretry: false

    # VCS configuration (v2 schema format)
    vcs:
      reference:
        value: main
        type: branch  # Options: branch, tag, sha
      repository: my-repo
      provider: GITHUB
      namespace: my-org
      project_root: terraform/
      project_globs:
        - "modules/**"

    # Vendor configuration
    vendor:
      terraform:
        manage_state: true
        version: "1.5.0"
        workspace: ${{ inputs.environment }}
        workflow_tool: OPEN_TOFU  # Options: TERRAFORM_FOSS, OPEN_TOFU, CUSTOM

    # Environment configuration
    environment:
      variables:
        - name: ENVIRONMENT
          value: ${{ inputs.environment }}
        - name: APP_NAME
          value: ${{ inputs.app_name }}
        - name: API_KEY
          value: ${{ inputs.api_key }}
          secret: true

      mounted_files:
        - path: config.json
          content: |
            {
              "environment": "${{ inputs.environment }}",
              "features": {
                "feature_a": ${{ inputs.enable_feature_a }}
              }
            }
          secret: false

    # Attachments
    attachments:
      contexts:
        - id: my-context-id
          priority: 1
      policies:
        - my-policy-id
      clouds:
        aws:
          id: my-aws-integration-id
          read: true
          write: true
```

{% endraw %}

!!! note
    Templates use the **blueprintV2Schema** format. Key differences from the original Blueprint schema:
    - Must use `stacks` array (not a single `stack` object)
    - Each stack requires a unique `key` field
    - VCS configuration uses `reference.value` and `reference.type` instead of direct `branch`, `tag`, or `sha` fields
    - See the [v2 Schema Reference](#blueprintv2schema-key-differences) section for complete details

For complete stack configuration options, refer to the [Stack Configuration](../stack/README.md) documentation.

## Multiple Stacks

Templates can create multiple stacks in a single deployment:

{% raw %}

```yaml
inputs:
  - id: app_name
    name: Application Name

stacks:
  - key: frontend
    name: ${{ inputs.app_name }}-frontend
    vcs:
      reference:
        value: main
        type: branch
      repository: frontend-repo
      provider: GITHUB
    vendor:
      terraform:
        manage_state: true
        version: "1.5.0"

  - key: backend
    name: ${{ inputs.app_name }}-backend
    depends_on:
      - frontend
    vcs:
      reference:
        value: main
        type: branch
      repository: backend-repo
      provider: GITHUB
    vendor:
      terraform:
        manage_state: true
        version: "1.5.0"
```

{% endraw %}

!!! note
    When using multiple stacks, each stack must have a unique `key` field for dependency management.

## Stack Dependencies

You can create dependencies between stacks using the `depends_on` field or `stack_dependency_references`:

{% raw %}

```yaml
stacks:
  - key: database
    name: ${{ inputs.app_name }}-db
    vcs:
      reference:
        value: main
        type: branch
      repository: database-repo
      provider: GITHUB
    vendor:
      terraform:
        manage_state: true
        version: "1.5.0"

  - key: application
    name: ${{ inputs.app_name }}-app
    depends_on:
      - database
    environment:
      stack_dependency_references:
        - name: DB_CONNECTION_STRING
          from_stack: database
          output: connection_string
    vcs:
      reference:
        value: main
        type: branch
      repository: app-repo
      provider: GITHUB
    vendor:
      terraform:
        manage_state: true
        version: "1.5.0"
```

{% endraw %}

### Dependency Features

- **depends_on**: Ensures stacks are created in order
- **stack_dependency_references**: Pass outputs from one stack to another as environment variables
- Multiple dependencies can be specified
- Prevents circular dependencies

## Template Engine

Templates use the same template engine as Blueprints, based on [Google CEL](https://github.com/google/cel-spec){: rel="nofollow"}. The implementation is available on [GitHub](https://github.com/spacelift-io/celplate/){: rel="nofollow"}.

### Supported Functions

CEL supports various built-in functions:

- **String operations**: `contains`, `startsWith`, `endsWith`, `matches`, `replace`, `lowerAscii`, `upperAscii`, `split`, `join`
- **Operators**: `*`, `/`, `-`, `+`, `==`, `!=`, `<`, `<=`, `>`, `>=`, `&&`, `||`, `!`, `?:`
- **Type conversions**: `string()`, `int()`, `bool()`

### CEL Expression Examples

{% raw %}

```yaml
inputs:
  - id: app_name
    name: Application Name
  - id: environment
    name: Environment
    type: select
    options:
      - dev
      - prod

stacks:
  - key: main
    # String manipulation
    name: ${{ inputs.app_name.lowerAscii().replace(" ", "-") }}-${{ inputs.environment }}

    # Conditional logic
    description: '${{ inputs.environment == "prod" ? "Production environment" : "Development environment" }}'

    # Boolean conditions
    autodeploy: ${{ inputs.environment != 'prod' }}
    administrative: ${{ inputs.environment == 'prod' }}

    # String operations
    labels:
      - '${{ inputs.environment.upperAscii() }}'
      - app/${{ inputs.app_name.lowerAscii() }}

    vcs:
      reference:
        value: main
        type: branch
      repository: my-repo
      provider: GITHUB
    vendor:
      terraform:
        manage_state: true
        version: "1.5.0"
```

{% endraw %}

### YAML Syntax Validity

Reserved YAML characters (`:`, `?`, `>`, `|`) within CEL expressions require quotes:

{% raw %}

```yaml
# Invalid - YAML parsing error
name: ${{ condition ? "yes" : "no" }}

# Valid - quoted expression
name: '${{ condition ? "yes" : "no" }}'
```

{% endraw %}

## Maps

Maps allow you to preconfigure specific values and enable deterministic value selection:

{% raw %}

```yaml
inputs:
  - id: env
    name: Environment
    type: select
    options:
      - prod
      - dev

maps:
  prod:
    stack_name: production-app
    description: Production environment
    instance_count: 5
    manage_state: true
  dev:
    stack_name: development-app
    description: Development environment
    instance_count: 1
    manage_state: false

stacks:
  - key: main
    name: ${{ maps[inputs.env].stack_name }}
    description: ${{ maps[inputs.env].description }}
    vcs:
      reference:
        value: main
        type: branch
      repository: my-repo
      provider: GITHUB
    vendor:
      terraform:
        manage_state: ${{ maps[inputs.env].manage_state }}
        version: "1.5.0"
    environment:
      variables:
        - name: INSTANCE_COUNT
          value: "${{ maps[inputs.env].instance_count }}"
```

{% endraw %}

!!! note
    Maps cannot reference inputs in their definitions, and inputs cannot reference maps.

### Map Use Cases

- Environment-specific configurations
- Predefined resource sizes (small, medium, large)
- Regional settings
- Tier-based configurations (bronze, silver, gold)

## Schedules

Templates support scheduling for drift detection and scheduled tasks:

{% raw %}

```yaml
inputs:
  - id: enable_drift_detection
    name: Enable Drift Detection
    type: boolean
  - id: enable_reconcile
    name: Enable Auto-Reconcile
    type: boolean
    default: false

stacks:
  - key: main
    name: scheduled-stack
    vcs:
      reference:
        value: main
        type: branch
      repository: my-repo
      provider: GITHUB
    vendor:
      terraform:
        manage_state: true
        version: "1.5.0"
    schedules:
      # Drift detection
      drift:
        cron:
          - "0 2 * * *"  # Run daily at 2 AM
        reconcile: ${{ inputs.enable_reconcile }}
        ignore_state: false
        timezone: UTC

      # Scheduled tasks
      tasks:
        - command: "terraform plan"
          cron:
            - "0 0 * * 0"  # Weekly on Sunday at midnight
          timezone: UTC
        - command: "echo 'Health check'"
          cron:
            - "0 */6 * * *"  # Every 6 hours
          timezone: UTC
```

{% endraw %}

### Schedule Types

**Drift Detection:**

- Automatically check for configuration drift
- Option to reconcile differences automatically
- Configurable cron schedule
- Can ignore state file changes

**Scheduled Tasks:**

- Run arbitrary commands on a schedule
- Support for multiple scheduled tasks
- Each task has its own cron schedule
- Timezone configuration per task

## Hooks

Templates support lifecycle hooks for custom actions:

{% raw %}

```yaml
stacks:
  - key: main
    name: hooked-stack
    vcs:
      reference:
        value: main
        type: branch
      repository: my-repo
      provider: GITHUB
    vendor:
      terraform:
        manage_state: true
        version: "1.5.0"
    hooks:
      init:
        before: ["echo", "Initializing..."]
        after: ["echo", "Initialization complete"]

      plan:
        before: ["echo", "Planning changes..."]
        after: ["./notify-team.sh", "${{ inputs.environment }}"]

      apply:
        before: ["echo", "Applying changes..."]
        after: ["echo", "Deployment complete"]

      destroy:
        before: ["echo", "Destroying resources..."]
        after: ["echo", "Resources destroyed"]

      run:
        after: ["./cleanup.sh"]
```

{% endraw %}

### Hook Types

- **init**: Run before/after initialization
- **plan**: Run before/after planning
- **apply**: Run before/after applying changes
- **destroy**: Run before/after destroying resources
- **run**: Run after any run completes

### Hook Best Practices

1. **Keep hooks simple**: Complex logic belongs in the repository
2. **Use for notifications**: Alert teams about deployments
3. **Validate inputs**: Check prerequisites before operations
4. **Cleanup**: Remove temporary files after runs

## Best Practices

### Input Design

Good input design:

```yaml
inputs:
  - id: app_name
    name: Application Name
    description: A unique name for your application (lowercase, hyphens allowed)
    type: short_text
    validations:
      required: true
      min_length: 3
      max_length: 30
      pattern: "^[a-z0-9-]+$"

  - id: environment
    name: Environment
    description: Select the target environment for deployment
    type: select
    options:
      - dev
      - staging
      - prod
    default: dev
```

Bad input design:

```yaml
inputs:
  - id: x
    name: X
    type: short_text

  - id: env
    name: Env
    type: short_text  # Should be select with options
```

### Template Structure

1. **Organize inputs logically**: Group related inputs together
2. **Use descriptive IDs**: Make input IDs clear and meaningful
3. **Provide defaults**: Set sensible defaults for optional inputs
4. **Add descriptions**: Help users understand what each input does
5. **Validate thoroughly**: Use validation rules to prevent errors

### Variable Usage

1. **Use maps for complex logic**: Instead of many conditional expressions
2. **Keep expressions simple**: Complex logic can be hard to debug
3. **Quote when needed**: Remember YAML special character rules
4. **Use context variables**: For unique identifiers and timestamps

### Security

1. **Mark secrets**: Always use `secret: true` for sensitive values
2. **Validate inputs**: Prevent injection attacks with pattern validation
3. **Least privilege**: Configure minimal required permissions
4. **Audit hooks**: Review hook commands for security issues

## Examples

### Simple Web Application

{% raw %}

```yaml
inputs:
  - id: app_name
    name: Application Name
    type: short_text
    validations:
      required: true
      pattern: "^[a-z0-9-]+$"

  - id: environment
    name: Environment
    type: select
    options:
      - dev
      - prod
    default: dev

stacks:
  - key: main
    name: ${{ inputs.app_name }}-${{ inputs.environment }}
    autodeploy: ${{ inputs.environment == 'dev' }}

    vcs:
      reference:
        value: main
        type: branch
      repository: web-app-template
      provider: GITHUB

    vendor:
      terraform:
        manage_state: true
        version: "1.5.0"

    environment:
      variables:
        - name: ENVIRONMENT
          value: ${{ inputs.environment }}
        - name: APP_NAME
          value: ${{ inputs.app_name }}
```

{% endraw %}

### Multi-Stack Application with Dependencies

{% raw %}

```yaml
inputs:
  - id: app_name
    name: Application Name
    type: short_text
    validations:
      required: true

stacks:
  - key: database
    name: ${{ inputs.app_name }}-db
    vcs:
      reference:
        value: main
        type: branch
      repository: postgres-template
      provider: GITHUB
    vendor:
      terraform:
        manage_state: true
        version: "1.5.0"

  - key: backend
    name: ${{ inputs.app_name }}-api
    depends_on:
      - database
    environment:
      stack_dependency_references:
        - name: DATABASE_URL
          from_stack: database
          output: connection_string
    vcs:
      reference:
        value: main
        type: branch
      repository: api-template
      provider: GITHUB
    vendor:
      terraform:
        manage_state: true
        version: "1.5.0"

  - key: frontend
    name: ${{ inputs.app_name }}-web
    depends_on:
      - backend
    environment:
      stack_dependency_references:
        - name: API_URL
          from_stack: backend
          output: api_endpoint
    vcs:
      reference:
        value: main
        type: branch
      repository: frontend-template
      provider: GITHUB
    vendor:
      terraform:
        manage_state: true
        version: "1.5.0"
```

{% endraw %}

### Environment-Based Configuration with Maps

{% raw %}

```yaml
inputs:
  - id: app_name
    name: Application Name
    type: short_text

  - id: environment
    name: Environment
    type: select
    options:
      - dev
      - staging
      - prod

maps:
  dev:
    instance_type: t3.micro
    instance_count: 1
    autodeploy: true
    backup_enabled: false
  staging:
    instance_type: t3.small
    instance_count: 2
    autodeploy: true
    backup_enabled: true
  prod:
    instance_type: t3.medium
    instance_count: 3
    autodeploy: false
    backup_enabled: true

stacks:
  - key: main
    name: ${{ inputs.app_name }}-${{ inputs.environment }}
    autodeploy: ${{ maps[inputs.environment].autodeploy }}

    vcs:
      reference:
        value: main
        type: branch
      repository: app-template
      provider: GITHUB

    vendor:
      terraform:
        manage_state: true
        version: "1.5.0"

    environment:
      variables:
        - name: INSTANCE_TYPE
          value: ${{ maps[inputs.environment].instance_type }}
        - name: INSTANCE_COUNT
          value: "${{ maps[inputs.environment].instance_count }}"
        - name: BACKUP_ENABLED
          value: "${{ maps[inputs.environment].backup_enabled }}"
```

{% endraw %}

## Schema

The up-to-date schema of a Blueprint is available through a [GraphQL query](../../integrations/api.md) for authenticated users:

```graphql
{
  blueprintV2Schema
}
```

!!! tip
    Remember that there are multiple ways to interact with Spacelift. You can use the [GraphQL API](../../integrations/api.md), the [CLI](https://github.com/spacelift-io/spacectl){: rel="nofollow"}, the [Terraform Provider](https://registry.terraform.io/providers/spacelift-io/spacelift/latest/docs){: rel="nofollow"}, or the web UI.

### BlueprintV2Schema Key Differences

Templates use the **blueprintV2Schema** format, which has important differences from the original [Blueprint schema](../blueprint/README.md#schema):

#### Required Changes

| Aspect | Original Blueprint Schema | V2 Schema (Templates) |
|--------|---------------------------|----------------------|
| **Stack Definition** | Single `stack` object OR `stacks` array | Only `stacks` array (required) |
| **Stack Key** | Not required | Each stack must have unique `key` field |
| **VCS Reference** | Direct fields: `branch`, `tag`, `sha` | Structured: `reference.value` and `reference.type` |
| **Space Field** | Required `space` field in stack | NOT allowed (assigned at deployment) |
| **Stack Limit** | Max 5 stacks | Max 10 stacks |

#### VCS Configuration Comparison

**Original Blueprint Schema:**

```yaml
vcs:
  branch: main           # Direct field
  repository: my-repo
  provider: GITHUB
```

**V2 Schema (Templates):**

```yaml
vcs:
  reference:
    value: main          # Can be branch name, tag, or SHA
    type: branch         # Must specify: "branch", "tag", or "sha"
  repository: my-repo
  provider: GITHUB
```

#### Reference Types

The `reference.type` field accepts three values:

- `branch`: Use a branch name (e.g., `main`, `develop`)
- `tag`: Use a git tag (e.g., `v1.0.0`)
- `sha`: Use a specific commit SHA (e.g., `abc123def456`)

!!! tip
    When a template version is published, it's automatically pinned to the current commit SHA of the specified branch/tag, ensuring deterministic deployments.

#### Available Stack Properties

The blueprintV2Schema supports the following stack-level properties:

| Property | Type | Description |
|----------|------|-------------|
| `key` | string | **Required.** Unique identifier for the stack (used in dependencies) |
| `name` | string | **Required.** Stack display name (can be templated) |
| `description` | string | Optional description (can be templated) |
| `labels` | array | Optional labels for categorization (can be templated) |
| `administrative` | boolean | Mark stack as administrative (can be templated) |
| `autodeploy` | boolean | Enable automatic deployment on VCS changes (can be templated) |
| `autoretry` | boolean | Enable automatic retry on failure (can be templated) |
| `vcs` | object | **Required.** VCS configuration (cannot be templated) |
| `vendor` | object | **Required.** Infrastructure tool configuration (Terraform, Pulumi, etc.) |
| `environment` | object | Environment variables and mounted files (can be templated) |
| `attachments` | object | Contexts, policies, and cloud integrations |
| `hooks` | object | Lifecycle hooks (init, plan, apply, destroy) |
| `schedules` | object | Drift detection and scheduled tasks (supports `drift` and `tasks` only) |
| `depends_on` | array | Stack dependencies (cannot be templated) |
| `runner_image` | string | Custom runner image |
| `worker_pool` | string | Worker pool ID |
| `secret_masking_enabled` | boolean | Enable secret masking in logs |

!!! note
    Property names in v2 schema are **case-sensitive** and use **lowercase without underscores** for boolean flags (e.g., `autodeploy`, not `auto_deploy`). Some properties from the original Blueprint schema are not available in v2.

## Related Resources

- [Template Overview](README.md) - General information about templates
- [Templates Workbench](workbench.md) - Creating and managing templates
- [Template Deployments](deployments.md) - Deploying from templates
- [Blueprint Configuration](../blueprint/README.md) - Similar configuration reference
- [Stack Configuration](../stack/README.md) - Stack settings reference
