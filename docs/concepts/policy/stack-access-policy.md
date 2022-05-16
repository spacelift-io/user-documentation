# Access policy

## Purpose

By default, non-admin users have no access to any [Stacks](../stack/) or [Modules](../../vendors/terraform/module-registry.md) and must be granted that explicitly. There are two levels of non-admin access - reader and writer, and the exact meaning of these roles is covered in a [separate section](stack-access-policy.md#readers-and-writers). For now all we need to care about is that access policies are what we use to give appropriate level of access to individual stacks to non-admin users in your account.

This type of access control is typically done either by building a separate user management system on your end or piggy-backing on one created by your identity provider. Both solutions have their limitations - a separate user management system makes it more difficult for organizations to onboard and offboard users, and the last thing we want is for a guy that was just fired to log in to Spacelift and have their revenge. User management systems are also pretty difficult to get right, too, especially if granular and sophisticated access controls are required.

Piggy-backing on the identity provider is probably a safer bet and is used by many DevTools vendors. With this approach, having some access level to a GitHub repo would give you the same access level to all Spacelift stacks and/or modules associated with it. That's somewhat reasonable, but not as flexible as having your own fancy user management system. Imagine having two stacks linked to one repo, representing two environments - staging and production. It's quite possible that you'd appreciate separate access controls for these two.

Access policies offer the best of both worlds - they give you a tool to build your own access management system using data obtained either from our identity provider (GitHub), or from your identity provider if using [single sign-on integration](../../integrations/single-sign-on.md). In subsequent sections we'll dive deeper into [what data is exposed to your policies](stack-access-policy.md#data-input), how you can [define access policies](stack-access-policy.md#cookbook) with different levels of access, and [what those levels actually mean](stack-access-policy.md#readers-and-writers).

## Rules

Your access policy can define the following boolean rules:

* **write**: gives the current user [write access](stack-access-policy.md#readers-and-writers) to the stack or module;
* **read**: gives the current user [read access](stack-access-policy.md#readers-and-writers) to the stack or module;
* **deny**: denies the current user **all** access to the stack or module, no matter the outcome of other rules;
* **deny\_write**:  denies the current user **write** access to the stack or module, no matter the outcome of other rules;

Note that write access automatically assumes read permissions, too, so there's no need to define separate **read** policies for writers.

Another thing to keep in mind when defining access policies is that they are executed quickly. Internally, we expect that running all access policies on all the stacks in one request (`stacks` in the [GraphQL API](../../integrations/api.md)) will take less than 500 milliseconds - otherwise the request fails. That's actually plenty for modern computers, but think twice before creating fancy regex rules in your access policies.

## Readers and writers

There are two levels of non-admin access to a [Spacelift stack](../stack/) or module - reader and writer. These are pretty intuitive for most developers, but this section will cover them in more detail to avoid any possible confusion. But first, let's try to understand the use case for different levels of access.

In every non-trivial organization there will be different roles - folks who build and manage shared infrastructure, folks who build and manage their team or project-level infrastructure, and folks who use this infrastructure to build great things. The first group is probably the people who manage your Spacelift accounts - the **admins**. They need to be able to set up everything - create [stacks](../stack/), [contexts](../configuration/context.md) and [policies](./), and attach them accordingly. You'd normally use [login policies](login-policy.md) to manage their access.

The second group - folks who manage their team or project-level infrastructure - should have a reasonable level of access to their project. They should be able to define the [environment](../configuration/environment.md), set up various integrations, trigger and confirm [runs](../run/), execute [tasks](../run/task.md). This level of access is granted by the **writer** permission. However, **writers** should still operate within the boundaries defined by **admins**, who do that mainly by attaching [contexts](../configuration/context.md) and [policies](./) to the [stacks](../stack/).

Last but not least the third group - folks who build things on top of existing infra - don't necessarily need to define the infra, but they need to understand what's available and when things are changing. You'll probably want to allow them to contribute to infra definitions, too, and allow them to see feedback from proposed runs. They can't _do_ anything, but they can _see_ everything. These are the **readers**. Most modern organizations tend to provide this level of access to as many stakeholders as possible to maintain transparency and facilitate collaboration.

## Data input

This is the schema of the data input that each policy request will receive:

```json
{
  "request": {
    "remote_ip": "string - IP of the user making a request",
    "timestamp_ns": "number - current Unix timestamp in nanoseconds"
  },
  "session": {
    "login": "string - GitHub username of the logged in user",
    "name":  "string - full name of the logged in GitHub user - may be empty",
    "teams": ["string - names of org teams the user is a member of"]
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

## Cookbook

With all the above theory in mind, let's jump straight to the code and define some access policies. This section will cover some common examples that can be copied more or less directly, and some contrived ones to serve as an inspiration.

!!! info
    Remember that access policies must be attached to a stack or a module to take effect.

### Read access to everyone (in Engineering)

I get read access, you get read access, everyone gets read access. As long as they're members of the Engineering team:

```opa
package spacelift

read { input.session.teams[_] == "Engineering" }
```

OK, that was simple. But let's also see it in the [Rego playground](https://play.openpolicyagent.org/p/JfvU6EmuMB).

### In case things go wrong, we want you to be there

You know when things go wrong it's usually because someone did something. Like an infra deployment. Let's try to make sure they're in the office when doing so and restrict write access to business hours and office IP range. This policy is best combined with one that gives read access.

```opa
package spacelift

now     := input.request.timestamp_ns
clock   := time.clock([now, "America/Los_Angeles"])
weekend := { "Saturday", "Sunday" }
weekday := time.weekday(now)
ip      := input.request.remote_ip

write      { input.session.teams[_] == "Product team" }
deny_write { weekend[weekday] }
deny_write { clock[0] < 9 }
deny_write { clock[0] > 17 }
deny_write { not net.cidr_contains("12.34.56.0/24", ip) }
```

Here is this example in [Rego playground](https://play.openpolicyagent.org/p/IDqCBBtZ0n).

### Protect administrative stacks

[Administrative](../stack/#administrative) stacks are powerful - getting **write** access to one is almost as good as being an **admin** - you can define and attach [contexts](../configuration/context.md) and [policies](./). So let's deny **write** access to them entirely. This works since access policies are not evaluated for **admin** users.

```opa
package spacelift

deny_write { input.stack.administrative }
```

And here's the necessary [Rego playground example](https://play.openpolicyagent.org/p/JG0MwLyyeQ).
