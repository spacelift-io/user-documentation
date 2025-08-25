# Role-Based Access Control (RBAC)

Up until recently, Spacelift used **legacy system roles** with broad roles (Reader, Writer, Admin) to manage user permissions.
This approach worked for many organizations but lacked the granularity and flexibility needed for modern infrastructure management.
With the introduction of the **Custom RBAC** system, Spacelift has transformed how permissions are managed, enabling a more
fine-grained, composable approach to advanced access control.

## Custom RBAC vs legacy system roles

### Legacy system roles (previous approach)

The legacy system used three broad roles:

- **Reader**: View-only access to resources.
- **Writer**: Reader permissions + ability to trigger runs and modify environment variables.
- **Admin**: Writer permissions + ability to create/modify stacks and attachable entities.

!!! note "Migration to custom RBAC"
    Existing legacy system role assignments have been automatically migrated to equivalent custom RBAC roles:

    | Legacy Role | RBAC Equivalent |
    |-------------|-----------------|
    | Reader      | Space Reader    |
    | Writer      | Space Writer    |
    | Admin       | Space Admin     |

### Custom RBAC (current approach)

Custom RBAC decomposes these broad roles into **individual, composable actions**.

!!! example "Custom RBAC Example"
    Instead of giving an actor, like an API key, full **Writer** access (which includes many permissions that are not needed), you can create a custom "Deployment Operator" role with just these permissions:

    - `run:trigger`: Can trigger stack runs.
    - `run:read`: Can view run details.

    This approach provides exactly the access needed for deployment operations without extra permissions.

## Core architecture

In Spacelift's RBAC system, **actors** are entities that perform **actions** on **subjects** within **spaces**. This architecture allows for precise control over who can do what, where, and how.

### Actors: who performs actions

Actors include users, API keys, and IdP groups.

#### Users

Individual team members who are authenticated through your identity provider (GitHub, GitLab, Microsoft, Google, or SAML/OIDC
SSO).

##### User patterns

- Use IdP groups for role assignment when possible.
- Limit individual user role assignments to exceptional cases.
- Regular access reviews and cleanup.

#### API Keys

Programmatic access tokens for automation and CI/CD integration.

##### API key patterns

- Create purpose-specific keys with minimal required permissions.
- Use specific custom roles rather than broad predefined roles.
- Use environment-specific keys rather than shared keys.
- Use descriptive names that indicate purpose (e.g., "terraform-ci-prod").
- Include environment or project context in the name.
- Implement key rotation policies.
- Document the purpose and owner of each API key.
- Monitor API key usage through audit trails.

#### IdP Groups

Groups of users as defined by your identity provider.

##### Examples of group sources

**GitHub Teams**:

- Passed in the users' token.

**SAML/OIDC Groups**:

- Defined by your enterprise identity provider.
- Mapped through SAML assertions or OIDC claims.
- Group membership determined by your IdP's group policies.

##### IdP group patterns

**Functional Groups**: Organize groups by job function across the organization.

- `platform-engineers` → Full infrastructure management
- `application-developers` → Deployment capabilities only
- `security-auditors` → Read-only access across all spaces

**Project Groups**: Organize groups by project or product.

- `project-alpha-team` → Full access to "Project Alpha" space
- `project-beta-team` → Full access to "Project Beta" space

**Hybrid Approach**: Combine functional and project-based groups.

- Base permissions from functional groups.
- Additional project-specific permissions from project groups.

### Actions: the building blocks of permissions

Actions are the smallest unit of permission granularity in Spacelift's RBAC system. Each action defines a specific
operation that can be performed:

| Action           | Description                | Legacy Equivalent |
|------------------|----------------------------|-------------------|
| `run:trigger`    | Trigger stack runs         | Writer            |
| `stack:manage`   | Create and modify stacks   | Admin             |
| `stack:delete`   | Delete stacks              | Admin             |
| `context:read`   | View contexts              | Reader            |
| `context:manage` | Create and modify contexts | Admin             |
| `space:read`     | View space contents        | Reader            |
| `space:manage`   | Manage space settings      | Admin             |

!!! note "Expanding action catalog"
    The RBAC system supports a limited, but expanding set of actions. Spacelift continuously adds new actions based on user feedback and use cases.

