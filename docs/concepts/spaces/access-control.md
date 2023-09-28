# Access Control

With Spaces, the whole permission management process is done within [Login policies](../policy/login-policy.md) where you can specify what type of role a user gets within the given spaces.

## Roles

There are 3 roles that you can assign to users on a space-by-space basis:

- **Read** - cannot create or modify neither stacks nor any attachable entities, but can view them
- **Write** - an extension to **Read**, as it can actually trigger runs in the stacks it sees
- **Admin** - can create and modify stacks and attachable entities, as well as trigger runs

A special case is someone who is given Admin permissions to the `root` space - we would call that person a Root Space Admin.
Any Root Space Admin is perceived to be an admin of the whole account. Only they can modify the space tree or access account-wide settings.

!!! info
    Administrative stacks get the Admin role in the space they belong to.

!!! warning
    Administrative stacks in the legacy space get admin access to the root space for backward compatibility reasons.

A comparison table of what users with given roles are capable of can be found below.

| Action\Who                    | Root Space Admin | Admin | Writer | Reader |
|-------------------------------|------------------|-------|--------|--------|
| Setup SSO                     | ✅                | ❌     | ❌      | ❌      |
| Setup VCS                     | ✅                | ❌     | ❌      | ❌      |
| Manage Sessions               | ✅                | ❌     | ❌      | ❌      |
| Manage Spaces                 | ✅                | ❌     | ❌      | ❌      |
| Manage Login Policies         | ✅                | ❌     | ❌      | ❌      |
| Manage Stacks                 | ✅                | ✅     | ❌      | ❌      |
| Manage Worker Pools, Contexts | ✅                | ✅     | ❌      | ❌      |
| Trigger runs                  | ✅                | ✅     | ✅      | ❌      |
| View Stacks                   | ✅                | ✅     | ✅      | ✅      |
| View Spaces                   | ✅                | ✅     | ✅      | ✅      |
| View Worker Pools, Contexts   | ✅                | ✅     | ✅      | ✅      |

## Login Policies

The way you can control access to Spaces in your Spacelift account is by using [Login policies](../policy/login-policy.md).

We have introduced new rules that allow you to assign access to spaces:

- **space_read**
- **space_write**
- **space_admin**

Here is a valid login policy that uses all of them:

```opa
package spacelift

developers := { "bob" }
login   := input.session.login
is_developer { developers[login] }
allow { is_developer }

# Let's give every developer read access to any space
space_read[space.id] {
  space := input.spaces[_]
  is_developer
}

# Assign write role to developers for spaces with "developers-are-writers" label
space_write[space.id] {
  space := input.spaces[_]
  space.labels[_] == "developers-are-writers"
  is_developer
}

# Assign admin role for the root space for anyone in the admin team
space_admin["root"] {
  input.session.teams[_] == "admin"
}
```

!!! warning
    Please note that Login policies are only allowed to be created in the `root` space, therefore only `root` space admins and administrative stacks, as well as `legacy` space administrative stacks can create or modify them.

!!! warning
    A logged-in user's access levels only get updated when they log out and in again, so newly added spaces might not be visible to some users. An exception is that the space's creator immediately gets access to it.

## Inheritance

Inheritance is a toggle that defines whether a space inherits resources from its parent space or not. When set to true, any stack in the child space can use resources such as worker pools or contexts from the parent space. If a space inherits from a parent and its parent inherits from the grandparent, then the space inherits from the grandparent as well.

Inheritance also modifies how roles propagate between spaces.

In a scenario when inheritance between spaces is turned off, the roles are propagated only down the space tree. On the other hand, when inheritance is enabled, then a user with any role in the child space also gets **Read** role in their parent.

Below is a diagram that demonstrates how this all works in practice. This is a view for a user that was given the following roles by Login policies:

- **Read** in `read access space`
- **Write** in `write access space`
- **Admin** in `admin access space`

Dashed lines indicate a lack of inheritance, while when it's enabled the lines are solid.

![](<../../assets/screenshots/spaces_access_propagation.png>)

Let's analyze the tree starting from the left.

As mentioned, the user was granted **Write** access to the `write access space` space.
Because inheritance is enabled, they also received **Read** access to the `access propagates up` space and the `root` space. The reason for that is to allow users to see resources that their space can now use.

Next, the user was given **Admin** access to the `admin access space` space. Regardless of the inheritance being off, they also received **Admin** access to the `access propagates down` space.
This makes sense, as we want to allow admins to still manage their spaces subtree even if they want to disable resource sharing between some spaces.

Finally, the user was given **Read** access to the `read access space` space. Because inheritance is off, they did not receive **Read** access to the `legacy` space.

!!! info
    Inheritance works well with Policy Autoattachment. By creating a policy with an `autoattach:*` label you enforce it on all the stacks in all the spaces that inherit the space where the policy resides.
