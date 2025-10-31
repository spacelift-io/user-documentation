# Authorization & RBAC

Spacelift provides a comprehensive **Role-Based Access Control (RBAC)** system designed for enterprise infrastructure teams. RBAC enables fine-grained, customizable permissions giving you precise control over who can access what resources and perform which actions.

## Evolution from legacy system roles

Spacelift has evolved from simple **legacy system roles** (Read, Write, Admin) to a custom RBAC system that offers advanced access control:

- **Custom roles**: Create roles tailored to your organization's specific needs.
- **Granular actions**: Composable permissions like `run:trigger`, `stack:manage`.
- **Flexible assignment**: Assign roles to users, IdP groups, and API keys.
- **Space-based control**: All roles are bound to specific [Spaces](../spaces/README.md) for organized access management.

## Core RBAC architecture

RBAC operates on three fundamental concepts: actions, actors, and subjects.

### Actions

**Actions** are the smallest unit of permission granularity. They define specific operations that can be performed within Spacelift. Examples include:

- `run:trigger`: Trigger stack runs.
- `stack:manage`: Create and modify stacks.

### Actors

**Actors** are entities that perform actions in the system:

- **Users**: Individual team members authenticated through your identity provider.
- **API Keys**: Programmatic access tokens for automation.
- **IdP Groups**: Groups of users as defined by your identity provider.
- **Stacks**: Stacks that can assume roles to make changes inside of Spacelift.

### Subjects

**Subjects** are the resources being acted upon. Examples include:

- **Stacks**: Stacks managing infrastructure and their runs.
- **Contexts**: Collections of environment variables and files.
- **Policies**: Rules that govern various Spacelift behaviors.
- **Spaces**: Organizational containers for resources.

## Getting started with RBAC

### For new Spacelift users

If you're new to Spacelift, you can start using RBAC right away. Follow these steps to set up your RBAC configuration:

1. Navigate to **Organization Settings** → **Access Control Center** → **Roles**.
2. Review the predefined roles (Space Admin, Space Writer, Space Reader). These are equivalent to legacy roles.
3. (Optional) Create custom roles with specific actions for your use cases.
4. Assign roles to users and spaces.

### Existing users: migration from legacy roles

If you're currently using legacy system roles (Read/Write/Admin), your existing configurations have been automatically migrated to equivalent RBAC roles:

- **Reader** → **Space Reader**
- **Writer** → **Space Writer**
- **Admin** → **Space Admin**

## Authorization Strategies

Spacelift offers two primary approaches for managing user access:

### User management (recommended for most organizations)

- **GUI or API based**: Manage access using the Spacelift web interface or using the Terraform provider.
- **User-friendly**: Invite users and assign roles without writing policies.
- **IdP Integration**: Seamlessly integrate with your identity provider for user management.

### Login policies (advanced)

- **Policy-as-code**: Define authorization rules using [Open Policy Agent](https://www.openpolicyagent.org/) (OPA).
- **Dynamic**: Conditional role assignment based on user attributes.
- **Flexible**: Support for complex authorization logic.

## Key RBAC features

### Access control center

A dedicated section in _Organization Settings_ for managing your RBAC configuration:

- Create and manage custom roles.
- Assign roles to users, groups, and API keys.
- Monitor role assignments across spaces.

### Custom roles

Go beyond predefined roles by creating custom roles that match your organization's specific needs.

### Space-bound permissions

All roles are assigned to specific spaces, providing:

- **Isolation**: Permissions are contained within designated spaces.
- **Inheritance**: Leverage space hierarchies for permission flow.
- **Scalability**: Manage permissions at the appropriate organizational level.

## Next steps

Dive deeper into RBAC with these guides:

- **[RBAC System](rbac-system.md)**: Detailed explanation of Spacelift's RBAC implementation.

## Related Topics

- **[User Management](../user-management/README.md)**: Invite and manage team members.
- **[Spaces](../spaces/README.md)**: Organize resources with spaces.
- **[Login Policies](../policy/login-policy.md)**: Policy-based access control.
- **[Single Sign-On](../../integrations/single-sign-on/README.md)**: Enterprise identity integration.
