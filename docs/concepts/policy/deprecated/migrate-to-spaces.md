# Migrating from access policies to Spaces

!!! warning "Access policy deprecation"
    Access policies are deprecated and will be entirely disabled on **May 30, 2026**. All access control must be migrated to [Spaces](../../spaces/access-control.md) and [login policies](../login-policy.md) before this date.

This guide helps you migrate from stack-level access policies to space-based RBAC. While Spaces provide a more scalable and maintainable approach to access control, some advanced access policy patterns require adaptation.

## Understanding the architectural shift

Access policies and Spaces represent fundamentally different approaches to access control:

| Aspect | Access Policies (Deprecated) | Spaces (Current) |
|--------|------------------------------|------------------|
| **Granularity** | Stack/module level | Space level |
| **Evaluation** | Per-request (dynamic) | At login (session-based) |
| **Control mechanism** | OPA/Rego policies attached to stacks | RBAC roles assigned to spaces |
| **Flexibility** | Highly dynamic (time, IP, state) | Organizational structure |
| **Scalability** | Can become complex with many stacks | Designed for large organizations |

!!! info "Why the change?"
    Access policies worked well for small teams but became difficult to manage at scale. Spaces provide:

    - Clear organizational structure aligned with your teams
    - Consistent RBAC across all Spacelift resources
    - Better performance and auditability
    - Simplified permission management through space inheritance

## Migration strategy overview

The migration process typically follows these steps:

1. **Audit existing access policies** - Identify all access policies and their rules
2. **Design space structure** - Plan spaces that reflect your organizational boundaries
3. **Map policies to spaces** - Determine which access patterns map to spaces vs login policies
4. **Implement space structure** - Create spaces and move stacks
5. **Configure access control** - Set up login policies or user management
6. **Test and validate** - Verify all users have appropriate access
7. **Remove access policies** - Clean up deprecated policies

## Common migration patterns

### Team-based access

The most common access policy pattern maps directly to Spaces.

#### Before: Access policy

=== "Rego v1"
    ```rego
    package spacelift

    # Engineering team gets read access
    read if {
        some team in input.session.teams
        team == "Engineering"
    }

    # DevOps team gets write access
    write if {
        some team in input.session.teams
        team == "DevOps"
    }
    ```

=== "Rego v0"
    ```rego
    package spacelift

    # Engineering team gets read access
    read { input.session.teams[_] == "Engineering" }

    # DevOps team gets write access
    write { input.session.teams[_] == "DevOps" }
    ```

#### After: Spaces + login policy

!!! tip "Using IdP group mappings"
For simpler setups, you can use the [user management UI](../../user-management/README.md) to map IdP groups directly to space roles without writing login policies.

**Step 1**: Create appropriate spaces

```hcl
resource "spacelift_space" "engineering" {
  name            = "Engineering"
  parent_space_id = "root"
  description     = "Engineering team infrastructure"
}
```

**Step 2**: Move stacks to the engineering space

```hcl
resource "spacelift_stack" "example" {
  name     = "Example Stack"
  space_id = spacelift_space.engineering.id
  # ... other configuration
}
```

**Step 3**: Configure access via login policy

=== "Rego v1"
    ```rego
    package spacelift

    # Basic login permissions
    allow if input.session.member

    # Engineering team - read access
    roles[spacelift_space.engineering.id] contains "space-reader" if {
        some team in input.session.teams
        team == "Engineering"
    }

    # DevOps team - write access
    roles[spacelift_space.engineering.id] contains "space-writer" if {
        some team in input.session.teams
        team == "DevOps"
    }
    ```

=== "Rego v0"
    ```rego
    package spacelift

    # Basic login permissions
    allow { input.session.member }

    # Engineering team - read access
    roles[spacelift_space.engineering.id]["space-reader"] {
        input.session.teams[_] == "Engineering"
    }

    # DevOps team - write access
    roles[spacelift_space.engineering.id]["space-writer"] {
        input.session.teams[_] == "DevOps"
    }
    ```

---

### Environment separation

Separating access by environment (dev/staging/prod) is a core Spaces use case.

#### Before: Access policy with labels

