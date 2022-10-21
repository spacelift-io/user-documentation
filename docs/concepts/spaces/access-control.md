# Access Control

When introducing Spaces we had to redefine the Account permission model.

Until now, you could use Login Policies to allow or deny access to Spacelift, while also assigning account admins.
You would then have to use Access Policies to manage access to individual stacks for the non-admin users.
Every other entity such as worker pools, policies or contexts was available only to account admins.

With Spaces, we decided that it doesn't make sense anymore to define access on stack-by-stack basis, but instead, we should focus on assigning access to particular Spaces.
Therefore, in the Spaces world we are deprecating all the Access Policies.
Instead, whole permission management process will be done solely within Login Policies where you can now specify what type of role do user get within given spaces.

A core concept of access control with spaces is inheritance. Each space has a toggle that defines whether it inherits resources from its parent space or not.
This toggle also affects how do roles propagate between spaces.

## Roles

There are 3 roles that you can assign to users on the space-by-space basis:
- **Read** - cannot create or modify neither stacks nor any attachable entities, but can view them
- **Write** - an extension to **Read**, as it can actually trigger runs in the stacks they see
- **Admin** - can create and modify stacks and attachable entities, as well as trigger runs

A special case is someone who is given Admin permissions to the root space - we would call that person a "Root Space Admin".
Any Root Space Admin is perceived to be an admin of the whole account. Only them can modify the space tree or access account-wide settings.


!!! info
    Administrative stacks get Admin role in the space they belong to.

!!! warning
    Administrative stacks in the legacy space get admin access to the root space for backwards-compatibility reasons.

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


## Login policies

The way you are able to control access to Spaces in your Spacelift account is by using [Login Policies](../policy/login-policy.md).
We have introduced new boolean rules that allow you to assign access to spaces:

- **space_reader**
- **space_writer**
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
    Please note that Login Policies are only allowed to be created in the root space, therefore only root space admins, as well as legacy space administrative stacks can create or modify them.

!!! warning
    A logged-in user's access levels only get updated when they log out and in again, so newly added spaces might not be visible to some users. An exception is that the space's creator immediately gets access to it.

## Inheritance

The inheritance is a toggle that defines whether a space inherits resources from its parent space or not.
When set to true, any stack in the child space can use resources such as worker pools or contexts from the parent space.
If parent spaces inherits from their own parent then it's children can also use the same resources inherited from their grandparents and so on.

Inheritance, also modifies how roles propagate between spaces.

In a scenario when inheritance between spaces is turned off, the roles are propagated only down the space tree.
On the other hand, when inheritance is enabled user with any role in the child space also gets **Read** role in its parent.

Bellow is a diagram that demonstrates how this all work in practice. This is a view for a user at was given following roles by Login Policies:

- **Read** in 'read-access-space'
- **Write** in 'write-access-space'
- **Admin** in 'admin-access-space'

Dashed lines indicate disabled inheritance, while when it's enabled lines are solid.

![](<../../assets/screenshots/spaces_access_propagation.png>)

Let's analyze the tree starting from the left.

As mentioned, user has been given **Write** role in the 'write-access-space' space.
Because inheritance is enabled, they also received **Read** role in the 'access propagates up' space and the 'root' space.
The reason for that is to allow users to see resources that their space can now use.

Next, user was given **Admin** role in the 'admin-access-space' space. Regardless of the inheritance being off, they also received **Admin** role in the 'access propagates down'.
This makes sense, as we want to allow admins to still manage their spaces subtree even if they want to disable resource sharing between some spaces.

Finally, user was given **Read** role in the 'read-access-space' space. Because inheritance is off, they did not receive **Read** role in the 'legacy' space.

!!! info
    The inheritance works well with Policy Autoattachment. By creating a policy with `autoattach:*` label you enforce it on all the stacks in all the spaces that inherit the space where policy resides.

