---
description: From this article you can learn how Pulumi is integrated into Spacelift
---

# Pulumi

!!! info
    Feature previews are subject to change, may contain bugs, and have not yet been ironed out based on real production usage.

On a high level, [Pulumi](https://github.com/pulumi/pulumi) has a very similar flow to Terraform. It uses a state backend, provides dry run functionality, reconciles the actual world with the desired state. In this article we'll dive into how each of the concepts in Spacelift translates into working with Pulumi.

However, if you're the type that prefers to start with doing, instead of reading too much, there are quickstarts for each of the runtimes supported by Pulumi:

* [C#](getting-started/c-sharp.md)
* [Go](getting-started/golang.md)
* [JavaScript](getting-started/javascript.md)
* [Python](getting-started/python.md)

In case you're just getting started with Pulumi, we'd recommend you to start with JavaScript. Believe it or not, it's actually the most pleasant experience we had with Pulumi! Later you can also easily switch to languages which compile to JavaScript, like TypeScript or ClojureScript.

The high level concepts of Spacelift don't change when used with Pulumi. Below, we'll cover a few lower level details, which may be of interest.

### Run Execution

#### Initialization

Previously described in [Run Initializing](../../concepts/run/#initializing), in Pulumi the initialization will run:

* `pulumi login` with your configured login URL
* `pulumi stack select --create --select` with your configured Pulumi stack name (the one you set in vendor-specific settings, not the Spacelift [Stack](../../concepts/stack/) name)

It will then commence to run all pre-initialization hooks.

#### Planning

We run `pulumi preview --refresh --diff --show-replacement-steps` in order to show planned changes.

#### Applying

We run `pulumi up --refresh --diff --show-replacement-steps` in order to apply changes.

### Policies

Most policies don't change at all. The one that changes most is the plan policy. Instead of the terraform raw plan in the `terraform` field, you'll get a `pulumi` field with the raw Pulumi plan and the following schema:

```
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
          "provider": "string - provider this resource stems from",
          "type": "string - resource type",
          "urn": "string - urn of this resource"
        },
        "old": {
          "custom": "boolean",
          "id": "string",
          "inputs": "object - input properties",
          "outputs": "object - output properties",
          "parent": "string - parent resource of this resource",
          "provider": "string - provider this resource stems from",
          "type": "string - resource type",
          "urn": "string - urn of this resource"
        },
        "op": "string - same, refresh, create, update, delete, create-replacement or delete-replaced",
        "provider": "string - provider this resource stems from",
        "type": "string - resource type",
        "urn": "string - urn of this resource"
      }
    ]
  },
  "spacelift": {"...": "..."}
}
```

Pulumi secrets are detected and encoded as "\[secret]" instead of the actual value, that's why there's no other string sanitization going on with Pulumi plans.

### Modules

Spacelift module CI/CD isn't currently available for Pulumi.