=== "Rego v1"
    ```rego
    package spacelift

    # Developers: write to dev, read to prod
    write if {
        some team in input.session.teams
        team == "Developers"
        some label in input.stack.labels
        label == "dev"
    }

    read if {
        some team in input.session.teams
        team == "Developers"
        some label in input.stack.labels
        label == "production"
    }

    # SREs: write to everything
    write if {
        some team in input.session.teams
        team == "SRE"
    }
    ```

=== "Rego v0"
    ```rego
    package spacelift

    # Developers: write to dev, read to prod
    write {
        input.session.teams[_] == "Developers"
        input.stack.labels[_] == "dev"
    }

    read {
        input.session.teams[_] == "Developers"
        input.stack.labels[_] == "production"
    }

    # SREs: write to everything
    write {
        input.session.teams[_] == "SRE"
    }
    ```

#### After: Environment-based spaces

**Step 1**: Create environment spaces

```hcl
resource "spacelift_space" "dev" {
  name            = "Development"
  parent_space_id = "root"
  description     = "Development environment"
}

resource "spacelift_space" "production" {
  name            = "Production"
  parent_space_id = "root"
  description     = "Production environment"
}
```

**Step 2**: Move stacks to appropriate spaces based on environment

```hcl
# Move dev stacks
resource "spacelift_stack" "app_dev" {
  name     = "App - Development"
  space_id = spacelift_space.dev.id
  branch   = "develop"
  # ... other configuration
}

# Move prod stacks
resource "spacelift_stack" "app_prod" {
  name     = "App - Production"
  space_id = spacelift_space.production.id
  branch   = "main"
  # ... other configuration
}
```

**Step 3**: Configure differentiated access

=== "Rego v1"
    ```rego
    package spacelift

    allow if input.session.member

    # Developers - write to dev
    roles[spacelift_space.dev.id] contains "space-writer" if {
        some team in input.session.teams
        team == "Developers"
    }

    # Developers - read production
    roles[spacelift_space.production.id] contains "space-reader" if {
        some team in input.session.teams
        team == "Developers"
    }

    # SREs - write to all environments
    roles[spacelift_space.dev.id] contains "space-writer" if {
        some team in input.session.teams
        team == "SRE"
    }

    roles[spacelift_space.production.id] contains "space-writer" if {
        some team in input.session.teams
        team == "SRE"
    }
    ```

=== "Rego v0"
    ```rego
    package spacelift

    allow { input.session.member }

    # Developers - write to dev
    roles[spacelift_space.dev.id]["space-writer"] {
        input.session.teams[_] == "Developers"
    }

    # Developers - read production
    roles[spacelift_space.production.id]["space-reader"] {
        input.session.teams[_] == "Developers"
    }

    # SREs - write to all environments
    roles[spacelift_space.dev.id]["space-writer"] {
        input.session.teams[_] == "SRE"
    }

    roles[spacelift_space.production.id]["space-writer"] {
        input.session.teams[_] == "SRE"
    }
    ```

!!! tip "Reducing duplication with helper rules"
    Use Rego helper functions to reduce duplication when assigning the same role across multiple spaces:

    === "Rego v1"
        ```rego
        sre_spaces := {spacelift_space.dev.id, spacelift_space.production.id}

        roles[space_id] contains "space-writer" if {
            some team in input.session.teams
            team == "SRE"
            some space_id in sre_spaces
        }
        ```

    === "Rego v0"
        ```rego
        sre_spaces := {spacelift_space.dev.id, spacelift_space.production.id}

        roles[space_id]["space-writer"] {
            input.session.teams[_] == "SRE"
            sre_spaces[space_id]
        }
        ```

---

### Repository-based access

Teams often organize infrastructure by repository, with each team owning specific repos.

#### Before: Access policy

=== "Rego v1"
    ```rego
    package spacelift

    write if {
        some team in input.session.teams
        team == "TeamA"
        input.stack.repository == "team-a-infra"
    }

    write if {
        some team in input.session.teams
        team == "TeamB"
        input.stack.repository == "team-b-infra"
    }
    ```

