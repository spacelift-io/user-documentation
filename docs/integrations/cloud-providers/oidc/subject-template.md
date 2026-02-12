# Customizing the OIDC Subject Claim

## Why customize the subject claim?

By default, Spacelift generates OIDC tokens with a subject claim that includes the space ID (slug), but not the full hierarchical path of the space. This works well for simple setups, but can create challenges in more complex organizational structures.

### The problem with space slugs

Consider this space hierarchy:

```text
root
├── production
│   ├── us-east-1
│   └── eu-west-1
└── staging
    ├── us-east-1
    └── eu-west-1
```

With the default subject format, you might have:

- Stack in `/root/production/us-east-1` → `space:us-east-1:stack:infra:run_type:TRACKED:scope:write`
- Stack in `/root/staging/us-east-1` → `space:us-east-1:stack:infra:run_type:TRACKED:scope:write`

These two completely different spaces produce **identical subject claims** because they share the same slug (`us-east-1`). This makes it impossible to distinguish between them in cloud provider trust policies.

### The solution: Custom subject templates

Custom subject templates allow you to include the full space path in the subject claim, enabling you to:

- **Distinguish between identically-named spaces** in different branches of your hierarchy
- **Create hierarchical trust policies** that grant access to all spaces under a specific branch (e.g., all production spaces)
- **Simplify access management** by avoiding the need to update trust policies every time you add a new space

## What is the subject template?

The subject template controls the format of the `sub` (subject) claim in the OIDC JWT token that Spacelift generates for each run. This token is used when authenticating with cloud providers like AWS, GCP, and Azure.

### Default format

By default, the subject claim follows this format:

```text
space:{spaceId}:{callerType}:{callerId}:run_type:{runType}:scope:{scope}
```

**Example:**

```text
space:production:stack:my-infra:run_type:TRACKED:scope:write
```

### Customizable format

You can customize this format using placeholders. For example, to include the full space path:

```text
space:{spaceId}:space_path:{spacePath}:{callerType}:{callerId}:run_type:{runType}:scope:{scope}
```

**Example:**

```text
space:us-east-1:space_path:/root/production/us-east-1:stack:my-infra:run_type:TRACKED:scope:write
```

## Available placeholders

When configuring a custom subject template, you can use the following placeholders:

| Placeholder | Description | Example |
|------------|-------------|---------|
| `{spaceId}` | The space slug | `production` or `us-east-1` |
| `{spacePath}` | The full hierarchical path of the space | `/root/production/us-east-1` |
| `{callerType}` | The type of entity that owns the run | `stack` or `module` |
| `{callerId}` | The stack or module slug | `my-infra` |
| `{runId}` | The run ULID | `01HXX123ABC...` |
| `{runType}` | The type of run | `PROPOSED`, `TRACKED`, `TASK`, `TESTING`, or `DESTROY` |
| `{scope}` | The scope of the token | `read` or `write` |

!!! info
    The `{spacePath}` placeholder is only populated when included in your template. If you don't use it in your template, this custom claim won't be added to the token.

## How to configure

1. Navigate to **Organization Settings** → **Security** → **OIDC subject template**
2. Enter your custom template in the template field
3. Leave the field empty to use the default format
4. Click **Save** to apply the changes

!!! info
    This feature requires account administrator privileges.

## Template syntax and validation

### Template examples

Here are some common template patterns:

**Include full space path (recommended for hierarchical setups):**

```text
space:{spaceId}:space_path:{spacePath}:{callerType}:{callerId}:run_type:{runType}:scope:{scope}
```

Result: `space:us-east-1:space_path:/root/production/us-east-1:stack:infra:run_type:TRACKED:scope:write`

**Simplified format with path:**

```text
{spacePath}|{callerType}:{callerId}|{runType}|{scope}
```

Result: `/root/production/us-east-1|stack:infra|TRACKED|write`

**Custom separator style:**

```text
path:{spacePath}:type:{callerType}:caller:{callerId}:run:{runId}:scope:{scope}
```

