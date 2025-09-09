# Stack

If you're managing your infrastructure in Spacelift, you're managing them with stacks. A stack is a combination of source code, the current state of the managed infrastructure (e.g. OpenTofu/Terraform state file) and the configuration ([environment](../configuration/environment.md) variables and mounted files). A stack is also an isolated, independent entity.

Unless you're only using Spacelift to host and test private [OpenTofu/Terraform modules](../../vendors/terraform/module-registry.md), your account should contain one or more stacks.

![Stacks list in UI](<../../assets/screenshots/stack/list/page-view.png>)

## What can I do with stacks?

- [Create, delete, and lock](./creating-a-stack.md) stacks.
- [Organize](./organizing-stacks.md) stacks.
- Configure [stack settings](./stack-settings.md).
- [Schedule](./scheduling.md) stack runs.
- Set up [stack dependencies](./stack-dependencies.md).
- [Detect drift](./drift-detection.md) in managed stacks.

## Stack state

Similar to [runs](../run/README.md) and [tasks](../run/task.md), stacks also have states that are generally equal to their most recent [tracked run state](../run/README.md#common-run-states).

The state is set to "None" on stacks with no runs:

![None state](<../../assets/screenshots/stack/list/none-state-item.png>)

Stack states show users the overall health of their infrastructure, and the level of development activity associated with it, at a glance.
