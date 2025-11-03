# Access control

Spaces provide the organizational structure for Spacelift's [role-based access control (RBAC) system](../authorization/README.md). Permission management is handled through [login policies](../policy/login-policy.md) or [user management](../user-management/README.md) depending on your authorization strategy. All roles are assigned to specific spaces, providing precise control over who can access what resources.

## Roles and RBAC

### Predefined roles

Spacelift provides three predefined roles that can be assigned to users on a space-by-space basis:

- **Space Reader**: View-only access to resources within the space, can add comments to runs for collaboration.
- **Space Writer**: Space Reader permissions + ability to trigger runs and modify environment variables.
- **Space Admin**: Space Writer permissions + ability to create and modify stacks and attachable entities.

These predefined roles correspond to the legacy system roles (Read/Write/Admin) and provide a simple starting point for organizations new to RBAC.

### Custom roles

Beyond predefined roles, you can create [custom roles](../authorization/rbac-system.md#custom-roles) with precisely tailored permissions:

- **Granular actions**: Compose roles from specific actions like `run:trigger`, `stack:manage`, `context:read`.
- **Business-aligned**: Match roles to your organizational structure and job functions.
- **Principle of Least Privilege**: Grant exactly the permissions needed, nothing more.

!!! example "Custom Role Example"

    Instead of giving someone full **Space Admin** access, create a custom "Infrastructure Developer" role with just:

    - `space:read`: View space contents
    - `stack:read`: Understand configurations
    - `run:trigger`: Deploy changes
    - `run:read`: Monitor deployments

A "Root Space Admin" is a user given administrative permissions to the `root` space, which is the top-level space in Spacelift's hierarchy. This grants special permissions and allows them to manage the entire account, including modifying the space tree and accessing account-wide settings.

### Role permissions

| Action / Role                 | Root Space Admin | Space Admin | Space Writer | Space Reader |
|-------------------------------|------------------|-------------|--------------|--------------|
| Set up SSO                    | ✅                | ❌           | ❌            | ❌            |
| Set up VCS                    | ✅                | ❌           | ❌            | ❌            |
| Manage Sessions               | ✅                | ❌           | ❌            | ❌            |
| Manage Login Policies & User Management Controls  | ✅ | ❌      | ❌            | ❌            |
| Manage Audit Trails           | ✅                | ❌           | ❌            | ❌            |
| Manage Spaces                 | ✅                | ✅*          | ❌            | ❌            |
| Manage Stack Config Settings  | ✅                | ✅           | ❌            | ❌            |
| Manage Worker Pools, Contexts | ✅                | ✅           | ❌            | ❌            |
| Manage Stack Env Vars         | ✅                | ✅           | ✅            | ❌            |
| Trigger runs                  | ✅                | ✅           | ✅            | ❌            |
| View Stacks                   | ✅                | ✅           | ✅            | ✅            |
| View Spaces                   | ✅                | ✅           | ✅            | ✅            |
| View Worker Pools, Contexts   | ✅                | ✅           | ✅            | ✅            |

*Can only manage assigned space(s)

## Authorization methods

### User management

The [user management](../user-management/) interface provides a way to assign roles to users, groups, and API keys:

1. Click your name in the bottom-left of the screen, then **Organization settings**.
2. In the _Identity Management_ section, select **Users**, **IdP group mapping**, or **API keys**.
3. Assign predefined or custom roles to specific spaces.

See [assigning roles to users](../authorization/assigning-roles-users.md) for detailed instructions.

### Login policies (policy-as-code)

Login policies can only be created in the `root` space. Therefore, only `root` and `legacy` space admins and administrative stacks can create or modify them.

[Login policies](../policy/login-policy.md) enable programmatic role assignment using OPA/Rego:

#### RBAC role assignment

!!! note "Getting role slugs"

    To use custom roles in login policies, copy the role slug from **Organization Settings** → **Access Control Center** → **Roles** → select role → copy slug.

Use the `roles` rule to assign RBAC roles in login policies:

```opa
package spacelift

# Basic login permissions
allow { input.session.member }

# Assign RBAC roles using role slugs
roles["space-id"]["developer-role-slug"] {
    input.session.teams[_] == "Frontend"
}

roles["space-id"]["platform-engineer-role-slug"] {
    input.session.teams[_] == "DevOps"
}

# Assign admin role for root space
roles["root"]["space-admin-role-slug"] {
    input.session.teams[_] == "Admin"
}
```

If a user is logged in, their access levels will not change, so newly added spaces might not be visible. The user must log out and back in to see new spaces they're granted access to.

However, the space's creator immediately has access to it.

#### Legacy space rules (deprecated)

The legacy space rules are deprecated in favor of RBAC roles:

- **space_read** → Use RBAC roles with `space:read` action.
- **space_write** → Use RBAC roles with appropriate write actions.
- **space_admin** → Use RBAC roles with management actions.

## Inheritance

Inheritance is a toggle that defines whether a space inherits resources from its parent space or not. When set to `true`, any stack in the child space can use resources (such as worker pools or contexts) from the parent space. If a space inherits from a parent and its parent inherits from the grandparent, then the space inherits from the grandparent as well.

Inheritance also modifies how roles propagate between spaces:

- If inheritance between spaces is **disabled**, the roles are propagated only down the space tree.
- If inheritance is **enabled**, a user with _any_ role in the child space also gets the **Read** role in the parent space.

### Inheritance diagram

The user in this diagram was given these roles via login policies:

- **Read** in `read access space`.
- **Write** in `write access space`.
- **Admin** in `admin access space`.

Solid lines indicate where inheritance is enabled, while dashed lines indicate where inheritance is disabled.

![Space role inheritance diagram](<../../assets/screenshots/spaces_access_propagation.png>)

Let's analyze the tree starting from the left.

- `write access space`: The user was granted **Write** access. Because inheritance is enabled, they also received **Read** access to the `access propagates up` space and the `root` space, which allows the user to see the resources they can use from the parent spaces.
- `admin access space`: The user was granted **Admin** access. Even though inheritance is disabled, they also received **Admin** access to the `access propagates down` space because we want admins to be able to manage their spaces subtree, even if they want to disable resource sharing between some spaces.
- `read access space`: The user was given **Read** access. Because inheritance is disabled, they did not receive any access (read or write) to the `legacy` space.

## Related topics

- **[Authorization & RBAC](../authorization/README.md)**: Complete guide to Spacelift's authorization system.
- **[RBAC System](../authorization/rbac-system.md)**: Understanding roles, actions, and actors.
- **[User Management](../user-management/)**: GUI-based permission management.
- **[Login Policies](../policy/login-policy.md)**: Policy-as-code authorization.
