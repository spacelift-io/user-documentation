# Permissions

When introducing Spaces we had to redefine the Account permission model.

Until now, you could use Login Policies to allow or deny access to Spacelift, while also assigning account admins.
You would then have to use Access Policies to manage access to individual stacks for the non-admin users.

With Spaces, we decided that it doesn't make sense anymore to define access on stack-by-stack basis, but instead, we should focus on assigning access to particular Spaces.
Therefore, in the Spaces world we are deprecating all the Access Policies.
Instead, whole permission management process will be done solely within Login Policies where you can now define permissions in a much more granular manner.

## Roles

In general, there are 3 roles that you can assign to users on the space-by-space basis:
1. Admin
1. Writer
1. Reader

A special case is someone who is given Admin permissions to the root space - we would call that person a "Root Space Admin".
Any Root Space Admin is perceived to be an admin of the whole account. Only them can modify the space tree or access account-wide settings.

A comparison table of what users with given roles are capable of can be found below:

| Action\Who                            | Root Space Admin | Space Admin | Writer | Reader |
|---------------------------------------|------------------|-------------|--------|--------|
| Setup SSO                             | ✅                | ❌           | ❌      | ❌      |
| Setup VCS                             | ✅                | ❌           | ❌      | ❌      |
| Manage Sessions                       | ✅                | ❌           | ❌      | ❌      |
| Create\Modify Spaces                  | ✅                | ❌           | ❌      | ❌      |
| Create\Modify Login Policies          | ✅                | ❌           | ❌      | ❌      |
| Create\Modify Stacks                  | ✅                | ✅           | ❌      | ❌      |
| Create\Modify Worker Pools, Contexts  | ✅                | ✅           | ❌      | ❌      |
| Trigger runs                          | ✅                | ✅           | ✅      | ❌      |
| View Stacks                           | ✅                | ✅           | ✅      | ✅      |
| View Spaces                           | ✅                | ✅           | ✅      | ✅      |
| View Worker Pools, Policies, Contexts | ✅                | ✅           | ✅      | ✅      |



## Login policies

The way you are able to control access to Spaces in your Spacelift account is by using [Login Policies](TODO://URL).



