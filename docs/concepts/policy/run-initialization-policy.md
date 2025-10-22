# Initialization policy

!!! warning
    Initialization policies are deprecated. Use [approval policies](./approval-policy.md) instead for a more flexible, powerful way to control which runs are allowed to proceed.

    Existing users with initialization policies should migrate as soon as possible using our [migration guide](#migration-guide).

Initialization policies can prevent a [run](../run/README.md) or a [task](../run/task.md) from being [initialized](../run/README.md#initializing), blocking any custom code or commands from being executed.

They look like [plan policies](terraform-plan-policy.md) in that they affect existing runs and print feedback to logs, but they don't get access to the plan. Instead, initialization policices can be used to [protect your stack from unwanted changes](#protect-your-stack-from-unwanted-changes) or [enforce organizational rules](#enforce-organizational-rules) concerning how and when runs are supposed to be triggered.

!!! warning
    Server-side initialization policies are being deprecated. We will be replacing them with [worker-side policies](../worker-pools#configuration-options) that can be set by using the launcher run initialization policy flag (`SPACELIFT_LAUNCHER_RUN_INITIALIZATION_POLICY`).

    For a limited time period we will be running both types of initialization policy checks but ultimately we're planning to move the pre-flight checks to the worker node, thus allowing customers to block suspicious looking jobs on their end.

Let's create a simple initialization policy, attach it to a stack, and see what it does:

```opa
package spacelift

deny["you shall not pass"] {
  true
}
```

This policy results in:

![Denied by policy message](<../../assets/screenshots/Initial_commit_·_Stack_managed_by_Spacelift (1).png>)

## Rules

Initialization policies only use a **deny** rule with a string message. A single result for that rule will fail the run before it has a chance to start, as shown above.

## Data input schema

Each policy request will receive this data input:

```json
{
  "commit": {
    "author": "string - GitHub login if available, name otherwise",
    "branch": "string - branch to which the commit was pushed",
    "created_at": "number  - creation Unix timestamp in nanoseconds",
    "message": "string - commit message"
  },
  "request": {
    "timestamp_ns": "number - current Unix timestamp in nanoseconds"
  },
  "run": {
    "based_on_local_workspace": "boolean - whether the run stems from a local preview",
    "changes": [
      {
        "action": "string enum - added | changed | deleted",
        "entity": {
          "address": "string - full address of the entity",
          "name": "string - name of the entity",
          "type": "string - full resource type or \"output\" for outputs",
          "entity_vendor": "string - the name of the vendor",
          "entity_type": "string - the type of entity, possible values depend on the vendor",
          "data": "object - detailed information about the entity, shape depends on the vendor and type"
        },
        "phase": "string enum - plan | apply"
      }
    ],
    "commit": {
      "author": "string - GitHub login if available, name otherwise",
      "branch": "string - branch to which the commit was pushed",
      "created_at": "number  - creation Unix timestamp in nanoseconds",
      "hash": "string - the commit hash",
      "message": "string - commit message"
    },
    "created_at": "number - creation Unix timestamp in nanoseconds",
    "flags" : ["string - list of flags set on the run by other policies" ],
    "id": "string - the run ID",
    "runtime_config": {
      "before_init": ["string - command to run before run initialization"],
      "project_root": "string - root of the Terraform project",
      "runner_image": "string - Docker image used to execute the run",
      "terraform_version": "string - Terraform version used to for the run"
    },
    "state": "string - the current run state",
    "triggered_by": "string or null - user or trigger policy who triggered the run, if applicable",
    "type": "string - PROPOSED or TRACKED",
    "updated_at": "number - last update Unix timestamp in nanoseconds",
    "user_provided_metadata": [
      "string - blobs of metadata provided using spacectl or the API when interacting with this run"
    ]
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

| Alias            | Source                     |
| ---------------- | -------------------------- |
| `commit`         | `input.commit`             |
| `run`            | `input.run`                |
| `runtime_config` | `input.run.runtime_config` |
| `stack`          | `input.stack`              |

## Use cases

There are two main use cases for run initialization policies:

- [Protecting your stack from unwanted changes](#protect-your-stack-from-unwanted-changes).
- [Enforcing organizational rules](#enforce-organizational-rules).

### Protect your stack from unwanted changes

Although Spacelift is specialized, you can run custom code before the Terraform initialization phase using [`before_init`](../configuration/runtime-configuration/README.md#before_-and-after_-hooks) scripts. This is a very powerful feature that must be handled responsibly. Since those scripts get full access to your Terraform environment, someone could, in theory, create a commit on a feature branch that would run [`terraform destroy -auto-approve`](https://www.terraform.io/docs/commands/destroy.html){: rel="nofollow"}.

Initialization policies can help you avoid unwanted runs. That's where initialization policies can help. This example policy explicitly blocklists all Terraform commands if they're running as [`before_init`](../configuration/runtime-configuration/README.md#before_-and-after_-hooks) scripts and adds a single exception for a formatting check:

```opa
package spacelift

deny[sprintf("don't use Terraform please (%s)", [command])] {
  command := input.run.runtime_config.before_init[_]

  contains(command, "terraform")
  command != "terraform fmt -check"
}
```

What if someone, to get around this policy, creates a [Docker image](../../integrations/docker.md) that symlinks something very innocent-looking to `terraform`? You have two choices: replace a blocklist with an allowlist, or make sure that a known good Docker is used to execute the run. Here's an example:

```opa
package spacelift

deny[sprintf("unexpected runner image (%s)", [image])] {
  image := input.run.runtime_config.runner_image

  image != "spacelift/runner:latest"
}
```

!!! danger
    If you're using an image other than what Spacelift controls, you'll be responsible for ensuring that the attacker can't push bad code to your Docker repo.

### Enforce organizational rules

Run initialization policies can also be used enforce best practices, ensuring that the right things get executed the right way and at the right time.

One of the above examples explicitly allowlisted an OpenTofu/Terraform formatting check. This example policy ensures that command always gets executed first. Per the [Anna Karenina principle](https://en.wikipedia.org/wiki/Anna_Karenina_principle){: rel="nofollow"}, this check is most elegantly defined as a _negation_ of another rule matching the required state of affairs:

```opa
package spacelift

deny["please always run formatting check first"] {
  not formatting_first
}

formatting_first {
  input.run.runtime_config.before_init[i] == "terraform fmt -check"
  i == 0
}
```

### Enforce feature branch naming convention

Now let's enforce a feature branch naming convention. We'll keep this example simple, requiring that feature branches start with either `feature/` or `fix/`, but you can require references to Jira tickets or even look at commit messages:

```opa
package spacelift

deny[sprintf("invalid feature branch name (%s)", [branch])] {
  branch := input.commit.branch

  input.run.type == "PROPOSED"
  not re_match("^(fix|feature)\/.*", branch)
}
```

## Migration guide

A run initialization policy can be expressed as an [approval policy](./approval-policy.md) if it defines a single `reject` rule, and an `approve` rule that is its negation. Here are the initialization policy examples expressed as [approval policies](./approval-policy.md).

### Enforcing OpenTofu/Terraform check

```opa
package spacelift

reject { not formatting_first}

approve { not reject }

formatting_first {
  input.run.runtime_config.before_init[i] == "terraform fmt -check"
  i == 0
}
```

### Disallowing before-init OpenTofu/Terraform commands other than formatting

```opa
package spacelift

reject {
  command := input.run.runtime_config.before_init[_]
  contains(command, "terraform"); command != "terraform fmt -check"
}

approve { not reject }
```

### Enforcing runner image

```opa
package spacelift

reject {
  input.run.runtime_config.runner_image != "spacelift/runner:latest"
}

approve { not reject }
```

### Enforcing feature branch naming convention

```opa
package spacelift

reject {
  branch := input.run.commit.branch
  input.run.type == "PROPOSED"
  not re_match("^(fix|feature)\/.*", branch)
}

approve { not reject }
```