=== "Rego v0"
    ```rego
    package spacelift

    write {
        input.session.teams[_] == "TeamA"
        input.stack.repository == "team-a-infra"
    }

    write {
        input.session.teams[_] == "TeamB"
        input.stack.repository == "team-b-infra"
    }
    ```

#### After: Team-based spaces

Create one space per team and move their stacks:

```hcl
resource "spacelift_space" "team_a" {
  name            = "Team A"
  parent_space_id = "root"
}

resource "spacelift_space" "team_b" {
  name            = "Team B"
  parent_space_id = "root"
}

# Team A stacks
resource "spacelift_stack" "team_a_stack" {
  name       = "Team A Infrastructure"
  repository = "team-a-infra"
  space_id   = spacelift_space.team_a.id
  # ... other configuration
}

# Team B stacks
resource "spacelift_stack" "team_b_stack" {
  name       = "Team B Infrastructure"
  repository = "team-b-infra"
  space_id   = spacelift_space.team_b.id
  # ... other configuration
}
```

Login policy:

=== "Rego v1"
    ```rego
    package spacelift

    allow if input.session.member

    roles[spacelift_space.team_a.id] contains "space-writer" if {
        some team in input.session.teams
        team == "TeamA"
    }

    roles[spacelift_space.team_b.id] contains "space-writer" if {
        some team in input.session.teams
        team == "TeamB"
    }
    ```

=== "Rego v0"
    ```rego
    package spacelift

    allow { input.session.member }

    roles[spacelift_space.team_a.id]["space-writer"] {
        input.session.teams[_] == "TeamA"
    }

    roles[spacelift_space.team_b.id]["space-writer"] {
        input.session.teams[_] == "TeamB"
    }
    ```

---

## Patterns requiring adaptation

Some access policy patterns don't map directly to Spaces and require alternative approaches.

### Time-based access control

Access policies could enforce time-of-day restrictions per request. Spaces evaluate access at login time only.

#### Before: Access policy

=== "Rego v1"
    ```rego
    package spacelift

    write if {
        some team in input.session.teams
        team == "Developers"
    }

    # Deny writes outside business hours
    deny_write if {
        clock := time.clock([input.request.timestamp_ns, "America/Los_Angeles"])
        clock[0] < 9
    }

    deny_write if {
        clock := time.clock([input.request.timestamp_ns, "America/Los_Angeles"])
        clock[0] > 17
    }

    deny_write if {
        weekend := {"Saturday", "Sunday"}
        weekday := time.weekday(input.request.timestamp_ns)
        weekend[weekday]
    }
    ```

=== "Rego v0"
    ```rego
    package spacelift

    write { input.session.teams[_] == "Developers" }

    # Deny writes outside business hours
    deny_write {
        clock := time.clock([input.request.timestamp_ns, "America/Los_Angeles"])
        clock[0] < 9
    }

    deny_write {
        clock := time.clock([input.request.timestamp_ns, "America/Los_Angeles"])
        clock[0] > 17
    }

    weekend := {"Saturday", "Sunday"}

    deny_write {
        weekday := time.weekday(input.request.timestamp_ns)
        weekend[weekday]
    }
    ```

#### After: Login policy with time checks

!!! warning "Evaluation timing difference"
    Login policies evaluate **when users log in**, not per-request. Users who log in during business hours will maintain access until their session expires, even outside business hours.

=== "Rego v1"
    ```rego
    package spacelift

    allow if input.session.member

    # Only grant write access during business hours
    roles["production-space-id"] contains "space-writer" if {
        some team in input.session.teams
        team == "Developers"

        # Check time
        clock := time.clock([input.request.timestamp_ns, "America/Los_Angeles"])
        clock[0] >= 9
        clock[0] <= 17

        # Check day
        weekend := {"Saturday", "Sunday"}
        weekday := time.weekday(input.request.timestamp_ns)
        not weekend[weekday]
    }

    # Always grant read access
    roles["production-space-id"] contains "space-reader" if {
        some team in input.session.teams
        team == "Developers"
    }
    ```

