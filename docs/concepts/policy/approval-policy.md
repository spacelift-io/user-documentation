# Approval policy

The approval policy allows organizations to create sophisticated run review and approval flows that reflect their preferred workflow, security goals, and business objectives. Without an explicit approval policy, anyone with write access to a stack can create a [run](../run/) (or a [task](../run/task.md)). An approval policy can make this way more granular and contextual.

Runs can be reviewed when they enter one of the two states - [queued](../run/#queued) or [unconfirmed](../run/tracked.md#unconfirmed). When a [queued](../run/#queued) run needs approval, it will not be scheduled before that approval is received, and if it is of a blocking type, it will block newer runs from scheduling, too. A [queued](../run/#queued) run that's pending approval can be [canceled](../run/#canceled) at any point.

Here's an example of a queued run waiting for a human review - note how the last approval policy evaluation returned an _Undecided_ decision. There's also a review button next to the cancelation one:

![](<../../.gitbook/assets/Mouse\_Highlight\_Overlay\_and\_Resource\_in\_a\_separate\_file\_·\_Bacon (2).png>)

Review can be positive (approve) or negative (reject):

![](<../../.gitbook/assets/Mouse\_Highlight\_Overlay\_and\_Resource\_in\_a\_separate\_file\_·\_Bacon (1).png>)

With a positive review, the approval policy could evaluate to Approve thus unblocking the run:

![](../../.gitbook/assets/Mouse\_Highlight\_Overlay\_and\_Resource\_in\_a\_separate\_file\_·\_Bacon.png)

When an [unconfirmed](../run/tracked.md#unconfirmed) run needs approval, you will not be able to [confirm](../run/tracked.md#confirmed) it until that approval is received. The run can however be [discarded](../run/tracked.md#discarded) at any point:

![](<../../.gitbook/assets/Mouse\_Highlight\_Overlay\_and\_Resource\_in\_a\_separate\_file\_·\_Bacon (3).png>)

In principle, the run review and approval process are very similar to GitHub's Pull Request review, the only exception being that it's the Rego policy (rather than a set of checkboxes and dropdowns) that defines the exact conditions to approve the run.

{% hint style="success" %}
If separate run approval and confirmation steps sound confusing, don't worry. Just think about how GitHub's Pull Requests work - you can approve a PR before merging it in a separate step. A PR approval means "I'm OK with this being merged". A run approval means "I'm OK with that action being executed".
{% endhint %}

## Rules

Your approval policy can define the following boolean rules:

* **approve**: the run is approved and no longer requires (or allows) review;
* **reject**: the run fails immediately;

While the 'approve' rule must be defined in order for the run to be able to progress, it's perfectly valid to not define the 'reject' rule. In that case, runs that look invalid can be cleaned up ([canceled](../run/#canceled) or [discarded](../run/tracked.md#discarded)) manually.

It's also perfectly acceptable for any given policy evaluation to return 'false' on both 'approve' and 'reject' rules. This only means that the result is yet 'undecided' and more reviews will be necessary to reach the conclusion. A perfect example would be a policy that requires 2 approvals for a given job - the first review is not yet supposed to set the 'approve' value to 'true'.

#### How it works

When a user reviews the run, Spacelift persists their review and passes it to the approval policy, along with other reviews, plus some information about the run and its stack. The same user can review the same run as many times as they want, but only their newest review will be presented to the approval policy. This mechanism allows you to change your mind, very similar to Pull Request reviews.

## Data input

This is the schema of the data input that each policy request will receive:

```jsonp
{
  "reviews": { // run reviews
    "current": { // reviews for the current state
      "approvals": [{ // positive reviews
        "author": "string - reviewer username",
        "request": { // request data of the review
          "remote_ip": "string - user IP",
          "timestamp_ns": "number - review creation Unix timestamp in nanoseconds",
        },
        "session": { // session data of the review
          "login": "string - username of the reviewer",
          "name": "string - full name of the reviewer",
          "teams": ["string - names of teams the reviewer was a member of"]
        },
        "state": "string - the state of the run at the time of the approval",
      }],
      "rejections": [/* negative reviews, see "approvals" for schema */]
    },
    "older": [/* reviews for previous state(s), see "current" for schema */]
  },
  "run": { // the run metadata
    "based_on_local_workspace": "boolean - whether the run stems from a local preview",
    "command": "string or null, set when the run type is TASK",
    "created_at": "number - creation Unix timestamp in nanoseconds",
    "runtime_config": {
      "before_init": ["string - command to run before run initialization"],
      "project_root": "string - root of the Terraform project",
      "runner_image": "string - Docker image used to execute the run",
      "terraform_version": "string - Terraform version used to for the run"
    },
    "triggered_by": "string or null - user or trigger policy who triggered the run, if applicable",
    "type": "string - type of the run",
    "updated_at": "number - last update Unix timestamp in nanoseconds"
    "user_provided_metadata": ["string - blobs of metadata provided using spacectl or the API when interacting with this run"]
  },
  "stack": { // the stack metadata
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
  },
}
```

## Examples

### Two approvals and no rejections to approve an Unconfirmed run

In this example, each Unconfirmed run will require two approvals - including proposed runs triggered by Git events. Additionally, the run should have no rejections. Anyone who rejects the run will need to change their mind in order for the run to go through.

{% hint style="info" %}
We suggest requiring more than one review because one approval should come from the run/commit author to indicate that they're aware of what they're doing, especially if their VCS handle is different than their IdP handle. This is something [we practice internally at Spacelift](https://spacelift.io/blog/flexible-backoffice-tool-using-slack).
{% endhint %}

```python
package spacelift

approve { input.run.state != "UNCONFIRMED" }

approve {
  count(input.reviews.current.approvals) > 1
  count(input.reviews.current.rejections) == 0
}
```

Here's a [minimal example to play with](https://play.openpolicyagent.org/p/Xhn6OL9OUP).

### Two to approve, two to reject

This is a variation of the above policy, but one that will automatically fail any run that receives more than one rejection.

```
package spacelift

approve { input.run.state != "UNCONFIRMED" }
approve { count(input.reviews.current.approvals) > 1 }
reject  { count(input.reviews.current.rejections) > 1 }
```

Here's a [minimal example to play with](https://play.openpolicyagent.org/p/swoLeAV4zq).

### Require approval for a task command not on the allowlist

```python
package spacelift

allowlist := ["ps", "ls", "rm -rf /"]

# Approve when not a task.
approve { input.run.type != "TASK" }

# Approve when allowlisted.
approve { input.run.command == allowlist[_] }

# Approve with two or more approvals.
approve { count(input.reviews.current.approvals) > 1 }
```

Here's a [minimal example to play with](https://play.openpolicyagent.org/p/iKwd84nfjR).

### Combining multiple rules

Usually, you will want to apply different rules to different types of jobs. Since approval policies are attached to stacks, you will want to be smart about how you combine different rules. Here's how you can do that in a readable way, combining two of the above approval flows as an example:

```python
package spacelift

# First, let's define all conditions that require explicit
# user approval.
requires_approval { input.run.state == "UNCONFIRMED" }
requires_approval { input.run.type == "TASK" }

# Then, let's automatically approve all other jobs.
approve { not requires_approval }

# Autoapprove some task commands. Note how we don't check for run type
# because only tasks will the have "command" field set.
task_allowlist := ["ps", "ls", "rm -rf /"]
approve { input.run.command == task_allowlist[_] }

# Two approvals and no rejections to approve.
approve {
  count(input.reviews.current.approvals) > 1
  count(input.reviews.current.rejections) == 0
}
```

Here's a [minimal example to play with](https://play.openpolicyagent.org/p/lvLa713Cyq).

### Role-based approval

Sometimes you want to give certain roles but not others the power to approve certain workloads. The policy below approves an unconfirmed run or a task when either a Director approves it, or **both** DevOps and Security roles approve it:

```perl
package spacelift

# First, let's define all conditions that require explicit
# user approval.
requires_approval { input.run.state == "UNCONFIRMED" }
requires_approval { input.run.type == "TASK" }
approve           { not requires_approval }

approvals := input.reviews.current.approvals

# Let's define what it means to be approved by a director, DevOps amd Security.
director_approval { approvals[_].session.teams[_] == "Director" }
devops_approval   { approvals[_].session.teams[_] == "DevOps" }
security_approval { approvals[_].session.teams[_] == "Security" }

# Approve when a single director approves:
approve { director_approval }

# Approve when both DevOps and Security approve:
approve { devops_approval; security_approval }
```

Here's a [minimal example to play with](https://play.openpolicyagent.org/p/GHcGbz1S8H).
