# Deprecated Policies

## Overview

Spacelift has deprecated two policy types in favor of the more powerful and flexible **approval policy**:

- **Initialization Policy** - Previously controlled whether runs could start
- **Task Policy** - Previously controlled which task commands could be executed

Both have been replaced by [approval policies](../approval-policy.md), which provide:

- Unified control for both runs and tasks
- Human review workflows with comments
- Role-based approval requirements
- Richer decision-making context

## Migration Path

All functionality from initialization and task policies can be replicated in approval policies, often with enhanced capabilities.

**[→ View the complete migration guide](./migrate-to-approval-policy.md)** with side-by-side examples and real-world use cases.

## Deprecated Policy Types

| Policy Type | What It Did | Replaced By |
|-------------|-------------|-------------|
| [Initialization](./run-initialization-policy.md) | Blocked runs before they started based on runtime config, branch names, or other pre-execution checks | [Approval Policy](../approval-policy.md) |
| [Task](./task-run-policy.md) | Restricted which commands could be executed as tasks based on user roles or command patterns | [Approval Policy](../approval-policy.md) |

## Timeline

- **Current status**: Deprecated (still functional)
- **Recommended action**: Migrate as soon as possible
- **End of life**: To be announced

## Need Help?

- Review the [migration guide](./migrate-to-approval-policy.md) for detailed examples
- Check our [policy examples library](https://github.com/spacelift-io/spacelift-policies-example-library){: rel="nofollow"}
- Contact [Spacelift support](../../../product/support/README.md#contact-support) for migration assistance