=== "Rego v0"
    ```rego
    package spacelift

    allow { input.session.member }

    # Only grant write access during business hours
    roles["production-space-id"]["space-writer"] {
        input.session.teams[_] == "Developers"

        # Check time
        clock := time.clock([input.request.timestamp_ns, "America/Los_Angeles"])
        clock[0] >= 9
        clock[0] <= 17

        # Check day
        weekend := {"Saturday", "Sunday"}
        weekday := time.weekday(input.request.timestamp_ns)
        not weekend[weekday]
    }

    # Always grant read access
    roles["production-space-id"]["space-reader"] {
        input.session.teams[_] == "Developers"
    }
    ```

**Mitigation strategies:**

1. **Use approval policies**: Add approval requirements that can evaluate time per-run
2. **Team expectations**: Communicate that time restrictions apply at login, not continuously

---

### IP-based access control

Similar to time-based restrictions, IP checks in access policies were per-request. Login policies check IP at login time only.

#### Before: Access policy

=== "Rego v1"
    ```rego
    package spacelift

    write if {
        some team in input.session.teams
        team == "Contractors"
    }

    # Deny writes from outside office network
    deny_write if {
        not net.cidr_contains("12.34.56.0/24", input.request.remote_ip)
    }
    ```

=== "Rego v0"
    ```rego
    package spacelift

    write { input.session.teams[_] == "Contractors" }

    # Deny writes from outside office network
    deny_write {
        not net.cidr_contains("12.34.56.0/24", input.request.remote_ip)
    }
    ```

#### After: Login policy with IP checks

=== "Rego v1"
    ```rego
    package spacelift

    allow if input.session.member

    # Only grant write if logging in from office
    roles["production-space-id"] contains "space-writer" if {
        some team in input.session.teams
        team == "Contractors"
        net.cidr_contains("12.34.56.0/24", input.session.creator_ip)
    }

    # Always allow read access
    roles["production-space-id"] contains "space-reader" if {
        some team in input.session.teams
        team == "Contractors"
    }
    ```

=== "Rego v0"
    ```rego
    package spacelift

    allow { input.session.member }

    # Only grant write if logging in from office
    roles["production-space-id"]["space-writer"] {
        input.session.teams[_] == "Contractors"
        net.cidr_contains("12.34.56.0/24", input.session.creator_ip)
    }

    # Always allow read access
    roles["production-space-id"]["space-reader"] {
        input.session.teams[_] == "Contractors"
    }
    ```

**Mitigation strategies:**

1. **VPN requirements**: Require VPN for production access at the network level
2. **Shorter sessions**: Reduce session timeout to re-check IP more frequently
3. **API key restrictions**: For programmatic access, use IP-restricted API keys

---

### Fine-grained access within the same repository

Access policies could provide different access levels to stacks from the same repository. With Spaces, stacks in the same space have the same access control.

#### Before: Access policy

=== "Rego v1"
    ```rego
    package spacelift

    # Developers can write to develop branch stacks
    write if {
        some team in input.session.teams
        team == "Developers"
        input.stack.branch == "develop"
        input.stack.repository == "my-infra"
    }

    # Developers can only read main branch stacks
    read if {
        some team in input.session.teams
        team == "Developers"
        input.stack.branch == "main"
        input.stack.repository == "my-infra"
    }
    ```

=== "Rego v0"
    ```rego
    package spacelift

    # Developers can write to develop branch stacks
    write {
        input.session.teams[_] == "Developers"
        input.stack.branch == "develop"
        input.stack.repository == "my-infra"
    }

    # Developers can only read main branch stacks
    read {
        input.session.teams[_] == "Developers"
        input.stack.branch == "main"
        input.stack.repository == "my-infra"
    }
    ```

#### After: Separate spaces per branch/environment

!!! warning "Architectural change required"
    You **cannot** provide different access levels to stacks within the same space. You must separate stacks into different spaces based on their access requirements.

