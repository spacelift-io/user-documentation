# Access control

Spaces provide the organizational structure for Spacelift's [RBAC system](../authorization/README.md). Permission
management is handled through [Login policies](../policy/login-policy.md) or [User Management](../user-management/)
depending on your authorization strategy. All roles are assigned to
specific spaces, providing precise control over who can access what resources.

## Roles and RBAC

### Predefined roles

Spacelift provides three predefined roles that can be assigned to users on a space-by-space basis:

- **Space Reader** - View-only access to resources within the space, can add comments to runs for collaboration
- **Space Writer** - Space Reader permissions + ability to trigger runs and modify environment variables
- **Space Admin** - Space Writer permissions + ability to create and modify stacks and attachable entities

These predefined roles correspond to the legacy system roles (Read/Write/Admin) and provide a simple starting point for
organizations new to RBAC.

### Custom roles

Beyond predefined roles, you can create [custom roles](../authorization/rbac-system.md#custom-roles) with precisely
tailored permissions:

- **Granular Actions**: Compose roles from specific actions like `run:trigger`, `stack:manage`, `context:read`
- **Business-Aligned**: Match roles to your organizational structure and job functions
- **Principle of Least Privilege**: Grant exactly the permissions needed, nothing more

!!! example "Custom Role Example"
    Instead of giving someone full **Space Admin** access, create a custom "Infrastructure Developer" role with just:

    - `space:read`: View space contents
    - `stack:read`: Understand configurations
    - `run:trigger`: Deploy changes
    - `run:read`: Monitor deployments

A "Root Space Admin" is a user given administrative permissions to the `root` space, which is the top-level space in Spacelift's hierarchy. This gives them special permissions and allows them to manage the entire account, including modifying the space tree and accessing account-wide settings.

### Permission comparison

| Action\Role                   | Root Space Admin | Space Admin | Space Writer | Space Reader |
|-------------------------------|------------------|-------------|--------------|--------------|
| Setup SSO                     | ✅                | ❌           | ❌            | ❌            |
| Setup VCS                     | ✅                | ❌           | ❌            | ❌            |
| Manage Sessions               | ✅                | ❌           | ❌            | ❌            |
| Manage Login Policies         | ✅                | ❌           | ❌            | ❌            |
| Manage Audit Trails           | ✅                | ❌           | ❌            | ❌            |
| Manage Spaces                 | ✅                | ✅*          | ❌            | ❌            |
| Manage Stack Config Settings  | ✅                | ✅           | ❌            | ❌            |
| Manage Worker Pools, Contexts | ✅                | ✅           | ❌            | ❌            |
| Manage Stack Env Vars         | ✅                | ✅           | ✅            | ❌            |
| Trigger runs                  | ✅                | ✅           | ✅            | ❌            |
| View Stacks                   | ✅                | ✅           | ✅            | ✅            |
| View Spaces                   | ✅                | ✅           | ✅            | ✅            |
| View Worker Pools, Contexts   | ✅                | ✅           | ✅            | ✅            |

*Only when assigned to the specific space

## Authorization methods

### User management

The [User Management](../user-management/) interface provides a way to assign roles to users, groups, and API
keys:

1. Navigate to **Organization Settings** → **Identity Management**
2. Select **Users**, **IdP group mapping**, or **API keys**
3. Assign predefined or custom roles to specific spaces

See [assigning roles to users](../authorization/assigning-roles-users.md) for detailed instructions.

### Login policies (policy-as-code)

[Login policies](../policy/login-policy.md) enable programmatic role assignment using OPA/Rego:

#### Legacy space rules (deprecated)

The legacy space rules are deprecated in favor of RBAC roles:

- **space_read** → Use RBAC roles with `space:read` action
- **space_write** → Use RBAC roles with appropriate write actions
- **space_admin** → Use RBAC roles with management actions

#### RBAC Role Assignment

Use the `roles` rule to assign RBAC roles in login policies:

```opa
package spacelift

# Basic login permissions
allow { input.session.member }

# Assign RBAC roles using role IDs
roles["development"]["developer-role-id"] {
    input.session.teams[_] == "Frontend"
}

roles["infrastructure"]["platform-engineer-role-id"] {
    input.session.teams[_] == "DevOps"
}

# Assign admin role for root space
roles["root"]["space-admin-role-id"] {
    input.session.teams[_] == "Admin"
}
```

!!! note "Getting Role IDs"
    To use custom roles in login policies, copy the role ID from **Organization Settings** → **Access Control Center** → **Roles** → select role → copy ID.

!!! warning
    - Please note that Login policies are only allowed to be created in the `root` space, therefore only `root` space admins and administrative stacks, as well as `legacy` space administrative stacks can create or modify them.
    - A logged-in user's access levels only get updated when they log out and in again, so newly added spaces might not be visible to some users. An exception is that the space's creator immediately gets access to it.

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

## Related topics

- **[Authorization & RBAC](../authorization/README.md)**: Complete guide to Spacelift's authorization system
- **[RBAC System](../authorization/rbac-system.md)**: Understanding roles, actions, and actors
- **[User Management](../user-management/)**: GUI-based permission management
- **[Login Policies](../policy/login-policy.md)**: Policy-as-code authorization
