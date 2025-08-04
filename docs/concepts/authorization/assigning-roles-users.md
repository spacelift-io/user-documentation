# User role bindings

Users can get permissions from three sources:

- **Direct Role Assignment**: Assign roles directly to individual users
- **IdP Group Assignment**: Assign roles based on group memberships defined in your identity provider
- **Login Policy**: Use Open Policy Agent (OPA) policies to dynamically assign roles (this can include assignment based on IdP group membership)

!!! note "Immediate Role Changes"
    Except for Login Policies, role assignments and changes to roles take effect immediately (they force re-authentication if needed).

## Assigning roles

### Assigning roles to users directly using the web UI

1. Prerequisites
    1. The selected management strategy for your organization must be User Management
    2. User must be invited to the Spacelift organization
    3. You must have appropriate permissions to manage user roles
    4. Target spaces must exist where you want to assign roles
2. Navigate to User Management:
    1. Click your name in the bottom left corner of the Spacelift interface
    2. Select **Organization Settings**
    3. Navigate to **Users** in the **Identity Management** section
    4. Find the user you want to modify
3. Access Role Management
    1. Click on the user's row in the user list
    2. Click the **Manage Roles** button
    3. This opens the role assignment interface
4. Assign Roles
    1. **Select Role**: Choose from predefined roles or custom roles
    2. **Select Space**: Choose the space where the role applies
    3. **Save Assignment**: Click **Add** to confirm the assignment

### Assigning roles to users directly using the terraform provider

Refer to [Spacelift Terraform provider documentation](https://registry.terraform.io/providers/spacelift-io/spacelift/latest/docs) for more details).

### Assigning roles to users directly using the login policies

1. Prerequisites
    1. The selected management strategy for your organization must be Login Policies
    2. You must have appropriate permissions to create or modify login policies
    3. Understanding of OPA/Rego policy language
2. Use the `roles` rule to assign roles to users:

```opa
package spacelift

# Basic login permission
allow { input.session.member }

# Role assignment syntax
roles[space_name][role_id] { condition }
```

#### Individual user assignment

```opa
package spacelift

allow { input.session.member }

# Assign platform engineer role to specific user
roles["infrastructure"]["platform-engineer-role-id"] {
    input.session.login == "alice@company.com"
}

# Assign multiple roles to same user
roles["development"]["developer-role-id"] {
    input.session.login == "alice@company.com"
}

roles["staging"]["developer-role-id"] {
    input.session.login == "alice@company.com"
}
```

#### Multiple users with same role

```opa
package spacelift

allow { input.session.member }

# Define user set
senior_engineers := {
    "alice@company.com",
    "bob@company.com",
    "charlie@company.com"
}

# Assign role to all users in set
roles["production"]["senior-developer-role-id"] {
    senior_engineers[input.session.login]
}
```

#### Environment-based access

```opa
package spacelift

allow { input.session.member }

# Junior developers: development only
roles["development"]["developer-role-id"] {
    input.session.teams[_] == "Junior-Developers"
}

# Senior developers: development + staging
roles[space]["developer-role-id"] {
    input.session.teams[_] == "Senior-Developers"
    environment_spaces := {"development", "staging"}
    environment_spaces[space]
}

# Lead developers: all environments
roles[space]["lead-developer-role-id"] {
    input.session.teams[_] == "Lead-Developers"
    all_spaces := {"development", "staging", "production"}
    all_spaces[space]
}
```

#### Time-based access

```opa
package spacelift

allow { input.session.member }

# Production access only during business hours
roles["production"]["prod-deployer-role-id"] {
    input.session.teams[_] == "SRE"
    is_business_hours
}

# Helper rule for business hours
is_business_hours {
    now := input.request.timestamp_ns
    clock := time.clock([now, "America/Los_Angeles"])
    weekday := time.weekday(now)

    # Monday through Friday, 9 AM to 5 PM
    not weekend[weekday]
    clock[0] >= 9
    clock[0] <= 17
}

weekend := {"Saturday", "Sunday"}
```

#### IP-based access

```opa
package spacelift

allow { input.session.member }

# Sensitive operations only from office network
roles["production"]["admin-role-id"] {
    input.session.teams[_] == "DevOps"
    is_office_network
}

# Helper rule for office network
is_office_network {
    office_networks := {
        "192.168.1.0/24",
        "10.0.0.0/8"
    }
    office_networks[network]
    net.cidr_contains(network, input.request.remote_ip)
}
```

### Assigning roles to users via IdP groups

See [IdP Group Role Bindings](assigning-roles-groups.md) for details on how to assign roles to IdP groups. Once a role is assigned to an IdP group, all actors (api keys and users that your identity provider reports as being members of that group) will inherit the assigned roles.

## Removing a user role binding

1. Navigate to User Management:
    1. Click your name in the bottom left corner of the Spacelift interface
    2. Select **Organization Settings**
    3. Navigate to **Users** in the **Identity Management** section
    4. Find the user you want to modify
2. Access Role Management
    1. Click on the user's row in the user list
    2. Click the **Manage Roles** button
    3. This opens the role assignment interface
3. Remove Role Assignment
    1. Find the role assignment to remove
    2. Click the **Unassign** button from the dropdown
    3. Confirm the removal

## Multiple roles

Actors can have multiple roles across different spaces:

- Different roles in different spaces for varied access levels
- Multiple roles in the same space (permissions are additive)
- Roles inherited from group membership plus individual assignments

## Getting role IDs

To use custom roles in login policies, you need their role IDs:

1. Navigate to **Organization Settings** → **Access Control Center** → **Roles**
2. Click on the custom role you want to use
3. Click **Copy ID** from the role detail page
4. Use this ID in your login policy

## Troubleshooting

### Common issues

**User Cannot See Resources**:

- Verify user has `space:read` action
- Check if user is assigned to correct space

**Role Assignment Not Taking Effect**:

- Check if login policy has syntax errors
- Verify role ID is correct in login policies

**Permission Denied Errors**:

- Verify user has required actions for the operation
- Check if operation is being performed in correct space
- Confirm role includes necessary permissions

**Login Policy Not Working**:

- Check policy syntax for errors
- Verify input data structure matches policy conditions
- Use policy sampling to debug input data
- Check for typos in team names or user logins
- Check for case sensitivity in team names and user logins

## Related Topics

- **[Assigning Roles to IdP Groups](assigning-roles-groups.md)**: Group-based role assignment
- **[Assigning Roles to API Keys](assigning-roles-api-keys.md)**: Service account permissions
- **[RBAC System](rbac-system.md)**: Understanding Spacelift's RBAC
- **[User Management](../user-management/README.md)**: User invitation and management
