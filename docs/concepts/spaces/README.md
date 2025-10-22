# Spaces

Spaces delegate partial admin rights to specific, limited environments within Spacelift. A single team of admins cannot scale when tens (or hundreds) of people at your organization are using Spacelift daily, and not every person needs the same level of access.

Spaces are sets that can be filled with various attachable Spacelift resources:

- [Stacks](../stack/README.md)
- [Policies](../policy/README.md)
- [Contexts](../configuration/context.md)
- [Modules](../../vendors/terraform/module-registry.md)
- [Worker pools](../../concepts/worker-pools/)
- [Cloud integrations](../../getting-started/integrate-cloud/README.md)

Add multiple spaces to your Spacelift account to give a team the access they need without the permissions to the entire account or other teams' environments.

Initially, you start with a `root` and a `legacy` space. The `root` space is the top-level space of your account, while the `legacy` space exists for backward compatibility with pre-spaces RBAC. [You can then create more spaces](./creating-a-space.md) to build a tree of segregated environments.

## Best practices

Spaces let you give users limited admin access so they can create stacks, policies, etc. in their space without interfering with resources present in other spaces.

Additionally, you can share resources between spaces, which means you can have a single worker pool and a single set of policies that can be reused by the whole organization.

### Plan your space structure

Spaces are a hierarchical structure, with the `root` space at the top. You can create as many spaces as you need, and each space can have its own child spaces.

Child spaces can "inherit" Spacelift resources from their parents, but they can also have their own.

When planning your [space structure](./creating-a-space.md#spaces-diagram-view), consider the following:

- **Who needs access?:** Spaces control access to resources. Who needs access to production stacks? Who should be able to approve IAM changes?
- **How do you want to organize your spaces?:** Spaces organize your resources. Do you want to organize by team, environment, project, or some other way?
- **How do you want to share resources?:** Spaces can share resources. Through space inheritance, you can share policies, worker pools, and other attachable resources from parent to child spaces.

You will need to balance these considerations to create a space structure that works for your organization. For example:

![Spaces tree example](<../../assets/screenshots/best-practices/spaces/spaces-example.png>)

In this example, the final spaces inside the tree are `dev` and `prod`, which helps when granting production access to a smaller subset of users.

### Use spaces to control access

Spaces are a powerful tool for [controlling access to resources](./access-control.md). By creating spaces for different teams, you can ensure that only the right people have access to the right resources.

Ensure production Spacelift constructs are separate from development constructs. This can be done by creating a `prod` space and a `dev` space, for example.

Additionally, stacks can receive [role attachments](../authorization/assigning-roles-stacks.md) to perform operations with elevated permissions in their space and child spaces.

#### IDP groups for scalability

Use IDP groups to manage permissions efficiently, especially in larger teams. Inside Spacelift [login policies](../policy/login-policy.md#teams), you can grant access to specific spaces using the teams attribute.

Using the example spaces layout above, you can set up this rule to allow your users to write to the R&D Team space if they are assigned the R&D team in your IDP:

```rego
space_write[space.id] {
     space := input.spaces[_]
     space.name == "R&D Team"
     input.session.teams[_] == "R&D"
}
```

### Space inheritance

[Space inheritance](./access-control.md#inheritance) is a tool for sharing resources between spaces. When a space inherits from another space, it can access all the resources in the parent space.

Inheritance works well with policy autoattachment. By creating a policy with the `autoattach:*` label, you enforce the policy on all stacks in all spaces that inherit the space where the policy resides.

Another good use case for inheritance is keeping VCS integrations and worker pools managed in a single space and inherited by all the spaces that need them.
