# IdP group role bindings

IdP groups can receive roles through direct group assignment. Assign roles to the entire group, which automatically applies to all members of that group.

## Assigning roles

### Assigning roles to IdP groups using the web UI

1. Prerequisites
    1. The selected management strategy for your organization must be User Management
    2. Your identity provider [must be connected to Spacelift](../../integrations/single-sign-on/README.md)
    3. You must have appropriate permissions to manage user group roles
    4. Target spaces must exist where you want to assign roles
2. Navigate to IdP Group Mapping
    1. Click your name in the bottom left corner of the Spacelift interface
    2. Go to **Organization Settings** → **Identity Management** -> **IdP group mapping**
3. Create IdP group mapping
    1. Click **Map IdP group**
    2. Enter the id of the IdP group (this is the id of the group in your identity provider, e.g., GitHub team slug)
    3. Select the Role you want to assign to the group
    4. Select the Space where the group should have this role
    5. Click **Add** to add role assignment
    6. Click **Add** to save the group mapping
4. Access Group Role Management
    1. Click on the group row in the group list
    2. Click the **Manage Roles** button
    3. This opens the group role assignment interface

### Assigning roles to IdP groups using the terraform provider

Refer to the [Spacelift Terraform provider documentation](https://registry.terraform.io/providers/spacelift-io/spacelift/latest/docs/resources/idp_group_mapping) for detailed instructions on creating IdP group mappings programmatically.

### Assigning roles to IdP groups using the login policies

1. Prerequisites
    1. The selected management strategy for your organization must be Login Policies
    2. You must have appropriate permissions to create or modify login policies
    3. Understanding of OPA/Rego policy language
2. Use the `roles` rule to assign roles to users:

```opa
package spacelift

allow { input.session.member }

# Assign role based on team membership
roles[space][role_id] {
    input.session.teams[_] == "team-name"
}
```

#### Individual group assignment

```opa
package spacelift

allow { input.session.member }

# DevOps team gets platform engineer role
roles["infrastructure"]["platform-engineer-role-id"] {
    input.session.teams[_] == "DevOps"
}

# Frontend team gets developer role
roles["frontend"]["developer-role-id"] {
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
roles["applications"]["developer-role-id"] {
    developer_teams[input.session.teams[_]]
}

# Assign platform access
roles["infrastructure"]["platform-role-id"] {
    platform_teams[input.session.teams[_]]
}
```

#### Hierarchical team access

```opa
package spacelift

allow { input.session.member }

# Junior developers: development only
roles["development"]["junior-dev-role-id"] {
    input.session.teams[_] == "Junior-Developers"
}

# Senior developers: development + staging
roles[space]["senior-dev-role-id"] {
    input.session.teams[_] == "Senior-Developers"
    senior_spaces := {"development", "staging"}
    senior_spaces[space]
}

# Team leads: all environments
roles[space]["team-lead-role-id"] {
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
roles["development"]["engineer-role-id"] {
    input.session.teams[_] == "Engineering"
}

# Operations department infrastructure access
roles["infrastructure"]["ops-role-id"] {
    input.session.teams[_] == "Operations"
}

# Security department audit access across all spaces
roles[space]["security-auditor-role-id"] {
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
roles["production"]["prod-deployer-role-id"] {
    deployment_teams := {"DevOps", "SRE", "Platform"}
    deployment_teams[input.session.teams[_]]

    # Additional condition: must also be in senior group
    input.session.teams[_] == "Senior-Engineers"
}
```

## Troubleshooting

### Common issues

**Group Permissions Not Working**:

- Verify group-to-role assignments are correct
- Check if user is actually a member of the group
- Ensure user has re-authenticated since group assignment
- Validate role includes required actions

**Conflicting Group Permissions**:

- Multiple groups can provide different roles
- Permissions are additive across group memberships
- Regular audit of group role combinations

### Debugging steps

1. **Verify Group Membership**: Check user is member of expected groups in IdP
2. **Validate Role Assignment**: Confirm group has correct role assignments
3. **Review Audit Logs**: Check for group-related permission errors

## Related Topics

- **[Assigning Roles to Users](assigning-roles-users.md)**: Individual user role assignment
- **[Assigning Roles to API Keys](assigning-roles-api-keys.md)**: Service account permissions
- **[Login Policies](../policy/login-policy.md)**: Policy-based access control
- **[Single Sign-On](../../integrations/single-sign-on/README.md)**: IdP integration setup