```hcl
# Create spaces by environment/branch
resource "spacelift_space" "dev" {
  name            = "Development"
  parent_space_id = "root"
  inherit_entities = true  # Inherit worker pools, contexts
}

resource "spacelift_space" "prod" {
  name            = "Production"
  parent_space_id = "root"
  inherit_entities = true
}

# Separate stacks by space
resource "spacelift_stack" "app_dev" {
  name       = "App - Dev"
  repository = "my-infra"
  branch     = "develop"
  space_id   = spacelift_space.dev.id
}

resource "spacelift_stack" "app_prod" {
  name       = "App - Prod"
  repository = "my-infra"
  branch     = "main"
  space_id   = spacelift_space.prod.id
}
```

Login policy:

=== "Rego v1"
    ```rego
    package spacelift

    allow if input.session.member

    # Write to dev space
    roles[spacelift_space.dev.id] contains "space-writer" if {
        some team in input.session.teams
        team == "Developers"
    }

    # Read-only to prod space
    roles[spacelift_space.prod.id] contains "space-reader" if {
        some team in input.session.teams
        team == "Developers"
    }
    ```

=== "Rego v0"
    ```rego
    package spacelift

    allow { input.session.member }

    # Write to dev space
    roles[spacelift_space.dev.id]["space-writer"] {
        input.session.teams[_] == "Developers"
    }

    # Read-only to prod space
    roles[spacelift_space.prod.id]["space-reader"] {
        input.session.teams[_] == "Developers"
    }
    ```

**Best practices:**

