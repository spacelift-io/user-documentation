# Access policy

!!! warning
    Access policies are deprecated. Use [space access control](../spaces/access-control.md) instead.

By default, non-admin Spacelift users have no access to any [stacks](../stack/README.md) or [modules](../../vendors/terraform/module-registry.md) and must be granted explicit permissions. There are two levels of non-admin access, [reader](#readers) and [writer](#writers). For now all we need to care about is that access policies are what we use to give appropriate level of access to individual stacks to non-admin users in your account.

This type of access control is typically done either by building a separate user management system on your end or piggy-backing on one created by your identity provider. Both solutions have their limitations:

- **Separate user management system**: Makes it more difficult for organizations to onboard and offboard users, and can be difficult to get right, especially if you require granular and sophisticated access controls.
- **Identity provider**: A safer bet used by many DevTools vendors. With this approach, having some access level to a GitHub repo would give you the same access level to all Spacelift stacks and/or modules associated with it, which can be inflexible if you want separate access controls for two stacks linked to one repo (such as staging and production).

Access policies give you a tool to build your own access management system using data obtained either from our identity provider (GitHub), or from your identity provider if using the [Single Sign-On integration](../../integrations/single-sign-on/README.md).

## Rules

Your access policy can define the following boolean rules:

- **write**: Grants the current user [write access](#writers) to the stack or module.
- **read**: Grants the current user [read access](#readers) to the stack or module.
- **deny**: Denies the current user **all** access to the stack or module, no matter the outcome of other rules.
- **deny_write**: Denies the current user **write** access to the stack or module, no matter the outcome of other rules.

Write access automatically assumes **read** permissions, so there's no need to define separate **read** policies for writers.

Access policies are executed quickly. Internally, we expect that running all access policies on all the stacks in one request (`stacks` in the [GraphQL API](../../integrations/api.md)) will take less than 500 milliseconds, otherwise the request fails. While that is usually enough time for modern computers, fancy regex rules in your access policies could cause issues in some cases.

## Access levels

There are two levels of non-admin access to a [Spacelift stack](../stack/README.md) or module: reader and writer. These are pretty intuitive for most developers, but this section will cover them in more detail to avoid any possible confusion.

In every non-trivial organization there will be different roles: people who build and manage shared infrastructure, people who build and manage their team or project-level infrastructure, and people who use this infrastructure to build great things.

### Admins

The people who manage your Spacelift accounts. They need to be able to set up:

- [Stacks](../stack/README.md).
- [Contexts](../configuration/context.md).
- [Policies](./README.md).

Use [login policies](login-policy.md) to manage admin access.

### Writers

The people who manage their team or project-level infrastructure. This group should be able to:

- Define the [environment](../configuration/environment.md).
- Set up various integrations like [source control](../../integrations/source-control/README.md), [cloud providers](../../integrations/cloud-providers/README.md), or [SSO](../../integrations/single-sign-on/README.md).
- Trigger and confirm [runs](../run/README.md).
- Execute [tasks](../run/task.md).

**Writers** should still operate within the boundaries defined by **admins**, who do that mainly by attaching [contexts](../configuration/context.md) and [policies](./README.md) to the [stacks](../stack/README.md).

### Readers

The people who build on top of existing infrastructure. They don't need to define the infra, but they need to understand what's available and when things are changing. You'll probably want to allow them to contribute to infra definitions, too, and allow them to see feedback from proposed runs.

Readers can't _do_ anything, but they can _see_ everything. Most modern organizations tend to provide this level of access to as many stakeholders as possible to maintain transparency and facilitate collaboration.

## Data input schema

Each policy request will receive this data input.

!!! tip "Official Schema Reference"
    For the most up-to-date and complete schema definition, please refer to the [official Spacelift policy contract schema](https://app.spacelift.io/.well-known/policy-contract.json){: rel="nofollow"} under the `ACCESS` policy type.

```json
{
  "request": {
    "remote_ip": "string - IP of the user making a request",
    "timestamp_ns": "number - current Unix timestamp in nanoseconds"
  },
  "session": {
    "admin": "boolean - is the current user a Spacelift admin",
    "creator_ip": "string - IP address of the user who created the session",
    "login": "string - GitHub username of the logged in user",
    "name":  "string - full name of the logged in GitHub user - may be empty",
    "teams": ["string - names of org teams the user is a member of"],
    "machine": "boolean - whether the creator is a machine or a user"
  },
  "stack": { // when access to a stack is being evaluated
    "id": "string - unique ID of the stack",
    "administrative": "boolean - is the stack administrative",
    "autodeploy": "boolean - is the stack currently set to autodeploy",
    "branch": "string - tracked branch of the stack",
    "labels": ["string - list of arbitrary, user-defined selectors"],
    "locked_by": "optional string - if the stack is locked, this is the name of the user who did it",
    "name": "string - name of the stack",
    "namespace": "string - repository namespace, only relevant to GitLab repositories",
    "project_root": "optional string - project root as set on the Stack, if any",
    "repository": "string - name of the source repository",
    "state": "string - current state of the stack",
    "terraform_version": "string or null - last Terraform version used to apply changes"
  },
  "module": { // when access to a module is being evaluated
    "id": "string - unique ID of the module",
    "administrative": "boolean - is the stack administrative",
    "branch": "string - tracked branch of the module",
    "labels": ["string - list of arbitrary, user-defined selectors"],
    "namespace": "string - repository namespace, only relevant to GitLab repositories",
    "repository": "string - name of the source repository",
    "terraform_provider": "string - name of the main Terraform provider used by the module"
  }
}
```

## Examples

!!! tip
    We maintain a [library of example policies](https://github.com/spacelift-io/spacelift-policies-example-library/tree/main/examples/access){: rel="nofollow"} that are ready to use or alter to meet your specific needs.

    If you cannot find what you are looking for below or in the library, please reach out to [our support](../../product/support/README.md#contact-support) and we will craft a policy to do exactly what you need.

This section will cover some common examples that can be copied more or less directly, and some contrived ones to serve as inspiration.

Access policies must be attached to a stack or a module to take effect.

### Read access to engineers

In this policy, every member of the engineering team gets **read** access:

```opa
package spacelift

read if {
  some team in input.session.teams
  team == "Engineering"
}
```

### Write only in-office during business hours

In this policy, **write** access is only provided to users that are in the office (using the office's IP address range) during business hours (9 to 5, weekdays). Write access is restricted in other cases. This policy is best combined with one that gives **read** access.

```opa
package spacelift

now := input.request.timestamp_ns
clock := time.clock([now, "America/Los_Angeles"])
weekend := {"Saturday", "Sunday"}
weekday := time.weekday(now)
ip := input.request.remote_ip

write if {
  some team in input.session.teams
  team == "Product team"
}

deny_write if weekend[weekday]
deny_write if clock[0] < 9
deny_write if clock[0] > 17
deny_write if not net.cidr_contains("12.34.56.0/24", ip)
```

### Protect administrative stacks

!!! warning
    The administrative flag is now deprecated and [will be gone on the 1st of June, 2026](../authorization/assigning-roles-stacks.md#migration-from-administrative-flag). **The flag will always return false from that date onwards**.

[Administrative](../stack/README.md) stacks are powerful. Having **write** access to one is almost as good as being an **admin**, as you can define and attach [contexts](../configuration/context.md) and [policies](./README.md). In this policy, we deny **write** access to administrative stacks entirely. This works since access policies are not evaluated for **admin** users.

```opa
package spacelift

deny_write if input.stack.administrative
```