Result: `path:/root/production/us-east-1:type:stack:caller:infra:run:01HXX123:scope:write`

### Validation rules

Templates are validated to ensure they:

- Do not exceed **1000 characters** in length
- Only contain valid placeholders
- Use only allowed characters: alphanumeric, `-`, `_`, `:`, `/`, `|`, `{`, `}`
- Do not contain spaces, newlines, tabs, or special characters like `&`, `=`, `?`, `#`, `@`, `%`
- Produce subject claims that do not exceed **2048 characters** when rendered

If your template fails validation, you'll see an error message explaining what needs to be fixed.

## Migration guide

!!! warning "Breaking change"
    Changing your subject template is a breaking change for existing cloud provider trust policies. You must update your trust policies **before** changing the template in Spacelift to avoid authentication failures.

### Safe migration process

Follow these steps to migrate safely:

1. **Update cloud provider trust policies** to accept **both** the old and new subject formats
2. **Test the dual-format policy** with a non-critical stack to ensure it works
3. **Configure the new template** in Spacelift (via UI or API)
4. **Verify successful authentication** by triggering runs and checking they can access cloud resources
5. **Remove the old format** from your trust policies after confirming everything works

### Example: Dual-format AWS trust policy

During migration, your AWS IAM role trust policy should accept both formats:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::123456789012:oidc-provider/demo.app.spacelift.io"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringLike": {
          "demo.app.spacelift.io:sub": [
            "space:production:*",
            "*:space_path:/root/production/*"
          ]
        }
      }
    }
  ]
}
```

!!! hint
    Replace `demo.app.spacelift.io` with the hostname of your Spacelift account, and adjust the space names to match your hierarchy.

Once you've verified that runs are authenticating successfully with the new format, you can remove the old format (`"space:production:*"`) from the policy.

## Use cases

### Hierarchical space authorization

The primary use case for custom subject templates is enabling hierarchical authorization in cloud providers.

**Scenario:** You want to grant access to all stacks in your production environment, regardless of which specific space they're in.

With the default template, you'd need to list each space individually:

```json
"StringLike": {
  "demo.app.spacelift.io:sub": [
    "space:production:*",
    "space:prod-us-east-1:*",
    "space:prod-eu-west-1:*"
  ]
}
```

This requires updating the policy every time you add a new production space.

**With `{spacePath}`**, you can create a single rule that covers the entire branch:

```json
"StringLike": {
  "demo.app.spacelift.io:sub": "*:space_path:/root/production/*"
}
```

Now, any stack in `/root/production/` or its child spaces automatically inherits access.

### Distinguishing identically-named spaces

**Scenario:** You have spaces with the same slug in different branches (e.g., `/root/production/us-east-1` and `/root/staging/us-east-1`).

With the default template, these produce identical subject claims, making it impossible to grant different permissions.

**With `{spacePath}`**, each space has a unique subject claim:

- Production: `*:space_path:/root/production/us-east-1:*`
- Staging: `*:space_path:/root/staging/us-east-1:*`

You can now create separate trust policies for each environment.

## Provider-specific considerations

Each cloud provider has different capabilities for matching the subject claim in trust policies:

- **AWS**: Supports wildcards (`*`) in `StringLike` conditions. See [AWS-specific examples](aws-oidc.md#using-custom-subject-templates).
- **GCP**: Supports CEL expressions and custom claim mappings. See [GCP-specific examples](gcp-oidc.md#using-space-paths-for-hierarchical-access-control).
- **Azure**: Requires exact matches with no wildcard support. See [Azure-specific examples](azure-oidc.md#using-custom-subject-templates).

Refer to the provider-specific documentation pages for detailed setup instructions and examples.

## Additional resources

- [OIDC Overview](README.md) - Learn about Spacelift's OIDC integration
- [AWS OIDC Integration](aws-oidc.md) - AWS-specific setup and examples
- [GCP OIDC Integration](gcp-oidc.md) - GCP-specific setup and examples
- [Azure OIDC Integration](azure-oidc.md) - Azure-specific setup and examples
