---
description: Learn how Pulumi integrates with Spacelift in this article.
---

# Pulumi

!!! info
    Feature previews are subject to change, may contain bugs, and have not yet been refined based on real production usage.

At a high level, [Pulumi](https://github.com/pulumi/pulumi){: rel="nofollow"} works similarly to Terraform. It uses a state backend, supports dry runs, and reconciles the actual infrastructure with your desired state. In this article, we’ll explain how Spacelift concepts map to Pulumi workflows.

If you prefer hands-on learning, check out our quickstart guides for each Pulumi-supported runtime:

- [C#](./c-sharp.md)
- [Go](./golang.md)
- [Javascript](./javascript.md)
- [Python](./python.md)

If you’re new to Pulumi, we recommend starting with Javascript—it’s the most user-friendly experience we’ve had with Pulumi. You can easily switch to other languages that compile to Javascript, like TypeScript or ClojureScript, later on.

The core concepts of Spacelift remain the same when using Pulumi. Below, we’ll cover some lower-level details that may be helpful.

## Run Execution

### Initialization

As described in [Run Initializing](../../concepts/run/README.md#initializing), Pulumi initialization runs the following:

- `pulumi login` with your configured login URL
- `pulumi stack select --create --select` with your configured Pulumi stack name (set in vendor-specific settings, not the Spacelift [Stack](../../concepts/stack/README.md) name)

After this, all pre-initialization hooks will run.

### Planning

We use `pulumi preview --refresh --diff --show-replacement-steps` to display planned changes.

### Applying

We use `pulumi up --refresh --diff --show-replacement-steps` to apply changes.

### Additional CLI Arguments

You can pass additional CLI arguments using the `SPACELIFT_PULUMI_CLI_ARGS_preview`, `SPACELIFT_PULUMI_CLI_ARGS_up`, and `SPACELIFT_PULUMI_CLI_ARGS_destroy` environment variables.

## Policies

Most policies remain unchanged. The main difference is with the plan policy. Instead of a raw Terraform plan in the `terraform` field, you’ll receive a `pulumi` field containing the raw Pulumi plan, following this schema:

```json
{
  "pulumi": {
    "steps": [
      {
        "new": {
          "custom": "boolean",
          "id": "string",
          "inputs": "object - input properties",
          "outputs": "object - output properties",
          "parent": "string - parent resource of this resource",
          "provider": "string - provider this resource comes from",
          "type": "string - resource type",
          "urn": "string - resource URN"
        },
        "old": {
          "custom": "boolean",
          "id": "string",
          "inputs": "object - input properties",
          "outputs": "object - output properties",
          "parent": "string - parent resource of this resource",
          "provider": "string - provider this resource comes from",
          "type": "string - resource type",
          "urn": "string - resource URN"
        },
        "op": "string - same, refresh, create, update, delete, create-replacement, or delete-replaced",
        "provider": "string - provider this resource comes from",
        "type": "string - resource type",
        "urn": "string - resource URN"
      }
    ]
  },
  "spacelift": {"...": "..."}
}
```

Pulumi secrets are detected and encoded as `[secret]` instead of showing the actual value. For this reason, no additional string sanitization is performed on Pulumi plans.

## Limitations

- Spacelift module CI/CD is not available for Pulumi.
- Import is not supported for Pulumi. Instead, you can run a task to import resources into your state.
