# Deprecated Policies

## Overview

Spacelift has deprecated several policy types in favor of more modern, scalable approaches:

### Access Policies → Spaces

**Access policies** provided stack-level access control but have been replaced by [Spaces](../../spaces/access-control.md) and [login policies](../login-policy.md), which provide:

- Organizational structure aligned with teams
- Space-level RBAC with role inheritance
- Better scalability and performance
- Consistent access control across all resources

!!! warning "Deprecation timeline"
    Access policies will be **entirely disabled on May 30, 2026**. All access control must be migrated to Spaces before this date.

### Initialization & Task Policies → Approval Policies

**Initialization and task policies** controlled run and task execution but have been replaced by [approval policies](../approval-policy.md), which provide:

- Unified control for both runs and tasks
- Human review workflows with comments
- Role-based approval requirements
- Richer decision-making context

## Migration Guides

Choose the appropriate migration guide based on the policy type you're migrating:

- **[→ Access Policy Migration Guide](./migrate-to-spaces.md)** - Migrate from access policies to Spaces and login policies
- **[→ Initialization/Task Policy Migration Guide](./migrate-to-approval-policy.md)** - Migrate from initialization/task policies to approval policies

## Deprecated Policy Types

| Policy Type | What It Did | Replaced By | Timeline |
|-------------|-------------|-------------|----------|
| [Access](../stack-access-policy.md) | Controlled read/write access to individual stacks and modules | [Spaces](../../spaces/access-control.md) | **Disabled May 30, 2026** |
| [Initialization](./run-initialization-policy.md) | Blocked runs before they started based on runtime config, branch names, or other pre-execution checks | [Approval Policy](../approval-policy.md) | To be announced |
| [Task](./task-run-policy.md) | Restricted which commands could be executed as tasks based on user roles or command patterns | [Approval Policy](../approval-policy.md) | To be announced |

## Deprecation Timeline

### Access Policies

- **Current status**: Deprecated (still functional)
- **End of life**: **May 30, 2026**
- **Required action**: Migrate to Spaces before May 30, 2026

### Initialization & Task Policies

- **Current status**: Deprecated (still functional)
- **Recommended action**: Migrate to approval policies as soon as possible
- **End of life**: To be announced

## Need Help?

- Review migration guides:
    - [Access policy migration](./migrate-to-spaces.md)
    - [Initialization/task policy migration](./migrate-to-approval-policy.md)
- Check our [policy examples library](https://github.com/spacelift-io/spacelift-policies-example-library){: rel="nofollow"}
- Contact [Spacelift support](../../../product/support/README.md#contact-support) for migration assistance
