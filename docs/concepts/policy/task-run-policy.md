# Task policy

!!! warning
    This feature is deprecated. New users should not use this feature and existing users are encouraged to migrate to the [approval policy](approval-policy.md), which offers a much more flexible and powerful way to control which tasks are allowed to proceed. A migration guide is available [here](#migration-guide).

## Purpose

Spacelift tasks are a handy feature that allows an arbitrary command to be executed within the context of your fully initialized stack. This feature is designed to make running one-off administrative tasks (eg. [resource tainting](https://www.terraform.io/docs/commands/taint.html){: rel="nofollow"}) safer and more convenient. It can also be an attack vector allowing evil people to do bad things, or simply a footgun allowing well-meaning people to err in a spectacular way.

Enter task policies. The sole purpose of task policies is to prevent certain commands from being executed, to prevent certain groups or individuals from executing any commands, or to prevent certain commands from being executed by certain groups or individuals.

!!! info
    Preventing **admins** from running tasks using policies can only play an advisory role and should not be considered a safety measure. A bad actor with admin privileges can detach a policy from the stack and run whatever they want. Choose your admins wisely.

Task policies are simple in that they only use a single rule - **deny** - with a string message. A single match for that rule will prevent a run from being created, with an appropriate API error. Let's see how that works in practice by defining a simple rule and attaching it to a stack:

```opa
package spacelift

deny["not in my town, you don't"] { true }
```

And here's the outcome when trying to run a task:

![](../../assets/screenshots/Tasks_·_Stack_managed_by_Spacelift.png)

## Data input

This is the schema of the data input that each policy request will receive:

!!! tip "Official Schema Reference"
    For the most up-to-date and complete schema definition, please refer to the [official Spacelift policy contract schema](https://app.spacelift.tf/.well-known/policy-contract.json){: rel="nofollow"} under the `TASK` policy type.

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
|-----------|-----------------|
| `request` | `input.request` |
| `session` | `input.session` |
| `stack`   | `input.stack`   |

## Examples

Let's have a look at a few examples to see what you can accomplish with task policies. You've seen one example already - disabling tasks entirely. That's perhaps both heavy-handed and naive given that admins can detach the policy if needed. So let's only block non-admins from running tasks:

```opa
package spacelift

deny["only admins can run tasks"] { not input.session.admin }
```

Let's look at an example of this simple policy in [the Rego playground](https://play.openpolicyagent.org/p/wKLPjJ4dEF){: rel="nofollow"}.

That's still pretty harsh. We could possibly allow writers to run some commands we consider safe - like resource [tainting and untainting](https://www.terraform.io/docs/commands/taint.html){: rel="nofollow"}. Let's try then, and please excuse the regex:

```opa
package spacelift

deny[sprintf("command not allowed (%s)", [command])] {
  command := input.request.command

  not input.session.admin
  not regex.match("^terraform\\s(un)?taint\\s[\\w\\-\\.]*$", command)
}
```

Feel free to play with the above example in [the Rego playground](https://play.openpolicyagent.org/p/MPoP9yQpEp){: rel="nofollow"}.

If you want to keep whitelisting different commands, it may be more elegant to flip the rule logic, create a series of _allowed_ rules, and define one _deny_ rule as `not allowed`. Let's have a look at this approach, and while we're at it let's remind everyone not to run anything during the weekend:

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

As usual, this example is [available to play around with](https://play.openpolicyagent.org/p/FP7xz7oWGp){: rel="nofollow"}.

## Migration guide

A task policy can be expressed as an [approval policy](./approval-policy.md) if it defines a single `reject` rule, and an `approve` rule that is its negation. Below you will find equivalents of the examples above expressed as [approval policies](./approval-policy.md).

### Migration example: only allow OpenTofu/Terraform taint and untaint

```opa
package spacelift

reject {
  command := input.run.command
  not regex.match("^terraform\\s(un)?taint\\s[\\w\\-\\.]*$", command)
}

approve { not reject }
```

### Migration example: no tasks on weekends

```opa
package spacelift

reject {
  today   := time.weekday(input.run.created_at)
  weekend := { "Saturday", "Sunday" }

  weekend[today]
}

approve { not reject }
```
