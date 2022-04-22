# Task policy

!!! Warning
This feature is deprecated. Using an [Approval policy](approval-policy.md) allows you to achieve the same goals in a more flexible and powerful way.


## Purpose

Spacelift tasks are a handy feature that allows an arbitrary command to be executed within the context of your fully initialized stack. This feature is designed to make running one-off administrative tasks (eg. [resource tainting](https://www.terraform.io/docs/commands/taint.html)) safer and more convenient. It can also be an attack vector allowing evil people to do bad things, or simply a footgun allowing well-meaning people to err in a spectacular way.

Enter task policies. The sole purpose of task policies is to prevent certain commands from being executed, to prevent certain groups or individuals from executing any commands, or to prevent certain commands from being executed by certain groups or individuals.

!!! Info
Preventing **admins** from running tasks using policies can only play an advisory role and should not be considered a safety measure. A bad actor with admin privileges can detach a policy from the stack and run whatever they want. Choose your admins wisely.


Task policies are simple in that they only use a single rule - **deny** - with a string message. A single match for that rule will prevent a run from being created, with an appropriate API error. Let's see how that works in practice by defining a simple rule and attaching it to a stack:

```perl
package spacelift

deny["not in my town, you don't"] { true }
```

And here's the outcome when trying to run a task:

![](/assets/images/Tasks_%C2%B7_Stack_managed_by_Spacelift.png)

## Data input

This is the schema of the data input that each policy request will receive:

```javascript
{
  "request": {
    "command": "string - command that the user is trying to execute as task",
    "remote_ip": "string - IP of the user trying to log in",
    "timestamp_ns": "number - current Unix timestamp in nanoseconds"
  },
  "session": {
    "admin": "boolean - is the current user a Spacelift admin",
    "login": "string - GitHub username of the current user",
    "name": "string - full name of the current user",
    "teams": ["string - names of org teams the current user is a member of"]
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

### Helpers

In addition to our [global helper functions](./#helper-functions), we also provide the following helpers for task policies:

* `request` - an alias for `input.request`.
* `session` - an alias for `input.session`.
* `stack` - an alias for `input.stack`.

## Examples

Let's have a look at a few examples to see what you can accomplish with task policies. You've seen one example already - disabling tasks entirely. That's perhaps both heavy-handed and naive given that admins can detach the policy if needed. So let's only block non-admins from running tasks:

```perl
package spacelift

deny["only admins can run tasks"] { not input.session.admin }
```

Let's look at an example of this simple policy in [the Rego playground](https://play.openpolicyagent.org/p/wKLPjJ4dEF).

That's still pretty harsh. We could possibly allow writers to run some commands we consider safe - like resource [tainting and untainting](https://www.terraform.io/docs/commands/taint.html). Let's try then, and please excuse the regex:

```perl
package spacelift

deny[sprintf("command not allowed (%s)", [command])] {
  command := input.request.command

  not input.session.admin
  not re_match("^terraform\\s(un)?taint\\s[\\w\\-\\.]*$", command)
}
```

Feel free to play with the above example in [the Rego playground](https://play.openpolicyagent.org/p/MPoP9yQpEp).

If you want to keep whitelisting different commands, it may be more elegant to flip the rule logic, create a series of _allowed_ rules, and define one _deny_ rule as `not allowed`. Let's have a look at this approach, and while we're at it let's remind everyone not to run anything during the weekend:

```perl
package spacelift

command := input.request.command

deny[sprintf("command not allowed (%s)", [command])] { not allowed }

deny["no tasks on weekends"] {
  today   := time.weekday(input.request.timestamp_ns)
  weekend := { "Saturday", "Sunday" }

  weekend[today]
}

allowed { input.session.admin }
allowed { re_match("^terraform\\s(un)?taint\\s[\\w\\-\\.]*$", command) }
allowed { re_match("^terraform\\simport\\s[\\w\\-\\.]*$", command) }
```

As usual, this example is [available to play around with](https://play.openpolicyagent.org/p/FP7xz7oWGp).