- Use [space inheritance](../../spaces/access-control.md#inheritance) to share worker pools and contexts
- Align space boundaries with permission boundaries
- Consider using a parent space for shared resources

---

### Complex conditional logic

Access policies could deny access based on runtime stack properties. This is not possible with Spaces.

#### No direct replacement

=== "Rego v1"
    ```rego
    package spacelift

    # Deny write to stacks in certain states
    deny_write if {
        input.stack.state == "FINISHED"
        some team in input.session.teams
        team != "SRE"
    }

    # Deny access to locked stacks (except owner)
    deny if {
        not is_null(input.stack.locked_by)
        input.session.login != input.stack.locked_by
    }
    ```

=== "Rego v0"
    ```rego
    package spacelift

    # Deny write to stacks in certain states
    deny_write {
        input.stack.state == "FINISHED"
        input.session.teams[_] != "SRE"
    }

    # Deny access to locked stacks (except owner)
    deny {
        not is_null(input.stack.locked_by)
        input.session.login != input.stack.locked_by
    }
    ```

#### Alternative: Use approval policies

For runtime checks, move the logic to [approval policies](../approval-policy.md) which evaluate when runs are triggered:

=== "Rego v1"
    ```rego
    package spacelift

    # Require approval from SRE for stacks in FINISHED state
    approve if {
        input.run.stack.state != "FINISHED"
    }

    approve if {
        input.run.stack.state == "FINISHED"
        some approval in input.reviews.current.approvals
        some team in approval.session.teams
        team == "SRE"
    }
    ```

=== "Rego v0"
    ```rego
    package spacelift

    # Require approval from SRE for stacks in FINISHED state
    approve {
        input.run.stack.state != "FINISHED"
    }

    approve {
        input.run.stack.state == "FINISHED"
        input.reviews.current.approvals[_].session.teams[_] == "SRE"
    }
    ```

!!! note "Stack locking is built-in"
    Stack locking is a built-in feature controlled by the `stack:unlock-force` permission. Only users with this permission (or the lock owner) can unlock stacks, so no custom policy is needed.

---

## Step-by-step migration guide

### Step 1: Audit current access policies

First, identify all access policies in your account:

**Using GraphQL API:**

```graphql
query ListAccessPolicies {
  policies(input: {type: ACCESS}) {
    id
    name
    body
    labels
    attachedStacksCount
    attachedModulesCount
  }
}
```

**Using Terraform:**

Search your Terraform code for `spacelift_policy` resources with `type = "ACCESS"`.

**Document each policy:**

- What stacks/modules is it attached to?
- What teams/users does it grant access to?
- What conditions does it check (time, IP, labels, etc.)?
- What access level does it grant (read/write)?

### Step 2: Design your space structure

Plan spaces based on:

- **Team boundaries**: Who needs access to what?
- **Environment separation**: Dev, staging, production
- **Organizational structure**: Business units, projects, products

!!! tip "Space design best practices"
    See [structuring your spaces tree](../../spaces/structuring-your-spaces-tree.md) for detailed guidance.

Example structure:

```text
root
├── infrastructure (platform team)
│   ├── networking
│   ├── security
│   └── shared-services
├── applications
│   ├── team-a
│   │   ├── dev
│   │   └── prod
│   └── team-b
│       ├── dev
│       └── prod
└── sandbox (unrestricted dev/test)
```

### Step 3: Create spaces

Create spaces using Terraform or the web UI:

```hcl
# Platform infrastructure
resource "spacelift_space" "infrastructure" {
  name             = "Infrastructure"
  parent_space_id  = "root"
  inherit_entities = true
}

# Team A spaces
resource "spacelift_space" "team_a" {
  name             = "Team A"
  parent_space_id  = "root"
  inherit_entities = true
}

resource "spacelift_space" "team_a_dev" {
  name             = "Development"
  parent_space_id  = spacelift_space.team_a.id
  inherit_entities = true
}

resource "spacelift_space" "team_a_prod" {
  name             = "Production"
  parent_space_id  = spacelift_space.team_a.id
  inherit_entities = true
}
```

### Step 4: Migrate stacks to spaces

Update each stack to use the appropriate space:

```hcl
resource "spacelift_stack" "example" {
  name     = "Example Stack"
  space_id = spacelift_space.team_a_dev.id  # Add this
  # ... rest of configuration
}
```

!!! warning "Plan before applying"
    Moving stacks between spaces may affect who can see and access them. Test with non-critical stacks first.

### Step 5: Configure access control

Choose your access control method:

#### Option A: Login policies (recommended for complex logic)

Create or update login policies in the `root` space:

=== "Rego v1"
    ```rego
    package spacelift

    # Allow organization members
    allow if input.session.member

    # Map teams to spaces
    roles[spacelift_space.team_a_dev.id] contains "space-writer" if {
        some team in input.session.teams
        team == "TeamA"
    }

    roles[spacelift_space.team_a_prod.id] contains "space-reader" if {
        some team in input.session.teams
        team == "TeamA"
    }

    # Platform team gets admin everywhere
    roles["root"] contains "space-admin" if {
        some team in input.session.teams
        team == "Platform"
    }
    ```

=== "Rego v0"
    ```rego
    package spacelift

    # Allow organization members
    allow { input.session.member }

    # Map teams to spaces
    roles[spacelift_space.team_a_dev.id]["space-writer"] {
        input.session.teams[_] == "TeamA"
    }

    roles[spacelift_space.team_a_prod.id]["space-reader"] {
        input.session.teams[_] == "TeamA"
    }

    # Platform team gets admin everywhere
    roles["root"]["space-admin"] {
        input.session.teams[_] == "Platform"
    }
    ```

#### Option B: User management UI (recommended for simple setups)

1. Go to **Organization Settings** → **Identity Management** → **IdP group mapping**
2. Map each IdP group to roles in specific spaces
3. See [assigning roles to groups](../../authorization/assigning-roles-groups.md) for details

### Step 6: Test access

Before removing access policies:

1. **Test with non-admin users**: Log in as different team members and verify they can access appropriate spaces
2. **Verify read/write permissions**: Ensure users can perform expected actions (trigger runs, modify environment variables)
3. **Check edge cases**: Test any special conditions (time-based, IP-based, etc.)
4. **Review audit logs**: Use [audit trail](../../../integrations/audit-trail.md) to verify access is working correctly

### Step 7: Remove access policies

Once access is verified:

1. **Detach access policies** from stacks/modules
2. **Delete access policies** (keep backups if needed)
3. **Update documentation** to reflect the new access control model

```hcl
# Remove these resources
# resource "spacelift_policy" "old_access_policy" { ... }
# resource "spacelift_policy_attachment" "old_attachment" { ... }
```

---

## Using custom roles for granular permissions

Instead of built-in Space Reader/Writer/Admin roles, create custom roles with specific permissions:

```hcl
# Custom role for deployments only
resource "spacelift_role" "deployer" {
  name        = "Deployer"
  description = "Can trigger and confirm runs, but not modify stacks"
  actions     = [
    "space:read",
    "run:read",
    "run:trigger",
    "run:confirm",
    "run:comment",
  ]
}

# Assign via login policy
roles["production-space-id"][spacelift_role.deployer.id] {
    input.session.teams[_] == "Deployment"
}
```

See [custom roles](../../authorization/rbac-system.md#custom-roles) for more details.

---

## Module access migration

Module access policies work the same way as stack access policies:

```hcl
# Create module-specific space
resource "spacelift_space" "modules" {
  name             = "Terraform Modules"
  parent_space_id  = "root"
  inherit_entities = false  # Modules don't need inheritance
}

# Move modules to the space
resource "spacelift_module" "example" {
  name     = "example-module"
  space_id = spacelift_space.modules.id
  # ... rest of configuration
}

# Share modules with other spaces using space:share-module
resource "spacelift_role" "module_consumer" {
  name    = "Module Consumer"
  actions = [
    "space:read",
    "space:share-module",  # Can use modules from other spaces
  ]
}
```

---

## Troubleshooting

### Users can't see spaces after login

**Problem**: Users log in successfully but see "No spaces available"

**Solution**:

1. Check login policy grants appropriate roles
2. Verify users belong to expected IdP teams/groups
3. Have users log out and back in (roles evaluated at login time)
4. Check space assignments in **Organization Settings** → **Users**

### Users lost access after migration

**Problem**: Users who had access via access policies can no longer access stacks

**Solution**:

1. Verify stacks moved to correct spaces
2. Check login policy or user management assigns roles to those spaces
3. Confirm user's IdP team membership hasn't changed
4. Review audit trail to see what roles user has

### Time/IP restrictions not working as expected

**Problem**: Users can perform actions outside business hours or from wrong locations

**Explanation**: Login policies evaluate at login time, not per-request

**Solution**:

1. Reduce session timeout to force more frequent re-authentication
2. Add approval policies for additional runtime checks
3. Use network-level controls (VPN, firewalls) for IP restrictions
4. Set clear team expectations about when policies are evaluated

### Different access needed for stacks in same space

**Problem**: Need write access to some stacks but read-only to others in the same space

**Solution**: You cannot do this with Spaces. Split stacks into different spaces based on access requirements, or use custom roles with approval policies that check stack properties.

### Migration breaking Terraform state

**Problem**: Moving stacks between spaces causes Terraform drift

**Solution**:

1. Import new space assignments: `terraform import spacelift_stack.example stack-id`
2. Plan carefully before applying to see what will change
3. Consider migrating in phases (non-critical stacks first)

---

## Migration checklist

Use this checklist to track your migration progress:

- **Audit phase**
    - List all access policies
    - Document access patterns for each policy
    - Identify policies that need adaptation
- **Design phase**
    - Design space structure
    - Map stacks to spaces
    - Plan login policy or user management approach
- **Implementation phase**
    - Create spaces in Terraform/UI
    - Move stacks to appropriate spaces
    - Configure login policies or IdP mappings
    - Create custom roles if needed
- **Testing phase**
    - Test with multiple user accounts
    - Verify read/write permissions
    - Test edge cases (time, IP, etc.)
    - Review audit logs
- **Cleanup phase**
    - Detach access policies
    - Delete access policies
    - Update team documentation
    - Communicate changes to users

---

## Related resources

- **[Spaces overview](../../spaces/README.md)**: Understanding Spacelift spaces
- **[Space access control](../../spaces/access-control.md)**: How RBAC works with spaces
- **[Login policies](../login-policy.md)**: Programmatic access control
- **[User management](../../user-management/README.md)**: GUI-based permission management
- **[RBAC system](../../authorization/rbac-system.md)**: Understanding roles and permissions
- **[Custom roles](../../authorization/rbac-system.md#custom-roles)**: Creating fine-grained permissions
- **[Structuring spaces](../../spaces/structuring-your-spaces-tree.md)**: Best practices for space design
- **[Stack access policy reference](../stack-access-policy.md)**: Original access policy documentation
