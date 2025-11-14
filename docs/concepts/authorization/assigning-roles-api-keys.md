# API key role bindings

[API keys](./../../integrations/api.md#spacelift-api-key) can receive roles through three methods:

- **Direct assignment**: Assign roles directly to the API key.
- **IdP group assignment**: Associate API keys with IdP groups to inherit group-based role assignment.
- **Login policy assignment**: Use OPA policies to assign roles based on API key attributes (this can include assignment based on IdP group membership).

!!! note "Immediate role changes"
    Except for login policies, role assignments and changes to roles take effect immediately (they force re-authentication if needed).

## Assign roles

### Assign roles to API keys directly using the web UI

!!! info "Permission Scope"
    - **Root Space Admins** can create/modify/delete API keys and manage role bindings across all spaces
    - **Non-root Space Admins** can view all API keys but only manage role bindings for spaces they administer; they cannot create/modify/delete API keys

1. Verify you meet the prerequisites:
    1. The selected management strategy for your organization must be User Management.
    2. The key must exist in your Spacelift organization.
    3. You must have Space Admin permissions on the target space where you want to assign roles (or Root Space Admin permissions for all spaces).
    4. Spaces where you want to assign roles must exist.
2. Navigate to _API Key Management_:
    1. Click your name in the bottom left corner of the Spacelift interface.
    2. Go to **Organization Settings**.
    3. Go to ** **API Keys** in the **Identity Management** section.
    4. Find the API key you want to assign roles to.
    5. Click on the API key row to open its details.
3. Access role management:
    1. In the API key details page, click **Manage Roles**.
    2. This opens the role assignment interface for the API key.
4. Assign roles:
    1. **Select Role**: Choose appropriate role for the automation.
    2. **Select Space**: Choose the space where the role applies.
    3. **Save Assignment**: Confirm the role assignment.

### Assign roles to API keys directly using the Terraform provider

Refer to [Spacelift Terraform provider documentation](https://registry.terraform.io/providers/spacelift-io/spacelift/latest/docs) for more details.

### Assign roles to API keys directly using login policies

1. Verify you meet the prerequisites:
    1. The selected management strategy for your organization must be Login Policies.
    2. You must have appropriate permissions to create or modify login policies.
    3. Understanding of OPA/Rego policy language.
2. Use the `roles` rule to assign roles to users:

```opa
package spacelift

# Allow API key login
allow {
    input.session.login == "api-key-name"
}

# Assign role to API key
roles[space][role_id] {
    input.session.login == "api-key-name"
}
```

#### By key name

```opa
package spacelift

allow { input.session.member }

# Assign role to specific API key
roles["production"]["deployer-role-id"] {
    input.session.login == "ci-cd-production"
}

roles["infrastructure"]["provisioner-role-id"] {
    input.session.login == "terraform-automation"
}
```

#### By key pattern

```opa
package spacelift

allow { input.session.member }

# Assign roles based on key naming patterns
roles["production"]["deployer-role-id"] {
    startswith(input.session.login, "ci-cd-")
}

roles["monitoring"]["reader-role-id"] {
    endswith(input.session.login, "-monitoring")
}
```

#### Separate keys per environment

```opa
package spacelift

allow { input.session.member }

# Development environment keys
roles["development"]["full-deployer-role-id"] {
    environment_keys := {
        "ci-cd-dev",
        "terraform-dev",
        "automation-dev"
    }
    environment_keys[input.session.login]
}

# Production environment keys (more restrictive)
roles["production"]["limited-deployer-role-id"] {
    production_keys := {
        "ci-cd-prod",
        "terraform-prod"
    }
    production_keys[input.session.login]
}
```

#### Multi-environment keys

```opa
package spacelift

allow { input.session.member }

# Keys that work across multiple environments
roles[space]["cross-env-role-id"] {
    cross_env_keys := {"backup-service", "monitoring-agent"}
    cross_env_keys[input.session.login]

    # Define allowed spaces
    allowed_spaces := {"development", "staging", "production"}
    allowed_spaces[space]
}
```

#### CI/CD pipeline keys

```opa
package spacelift

allow { input.session.member }

# GitHub Actions deployment key
roles["applications"]["github-deployer-role-id"] {
    input.session.login == "github-actions-deploy"
}

# GitLab CI deployment key
roles["applications"]["gitlab-deployer-role-id"] {
    input.session.login == "gitlab-ci-deploy"
}

# Jenkins deployment key
roles["applications"]["jenkins-deployer-role-id"] {
    input.session.login == "jenkins-deploy"
}
```

#### Infrastructure tools

```opa
package spacelift

allow { input.session.member }

# Terraform Cloud integration
roles["infrastructure"]["terraform-cloud-role-id"] {
    input.session.login == "terraform-cloud-integration"
}

# Ansible automation
roles["configuration"]["ansible-role-id"] {
    input.session.login == "ansible-automation"
}

# Kubernetes operator
roles["kubernetes"]["k8s-operator-role-id"] {
    input.session.login == "k8s-spacelift-operator"
}
```

#### Conditional API key access

```opa
package spacelift

allow { input.session.member }

# Time-based API key restrictions
roles["production"]["time-limited-role-id"] {
    input.session.login == "scheduled-deployment"
    is_deployment_window
}

# Helper rule for deployment windows
is_deployment_window {
    now := input.request.timestamp_ns
    clock := time.clock([now, "UTC"])

    # Allow deployments only during maintenance window
    # Tuesday and Thursday, 2-4 AM UTC
    weekday := time.weekday(now)
    maintenance_days := {"Tuesday", "Thursday"}
    maintenance_days[weekday]

    clock[0] >= 2
    clock[0] <= 4
}
```

#### IP-restricted API keys

```opa
package spacelift

allow { input.session.member }

# API keys restricted to specific networks
roles["production"]["secure-deployer-role-id"] {
    secure_keys := {"production-deploy", "critical-automation"}
    secure_keys[input.session.login]

    # Only allow from secure networks
    is_secure_network
}

is_secure_network {
    secure_cidrs := {
        "10.0.0.0/8",        # Corporate network
        "192.168.100.0/24"   # Secure CI/CD subnet
    }
    secure_cidrs[cidr]
    net.cidr_contains(cidr, input.request.remote_ip)
}
```

### Assign roles to API keys using IdP groups

See [IdP group role bindings](assigning-roles-groups.md) for details on how to assign roles to IdP groups. Once a role is assigned to an IdP group, all actors (api keys and users that your identity provider reports as being members of that group) will inherit the assigned roles.

## Remove an API key role binding

1. Navigate to API Key Management:
    1. Click your name in the bottom left corner of the Spacelift interface.
    2. Go to **Organization Settings**.
    3. Go to **API Keys** in the **Identity Management** section.
    4. Find the API key you want to assign roles to.
    5. Click on the API key row to open its details.
2. Access role management:
    1. In the API key details page, click **Manage Roles**.
    2. This opens the role assignment interface for the API key.
3. Remove role assignment:
    1. Find the role assignment to remove.
    2. Click **Unassign** from the dropdown.
    3. Confirm the removal.

## Multiple roles

Actors can have multiple roles across different spaces:

- Different roles in different spaces for varied access levels.
- Multiple roles in the same space (permissions are additive).
- Roles inherited from group membership plus individual assignments.

## Find role IDs

To use custom roles in login policies, you need their role slugs:

1. Navigate to **Organization Settings** → **Access Control Center** → **Roles**.
2. Click on the custom role you want to use.
3. Click **Copy slug** from the role detail page.
4. Use this slug in your login policy.

## Troubleshooting

### API Key authentication failures

- Verify key is active and not expired.
- Ensure key is being used with correct endpoints.
- Validate key format and encoding.

### Permission denied errors

- Confirm API key has required role assignments.
- Verify role includes necessary actions for the operation.
- Check if operation is being performed in correct space.
- Ensure space exists and API key has access.

### Inconsistent behavior

- API key permissions don't require re-authentication.
- Changes to role assignments take effect immediately.
- Check for policy conflicts or syntax errors.
- Validate role IDs are correct in login policies.

### Debugging

1. **Test API key authentication**: You can create an interactive session with an API key (as if it was a user) to test the key's permissions and actions. To do that, go to `<your-spacelift-subdomain>.spacelift.io/apikeytoken` and enter your API key.
2. **Check role assignments**: Confirm key has correct roles in target spaces.
3. **Validate actions**: Ensure assigned roles include required permissions.
4. **Test operations**: Use API key to perform expected operations.
5. **Review audit Logs**: Check for API key related errors or warnings.
6. **Policy validation**: If using login policies, verify syntax and logic, use the sample and simulate feature.

## Related Topics

- **[Assigning Roles to Users](assigning-roles-users.md)**: Individual user role assignment
- **[Assigning Roles to IdP Groups](assigning-roles-groups.md)**: Group-based role assignment
- **[RBAC System](rbac-system.md)**: Understanding Spacelift's RBAC
- **[API Integration](../../integrations/api.md)**: Using Spacelift's GraphQL API
