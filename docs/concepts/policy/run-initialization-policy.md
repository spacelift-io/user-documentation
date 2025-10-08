# Initialization policy

!!! warning
    This feature is deprecated. New users should not use this feature and existing users are encouraged to migrate to the [approval policy](./approval-policy.md), which offers a much more flexible and powerful way to control which runs are allowed to proceed. A migration guide is available [here](#migration-guide).

## Purpose

Initialization policy can prevent a [Run](../run/README.md) or a [Task](../run/task.md) from being [initialized](../run/README.md#initializing), thus blocking any custom code or commands from being executed. It superficially looks like a [plan policy](terraform-plan-policy.md) in that it affects an existing Run and prints feedback to logs, but it does not get access to the plan. Instead, it can be used to [protect your stack from unwanted changes](run-initialization-policy.md#protect-your-stack-from-unwanted-changes) or [enforce organizational rules](run-initialization-policy.md#enforce-organizational-rules) concerning how and when runs are supposed to be triggered.

!!! warning
    Server-side initialization policies are being deprecated. We will be replacing them with [worker-side policies](../worker-pools#configuration-options) that can be set by using the launcher run initialization policy flag (`SPACELIFT_LAUNCHER_RUN_INITIALIZATION_POLICY`).

    For a limited time period we will be running both types of initialization policy checks but ultimately we're planning to move the pre-flight checks to the worker node, thus allowing customers to block suspicious looking jobs on their end.

Let's create a simple initialization policy, attach it to the stack, and see what gives:

```opa
package spacelift

deny["you shall not pass"] {
  true
}
```

...and boom:

![](<../../assets/screenshots/Initial_commit_·_Stack_managed_by_Spacelift (1).png>)

## Rules

Initialization policies are simple in that they only use a single rule - **deny** - with a string message. A single result for that rule will fail the run before it has a chance to start - as we've just witnessed above.

## Data input

This is the schema of the data input that each policy request will receive:

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
|------------------|----------------------------|
| `commit`         | `input.commit`             |
| `run`            | `input.run`                |
| `runtime_config` | `input.run.runtime_config` |
| `stack`          | `input.stack`              |

## Use cases

There are two main use cases for run initialization policies - [protecting your stack from unwanted changes](run-initialization-policy.md#protect-your-stack-from-unwanted-changes) and [enforcing organizational rules](run-initialization-policy.md#enforce-organizational-rules). Let's look at these one by one.

### Protect your stack from unwanted changes

While specialized, Spacelift is still a CI/CD platform and thus allows running custom code before Terraform initialization phase using [`before_init`](../configuration/runtime-configuration/README.md#before_init-scripts)scripts. This is a very powerful feature, but as always, with great power comes great responsibility. Since those scripts get full access to your Terraform environment, how hard is it to create a commit on a feature branch that would run [`terraform destroy -auto-approve`](https://www.terraform.io/docs/commands/destroy.html){: rel="nofollow"}? Sure, all Spacelift runs are tracked and this prank will sooner or later be tracked down to the individual who ran it, but at that point do you still have a business?

That's where initialization policies can help. Let's explicitly blacklist all Terraform commands if they're running as [`before_init`](../configuration/runtime-configuration/README.md#before_init-scripts) scripts. OK, let's maybe add a single exception for a formatting check.

```opa
package spacelift

deny[sprintf("don't use Terraform please (%s)", [command])] {
  command := input.run.runtime_config.before_init[_]

  contains(command, "terraform")
  command != "terraform fmt -check"
}
```

Feel free to play with this example in [the Rego playground](https://play.openpolicyagent.org/p/V0sr5abgWI){: rel="nofollow"}.

OK, but what if someone gets clever and creates a [Docker image](../../integrations/docker.md) that symlinks something very innocent-looking to `terraform`? Well, you have two choices - you could replace a blacklist with a whitelist, but a clever attacker can be really clever. So the other choice is to make sure that a known good Docker is used to execute the run. Here's an example:

```opa
package spacelift

deny[sprintf("unexpected runner image (%s)", [image])] {
  image := input.run.runtime_config.runner_image

  image != "spacelift/runner:latest"
}
```

Here's the above example in [the Rego playground](https://play.openpolicyagent.org/p/VxIREPOS0d){: rel="nofollow"}.

!!! danger
    Obviously, if you're using an image other than what we control, you still have to ensure that the attacker can't push bad code to your Docker repo. Alas, this is beyond our control.

### Enforce organizational rules

While the previous section was all about making sure that bad stuff does not get executed, this use case presents run initialization policies as a way to ensure best practices - ensuring that the right things get executed the right way and at the right time.

One of the above examples explicitly whitelisted OpenTofu/Terraform formatting check. Keeping your code formatted in a standard way is generally a good idea, so let's make sure that this command always gets executed first. Note that as per [Anna Karenina principle](https://en.wikipedia.org/wiki/Anna_Karenina_principle){: rel="nofollow"} this check is most elegantly defined as a _negation_ of another rule matching the required state of affairs:

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

Here's this example [in the Rego playground](https://play.openpolicyagent.org/p/ghtWZGhbgP){: rel="nofollow"}.

This time we'll skip the mandatory "don't deploy on weekends" check because while it could also be implemented here, there are probably better places to do it. Instead, let's enforce a feature branch naming convention. We'll keep this example simple, requiring that feature branches start with either `feature/` or `fix/`, but you can go fancy and require references to Jira tickets or even look at commit messages:

```opa
package spacelift

deny[sprintf("invalid feature branch name (%s)", [branch])] {
  branch := input.commit.branch

  input.run.type == "PROPOSED"
  not re_match("^(fix|feature)\/.*", branch)
}
```

Here's this example [in the Rego playground](https://play.openpolicyagent.org/p/qNMygC4i9K){: rel="nofollow"}.

## Migration guide

A run initialization policy can be expressed as an [approval policy](./approval-policy.md) if it defines a single `reject` rule, and an `approve` rule that is its negation. Below you will find equivalents of the examples above expressed as [approval policies](./approval-policy.md).

### Migration example: enforcing OpenTofu/Terraform check

```opa
package spacelift

reject { not formatting_first}

approve { not reject }

formatting_first {
  input.run.runtime_config.before_init[i] == "terraform fmt -check"
  i == 0
}
```

### Migration example: disallowing before-init OpenTofu/Terraform commands other than formatting

```opa
package spacelift

reject {
  command := input.run.runtime_config.before_init[_]
  contains(command, "terraform"); command != "terraform fmt -check"
}

approve { not reject }
```

### Migration example: enforcing runner image

```opa
package spacelift

reject {
  input.run.runtime_config.runner_image != "spacelift/runner:latest"
}

approve { not reject }
```

### Migration example: enforcing feature branch naming convention

```opa
package spacelift

reject {
  branch := input.run.commit.branch
  input.run.type == "PROPOSED"
  not re_match("^(fix|feature)\/.*", branch)
}

approve { not reject }
```
