# Spaces Best Practices

Every stack, context, cloud integration, and other Spacelift element resides inside a “space.”
Think of this as your organizational structure for Spacelift: Who needs access to what in order to do some task?

## Plan your space structure

Spaces are a hierarchical structure, with the `root` space at the top.
You can create as many spaces as you need, and each space can have its own subspaces.
Subspaces can "inherit" spacelift constructs from their parents, but they can also have their own.
This is a powerful tool for organizing your resources, but it can also be a bit overwhelming if you don’t plan it out.

When planning your space structure, consider the following:

- **Who needs access?** Spaces are a way to control access to resources. Does Jimmy-Developer need access to production stacks? Should Sally-Security-Engineer approve IAM changes?
- **How do you want to organize your spaces?** Spaces are a way to organize your resources. Do you want to organize by team, by environment, by project?
- **How do you want to share resources?** Spaces are a way to share resources. Through space inheritance you can share policies, worker pools, and other resources from parent to child spaces.

You will need to balance these considerations to create a space structure that works for your organization.
An example of an organization based structure might look like the following.

![](<../../assets/screenshots/best-practices/spaces/spaces-example.png>)

Note how the final spaces inside the tree are `dev` and `prod`, this is good to keep in mind as you build out your space structure so you can grant production access to a subset of users.

## Use spaces to control access

Spaces are a powerful tool for controlling access to resources.
By creating spaces for different teams, you can ensure that only the right people have access to the right resources.
You should, specifically, ensure production Spacelift constructs are separate from development constructs. This can be done by creating a `prod` space and a `dev` space, for example.
Additionally, Administrative stacks get the Admin role in the space they belong to. (Administrative stacks in the legacy space get admin access to the root space for backward compatibility reasons.)

### IDP Groups for Scalability

Utilize IDP groups to manage permissions efficiently, especially in larger teams.
Inside Spacelift login policies, you can grant access to specific Spaces using the teams attribute.
Using the above example spaces layout, you can set up the following rule to allow your users to write to the R&D Team space if they are assigned the R&D team in your IDP:

```rego
space_write[space.id] {
     space := input.spaces[_]
     space.name == "R&D Team"
     input.session.teams[_] == "R&D"
}
```

### Space Inheritance

Space inheritance is a tool for sharing resources between spaces.
When a space inherits from another space, it gets access to all the resources in the parent space.

Inheritance works well with Policy Autoattachment. By creating a policy with an `autoattach:*` label you enforce the policy on all the stacks in all the spaces that inherit the space where the policy resides.

Another good use case for inheritance is keeping VCS integrations and Worker Pools managed in a single space and inherited by all the spaces that need them.