### Subjects: what actions are performed on

Subjects are the resources that actors interact with, for example:

- **Stacks**: Infrastructure definitions, runs, and associated metadata.
- **Contexts**: Environment variables, mounted files, and configuration collections.
- **Policies**: Rules governing Spacelift behavior (approval, notification, etc.).

!!! warning "Space-level granularity"
    Currently, RBAC operates at the [**space level**](../spaces/access-control.md). All roles are bound to specific spaces and apply equally to all subjects within that space. Entity-level granularity (e.g., permissions for individual stacks) is not yet supported.

#### Stack access patterns

**Development Stacks**:

- Developers need full management capabilities.
- Frequent deployments and experimentation.
- Less restrictive approval requirements.

**Production Stacks**:

- Limited management access to senior engineers.
- Strict approval workflows.
- Enhanced audit and monitoring.

**Shared Infrastructure Stacks**:

- Platform team management.
- Application team read access.
- Cross-team coordination requirements.

#### Policy access patterns

**Centralized Governance**:

- Security team manages all policies.
- Consistent rules across the organization.
- Limited policy creation permissions.

**Federated Governance**:

- Teams manage policies for their own spaces.
- Organization-wide baseline policies.
- Team-specific additional policies.

### Spaces: the scope of permissions

All RBAC roles are **space-bound**, meaning:

- Roles are assigned to specific spaces.
- Permissions apply to all subjects within that space.
- Users need appropriate roles in each space they need to access.

#### Space hierarchy

Spaces can be organized hierarchically to reflect your organizational structure:

```text
Root Space
├── Infrastructure (Platform team management)
│   ├── Networking
│   ├── Security
│   └── Monitoring
├── Applications (Application teams)
│   ├── Frontend
│   ├── Backend
│   └── Mobile
└── Sandbox (Development and testing)
```

#### Space design patterns

**Isolation requirements**:

- Separate spaces for different environments (dev/staging/prod).
- Separate spaces for different teams or projects.
- Separate spaces for different compliance requirements.

**Permission boundaries**:

- Align space boundaries with permission requirements.
- Consider who needs access to what resources.
- Plan for space hierarchy and inheritance patterns.

## Roles

### Predefined roles

Spacelift provides three predefined roles (corresponding to the legacy system roles):

#### Space reader

**Actions**: Basic read permissions

- View stacks, contexts, policies, and runs.
- Add comments to runs for feedback.
- Cannot trigger actions or modify resources.
- Equivalent to legacy **Reader** role.

#### Space writer

**Actions**: Space Reader + multiple execution permissions

- All Space Reader permissions.
- Trigger stack runs.
- Execute tasks.
- Modify stack environment variables.
- Equivalent to legacy **Writer** role.

#### Space admin

**Actions**: Space Writer + management permissions

- All Space Writer permissions.
- Create and modify stacks.
- Create and modify contexts and policies.
- Manage space settings (when assigned to specific space).
- Equivalent to legacy **Admin** role.

!!! info "Root Space Admin"
    Users with Space Admin role on the **root** space become **Root Space Admins** with account-wide privileges including SSO setup, VCS configuration, and audit trail management.

### Custom roles

#### Create custom roles using the web UI

1. Go to **Organization Settings** → **Access Control Center** → **Roles**.
2. Click **Create Role** to start defining a new role.
3. **Define Role Properties**:
    - **Name**: Descriptive role name (e.g., "Infrastructure Developer").
    - **Description**: Clear explanation of the role's purpose.
    - **Actions**: Select specific permissions needed.

!!! note "Read access baseline"
    The `space:read` action is required to view any subjects within a space. Without it, users cannot see other resources even if they have permissions for them.

#### Create custom roles using the Terraform provider

Refer to the [Spacelift Terraform provider documentation](https://registry.terraform.io/providers/spacelift-io/spacelift/latest/docs/resources/role) for detailed instructions on creating custom roles programmatically.

## Role bindings (assigning roles to actors)

View more detailed instructions for assigning roles to:

- [Individual users](./assigning-roles-users.md)
- [API keys](./assigning-roles-api-keys.md)
- [IdP groups](./assigning-roles-groups.md)
