# Task policy

!!! warning

    Task run policies are deprecated. Use [approval policies](../approval-policy.md) instead for a more flexible, powerful way to control which tasks are allowed to proceed.

    Existing users with task run policies should migrate as soon as possible using our [migration guide](#migration-guide).

Spacelift tasks allow an arbitrary command to be executed within the context of your fully initialized stack. This feature is designed to make running one-off administrative tasks (e.g. [resource tainting](https://www.terraform.io/docs/commands/taint.html){: rel="nofollow"}) safer and more convenient. However, it can also be an attack vector for bad actors.

Task run policies prevent:

- Certain commands from being executed.
- Certain groups or individuals from executing any commands.
- Certain commands from being executed by certain groups or individuals.

!!! info
    Preventing **admins** from running tasks using policies can only play an advisory role and should not be considered a safety measure. A bad actor with admin privileges can detach a policy from the stack and run whatever they want. Choose your admins wisely.

Task policies only use a single rule, **deny**, with a string message. A single match for that rule will prevent a run from being created, with an appropriate API error. Let's define a simple rule and attach it to a stack:

=== "Rego v1"
    ```opa
    package spacelift

    deny contains "not in my town, you don't" if true
    ```

=== "Rego v0"
    ```opa
    package spacelift

    deny["not in my town, you don't"] { true }
    ```

Here's the outcome when trying to run a task:

![Task run policy deny outcome](../../../assets/screenshots/Tasks_·_Stack_managed_by_Spacelift.png)

## Data input schema

Each policy request will receive this data input.

!!! tip "Official Schema Reference"
    For the most up-to-date and complete schema definition, please refer to the [official Spacelift policy contract schema](https://app.spacelift.io/.well-known/policy-contract.json){: rel="nofollow"} under the `TASK` policy type.

```json
{
  "request": {
    "command": "string - command that the user is trying to execute as task",
    "remote_ip": "string - IP of the user trying to log in",
    "timestamp_ns": "number - current Unix timestamp in nanoseconds"
  },
  "session": {
    "admin": "boolean - is the current user a Spacelift admin",
    "creator_ip": "string - IP address of the user who created the session",
    "login": "string - GitHub username of the current user",
    "name": "string - full name of the current user",
    "teams": ["string - names of org teams the current user is a member of"],
    "machine": "boolean - whether the creator is a machine or a user"
  },
  "stack": {
    "administrative": "boolean - is the stack administrative",
    "roles": [{
      "id": "string - the role slug, eg. space-admin",
      "name": "string - the role name"
    }],
    "autodeploy": "boolean - is the stack currently set to autodeploy",
    "branch": "string - tracked branch of the stack",
    "labels": ["string - list of arbitrary, user-defined selectors"],
    "locked_by": "optional string - if the stack is locked, this is the name of the user who did it",
    "name": "string - name of the stack",
    "namespace": "string - repository namespace, only relevant to GitLab repositories",
    "project_root": "optional string - project root as set on the Stack, if any",
    "repository": "string - name of the source GitHub repository",
    "state": "string - current state of the stack",
    "terraform_version": "string or null - last Terraform version used to apply changes"
  }
}
```

### Aliases

In addition to our [helper functions](./README.md#helper-functions), we provide aliases for commonly used parts of the input data:

| Alias     | Source          |
| --------- | --------------- |
| `request` | `input.request` |
| `session` | `input.session` |
| `stack`   | `input.stack`   |

## Examples

This example blocks non-admins from running tasks:

=== "Rego v1"
    ```opa
    package spacelift

    deny contains "only admins can run tasks" if not input.session.admin
    ```

=== "Rego v0"
    ```opa
    package spacelift

    deny["only admins can run tasks"] { not input.session.admin }
    ```

However, we could allow writers to run some commands we consider safe, like resource [tainting and untainting](https://www.terraform.io/docs/commands/taint.html){: rel="nofollow"}:

=== "Rego v1"
    ```opa
    package spacelift

    deny contains sprintf("command not allowed (%s)", [command]) if {
      command := input.request.command

      not input.session.admin
      not regex.match("^terraform\\s(un)?taint\\s[\\w\\-\\.]*$", command)
    }
    ```

=== "Rego v0"
    ```opa
    package spacelift

    deny[sprintf("command not allowed (%s)", [command])] {
      command := input.request.command

      not input.session.admin
      not regex.match("^terraform\\s(un)?taint\\s[\\w\\-\\.]*$", command)
    }
    ```

If you want to keep allowlisting different commands, it may be more elegant to flip the rule logic by creating a series of _allowed_ rules and one _deny_ rule as `not allowed`. This example uses that approach to remind users not to run anything during the weekend:

=== "Rego v1"
    ```opa
    package spacelift

    command := input.request.command

    deny contains sprintf("command not allowed (%s)", [command]) if not allowed

    deny contains "no tasks on weekends" if {
      today := time.weekday(input.request.timestamp_ns)
      weekend := {"Saturday", "Sunday"}

      weekend[today]
    }

    allowed if input.session.admin
    allowed if regex.match("^terraform\\s(un)?taint\\s[\\w\\-\\.]*$", command)
    allowed if regex.match("^terraform\\simport\\s[\\w\\-\\.]*$", command)
    ```

=== "Rego v0"
    ```opa
    package spacelift

    command := input.request.command

    deny[sprintf("command not allowed (%s)", [command])] { not allowed }

    deny["no tasks on weekends"] {
      today   := time.weekday(input.request.timestamp_ns)
      weekend := { "Saturday", "Sunday" }

      weekend[today]
    }

    allowed { input.session.admin }
    allowed { regex.match("^terraform\\s(un)?taint\\s[\\w\\-\\.]*$", command) }
    allowed { regex.match("^terraform\\simport\\s[\\w\\-\\.]*$", command) }
    ```

## Migration guide

A task policy can be expressed as an [approval policy](../approval-policy.md) if it defines a single `reject` rule, and an `approve` rule that is its negation. Spacelift has, more or less, deprecated task policies in favor of approval policies.

Here are the [task policy examples](#examples) rewritten as approval policies.

### Only allow OpenTofu/Terraform taint and untaint

=== "Rego v1"
    ```opa
    package spacelift

    reject if {
      command := input.run.command
      not regex.match("^terraform\\s(un)?taint\\s[\\w\\-\\.]*$", command)
    }

    approve if not reject
    ```

=== "Rego v0"
    ```opa
    package spacelift

    reject {
      command := input.run.command
      not regex.match("^terraform\\s(un)?taint\\s[\\w\\-\\.]*$", command)
    }

    approve { not reject }
    ```

### No tasks on weekends

=== "Rego v1"
    ```opa
    package spacelift

    reject if {
      today := time.weekday(input.run.created_at)
      weekend := {"Saturday", "Sunday"}

      weekend[today]
    }

    approve if not reject
    ```

=== "Rego v0"
    ```opa
    package spacelift

    reject {
      today   := time.weekday(input.run.created_at)
      weekend := { "Saturday", "Sunday" }

      weekend[today]
    }

    approve { not reject }
    ```
