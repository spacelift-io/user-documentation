# Migrating out of the legacy space

If you started using Spacelift before the introduction of spaces, most of your resources were moved to the `legacy` space to provide backwards compatibility with your existing setup. [Access policies](../policy/stack-access-policy.md) also only work in the `legacy` space.

To get the most out of Spacelift, you'll want to move out of the `legacy` space into other spaces. [Choose a new space](./structuring-your-spaces-tree.md#moving-an-attachable-resource) for each resource (stacks, policies, worker pools, contexts, etc.) in its settings. When doing so, remember:

1. Moving resources can't break any relationships between them. For example, if you have a policy attached to a stack, you can't move the policy to a space where it won't be accessible to the stack.
2. You have to move resources one by one, which means that moving stacks with their attachments (policies, contexts, worker pools, etc.) needs to be done in multiple steps.

## Migration process

1. Create your new space as a child of the `root` space with inheritance enabled.
2. Move all the attachable resources (policies, contexts, worker pools, etc.) from the `legacy` space to the `root` space. This way they're accessible from both the `legacy` space and your new space.
3. Move the stacks to your new space.
4. Move the attachable resources to your new space.

![Spaces tree with legacy space](<../../assets/screenshots/spaces_migration_1.png>)

## Replace access policies

To stop using access policies in the `legacy` space, implement [space access control](./access-control.md) and [RBAC](../policy/login-policy.md#rbac-role-assignment) via login policies. The moment the login policy specifies roles for a user for the `legacy` space, access policies will stop being evaluated for the user.
