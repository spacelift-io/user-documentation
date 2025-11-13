# IdP group role bindings

IdP groups can receive roles through direct group assignment. Assign roles to the entire group, which automatically applies to all members of that group.

## Assign roles

### Assign roles to IdP groups using the web UI

!!! info "Permission Scope"
    - **Root Space Admins** can create/modify/delete IdP group mappings and manage role bindings across all spaces
    - **Non-root Space Admins** can view all IdP group mappings but only manage role bindings for spaces they administer; they cannot create/modify/delete IdP group mappings

1. Verify you meet the prerequisites:
    1. The selected management strategy for your organization must be User Management.
    2. Your identity provider [must be connected to Spacelift](../../integrations/single-sign-on/README.md).
    3. You must have Space Admin permissions on the target space where you want to assign roles (or Root Space Admin permissions for all spaces).
    4. Target spaces must exist where you want to assign roles.
2. Navigate to IdP group mapping:
    1. Click your name in the bottom left corner of the Spacelift interface.
    2. Go to **Organization Settings** → **Identity Management** -> **IdP group mapping**.
3. Create IdP group mapping:
    1. Click **Map IdP group**.
    2. Enter the id of the IdP group (this is the id of the group in your identity provider, e.g., GitHub team slug).
    3. Select the role you want to assign to the group.
    4. Select the space where the group should have this role.
    5. Click **Add** to add role assignment.
    6. Click **Add** to save the group mapping.
4. Access group role management:
    1. Click on the group row in the group list.
    2. Click **Manage Roles**.
    3. This opens the group role assignment interface.

### Assign roles to IdP groups using the Terraform provider

Refer to the [Spacelift Terraform provider documentation](https://registry.terraform.io/providers/spacelift-io/spacelift/latest/docs/resources/idp_group_mapping) for detailed instructions on creating IdP group mappings programmatically.

### Assign roles to IdP groups using the login policies

1. Verify you meet the prerequisites:
    1. The selected management strategy for your organization must be Login Policies.
    2. You must have appropriate permissions to create or modify login policies.
    3. Understanding of OPA/Rego policy language.
2. Use the `roles` rule to assign roles to users:

```opa
package spacelift

allow { input.session.member }

# Assign role based on team membership
roles[space][role_id] {
    input.session.teams[_] == "team-name"
}
```

#### RBAC role assignment

!!! note "Getting Role slugs"

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

#### Individual group assignment

```opa
package spacelift

allow { input.session.member }

# DevOps team gets platform engineer role
roles["space-id"]["platform-engineer-role-slug"] {
    input.session.teams[_] == "DevOps"
}

# Frontend team gets developer role
roles["space-id"]["developer-role-slug"] {
    input.session.teams[_] == "Frontend"
}
```

#### Multiple teams, same role

```opa
package spacelift

allow { input.session.member }

# Define team sets
developer_teams := {"Frontend", "Backend", "Mobile", "QA"}
platform_teams := {"DevOps", "SRE", "Platform"}

# Assign developer access
roles["space-id"]["developer-role-slug"] {
    developer_teams[input.session.teams[_]]
}

# Assign platform access
roles["space-id"]["platform-role-slug"] {
    platform_teams[input.session.teams[_]]
}
```

#### Hierarchical team access

```opa
package spacelift

allow { input.session.member }

# Junior developers: development only
roles["space-id"]["junior-dev-role-slug"] {
    input.session.teams[_] == "Junior-Developers"
}

# Senior developers: development + staging
roles[space]["senior-dev-role-slug"] {
    input.session.teams[_] == "Senior-Developers"
    senior_spaces := {"development", "staging"}
    senior_spaces[space]
}

# Team leads: all environments
roles[space]["team-lead-role-slug"] {
    input.session.teams[_] == "Team-Leads"
    all_spaces := {"development", "staging", "production"}
    all_spaces[space]
}
```

#### Department-based access

```opa
package spacelift

allow { input.session.member }

# Engineering department base access
roles["space-id"]["engineer-role-slug"] {
    input.session.teams[_] == "Engineering"
}

# Operations department infrastructure access
roles["space-id"]["ops-role-slug"] {
    input.session.teams[_] == "Operations"
}

# Security department audit access across all spaces
roles[space]["security-auditor-role-slug"] {
    input.session.teams[_] == "Security"
    # Apply to all spaces
    space := input.spaces[_].id
}
```

#### Project and functional groups

```opa
package spacelift

allow { input.session.member }

# Project-based access
roles["project-alpha"]["developer-role-id"] {
    input.session.teams[_] == "Project-Alpha-Team"
}

roles["project-beta"]["developer-role-id"] {
    input.session.teams[_] == "Project-Beta-Team"
}

# Functional role overlays
roles["infrastructure"]["platform-role-id"] {
    input.session.teams[_] == "Platform-Engineers"
}

roles[space]["security-role-id"] {
    input.session.teams[_] == "Security-Champions"
    # Security champions get audit access everywhere
    space := input.spaces[_].id
}
```

#### Multi-condition team assignment

```opa
package spacelift

allow { input.session.member }

# Production access requires both team membership and seniority
roles["production"]["prod-deployer-role-slug"] {
    deployment_teams := {"DevOps", "SRE", "Platform"}
    deployment_teams[input.session.teams[_]]

    # Additional condition: must also be in senior group
    input.session.teams[_] == "Senior-Engineers"
}
```

## Troubleshooting

### Group permissions not working

- Verify group-to-role assignments are correct.
- Check if user is actually a member of the group.
- Ensure user has re-authenticated since group assignment.
- Validate role includes required actions.

### Conflicting group permissions

- Multiple groups can provide different roles.
- Permissions are additive across group memberships.
- Regular audit of group role combinations.

## Debugging

1. **Verify Group Membership**: Check user is member of expected groups in IdP
2. **Validate Role Assignment**: Confirm group has correct role assignments
3. **Review Audit Logs**: Check for group-related permission errors

## Related Topics

- **[Assigning Roles to Users](assigning-roles-users.md)**: Individual user role assignment
- **[Assigning Roles to API Keys](assigning-roles-api-keys.md)**: Service account permissions
- **[Login Policies](../policy/login-policy.md)**: Policy-based access control
- **[Single Sign-On](../../integrations/single-sign-on/README.md)**: IdP integration setup
