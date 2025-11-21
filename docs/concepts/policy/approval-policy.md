# Approval policy

Approval policies allow organizations to create sophisticated run review and approval flows that reflect their preferred workflow, security goals, and business objectives. Without an explicit approval policy, **anyone with write access** to a stack can create a [run](../run/README.md) or [task](../run/task.md). An approval policy can make this process more granular and contextual.

Runs can be reviewed by approval policies when they enter one of three states: [queued](../run/README.md#queued), [unconfirmed](../run/tracked.md#unconfirmed), or [pending review](../run/proposed.md#pending-review). If a stack has [autodeploy](../stack/stack-settings.md#autodeploy) enabled, then the approval policy will not be evaluated here, and you should use a [plan policy](../policy/terraform-plan-policy.md) to warn, which will force the stack into an unconfirmed state, at which point the approval policy will get evaluated as a safeguard.

When a [queued](../run/README.md#queued) run needs approval, it will not be scheduled until that approval is received. If the run is of a blocking type, it will block newer runs from scheduling too. A [queued](../run/README.md#queued) run that's pending approval can be [canceled](../run/README.md#common-run-states) at any point.

## Review a run

In this example, a queued run is waiting for a human review, and the last approval policy evaluation returned an _Undecided_ decision.

1. Navigate to the _Ship Infra_ > _Runs_ tab and select the run that needs review.
      - You can also access runs for a specific stack by navigating to the _Stacks_ tab, clicking the name of the stack, and clicking the run to review in the _Tracked Run_ section.
2. Click **Review** in the top right.
    ![Review a queued run](<../../assets/screenshots/Mouse_Highlight_Overlay_and_Resource_in_a_separate_file_·_Bacon (2).png>)
3. Review the changes, then click **Approve** if the run can continue, or **Reject** if the run should be canceled.
      - If desired, you can leave a comment from your review in the text box.
    ![Approve or Reject changes](<../../assets/screenshots/Mouse_Highlight_Overlay_and_Resource_in_a_separate_file_·_Bacon (1).png>)
4. Click **Submit Review**.
5. If you approved the run, the approval policy will evaluate to Approved, thus unblocking the run.
    ![Run unblocked by approval](<../../assets/screenshots/Mouse_Highlight_Overlay_and_Resource_in_a_separate_file_·_Bacon.png>)

When an [unconfirmed](../run/tracked.md#unconfirmed) run needs approval, you will not be able to [confirm](../run/tracked.md#confirmed) it until that approval is received. The run can, however, be [discarded](../run/tracked.md#discarded) at any point:

![Discard unconfirmed run](<../../assets/screenshots/Mouse_Highlight_Overlay_and_Resource_in_a_separate_file_·_Bacon (3).png>)

The run review and approval process is very similar to GitHub's Pull Request review. The only exception is that it's the Rego policy (rather than a set of checkboxes and dropdowns) that defines the exact conditions to approve the run.

!!! tip
    If separate run approval and confirmation steps sound confusing, think about how GitHub's Pull Requests work. You can approve a PR before merging it in a separate step. A PR approval means "I'm ok with this being merged", while a run approval means "I'm OK with that action being executed".

## Rules

Your approval policy can define the following boolean rules:

- **approve**: The run is approved and no longer requires (or allows) review.
- **reject**: The run fails immediately.

While the `approve` rule must be defined in order for the run to be able to progress, you don't need to define the `reject` rule. If `reject` rules are undefined, runs that look invalid can be [canceled](../run/README.md#common-run-states) or [discarded](../run/tracked.md#discarded) manually.

Any given policy evaluation can also return `false` on both `approve` and `reject` rules. This only means that the result is yet `undecided`, and more reviews will be necessary. A perfect example would be a policy that requires 2 approvals for a given job; the first review is not supposed to set the `approve` value to `true`.

!!! info
    Users must have [`write`](./stack-access-policy.md#writers) or [`admin`](./login-policy.md#rbac-role-assignment) access to the stack to be able to approve changes.

### How it works

When a user reviews the run, Spacelift persists the review and passes it to the approval policy (along with other reviews), plus some information about the run and its stack.

The same user can review the same run as many times as they want, but **only their newest review** will be presented to the approval policy. This mechanism allows you to change your mind, very similar to Pull Request reviews in GitHub.

## Data input schema

This schema is an informational example, as JSON doesn't support comments by design. You can play with this sample (and others) using the [policy workbench](./README.md#policy-workbench) or [policy templates](./README.md#import-policy-templates).

Each approval policy request will receive this data input schema:

!!! tip "Official Schema Reference"
    For the most up-to-date and complete schema definition, please refer to the [official Spacelift policy contract schema](https://app.spacelift.io/.well-known/policy-contract.json){: rel="nofollow"} under the `APPROVAL` policy type.

```json
{
  "reviews": { // run reviews
    "current": { // reviews for the current state
      "approvals": [{ // positive reviews
        "author": "string - reviewer username",
        "author_roles": [{ // roles assigned to the reviewer
          "ulid": "string - unique identifier for the role",
          "slug": "string - URL-friendly role identifier",
          "id": "string - role slug (kept for backwards compatibility)",
          "name": "string - human-readable role name"
        }],
        "request": { // request data of the review
          "remote_ip": "string - user IP",
          "timestamp_ns": "number - review creation Unix timestamp in nanoseconds"
        },
        "session": { // session data of the review
          "login": "string - username of the reviewer",
          "name": "string - full name of the reviewer",
          "teams": ["string - names of teams the reviewer was a member of"]
        },
        "state": "string - the state of the run at the time of the approval"
      }],
      "rejections": [/* negative reviews, see "approvals" for schema */]
    },
    "older": [/* reviews for previous state(s), see "current" for schema */]
  },
  "run": { // the run metadata
    "based_on_local_workspace": "boolean - whether the run stems from a local preview",
    "branch": "string - the branch the run was triggered from",
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
    "command": "string or null, set when the run type is TASK",
    "commit": {
      "author": "string - GitHub login if available, name otherwise",
      "branch": "string - branch to which the commit was pushed",
      "created_at": "number - creation Unix timestamp in nanoseconds",
      "hash": "string - the commit hash",
      "message": "string - commit message",
      "exist_on_tracked_branch": "boolean - true if commit with this hash exist on tracked branch"
    },
    "created_at": "number - creation Unix timestamp in nanoseconds",
    "creator_session": {
      "admin": "boolean - is the current user a Spacelift admin",
      "creator_ip": "string - IP address of the user who created the session",
      "login": "string - username of the creator",
      "name": "string - full name of the creator",
      "teams": ["string - names of teams the creator was a member of"],
      "machine": "boolean - whether the run was initiated by a human or a machine"
    },
    "drift_detection": "boolean - is this a drift detection run",
    "flags": ["string - list of flags set on the run by other policies"],
    "id": "string - the run ID",
    "runtime_config": {
      "before_init": ["string - command to run before run initialization"],
      "project_root": "string - root of the Terraform project",
      "runner_image": "string - Docker image used to execute the run",
      "terraform_version": "string - Terraform version used for the run"
    },
    "state": "string - the current run state",
    "triggered_by": "string or null - user, trigger policy, or dependent stack that triggered the run. For a dependent stack, this is set to the stack ID that triggered it.",
    "type": "string - type of the run",
    "updated_at": "number - last update Unix timestamp in nanoseconds",
    "user_provided_metadata": [
      "string - blobs of metadata provided using spacectl or the API when interacting with this run"
    ]
  },
  "stack": { // the stack metadata
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
    "terraform_version": "string or null - last Terraform version used to apply changes",
    "worker_pool": {
      "id": "string - the worker pool ID, if it is private",
      "labels": ["string - list of arbitrary, user-defined selectors, if the worker pool is private"],
      "name": "string - name of the worker pool, if it is private",
      "public": "boolean - is the worker pool public"
    }
  }
}
```

## Approval policy examples

These [policy examples can be imported](./README.md#import-policy-templates) directly into your Spacelift.

!!! tip
    We maintain a [library of example policies](https://github.com/spacelift-io/spacelift-policies-example-library/tree/main/examples/approval){: rel="nofollow"} ready to use or alter to meet your specific needs.

    If you cannot find what you are looking for below or in the library, please reach out to [our support](../../product/support/README.md#contact-support) and we will craft a policy to do exactly what you need.

### Two approvals, no rejections

In this example, each Unconfirmed run (including proposed runs triggered by Git events) will require two approvals. Additionally, the run should have no rejections. Anyone who rejects the run will need to go back and approve it in order for the run to go through.

!!! info
    We suggest requiring more than one review because one approval should come from the run/commit author to indicate that they're aware of what they're doing, especially if their VCS handle is different than their IdP handle. This is something [we practice internally at Spacelift](https://spacelift.io/blog/flexible-backoffice-tool-using-slack){: rel="nofollow"}.

```opa
package spacelift

approve { input.run.state != "UNCONFIRMED" }

approve {
  count(input.reviews.current.approvals) > 1
  count(input.reviews.current.rejections) == 0
}
```

### Two to approve, two to reject

This is a variation of the above policy that will automatically fail any run that receives more than one rejection.

```opa
package spacelift

approve { input.run.state != "UNCONFIRMED" }
approve { count(input.reviews.current.approvals) > 1 }
reject  { count(input.reviews.current.rejections) > 1 }
```

### Require approval for a task command not on the allowlist

```opa
package spacelift

allowlist := ["ps", "ls", "rm -rf /"]

# Approve when not a task.
approve { input.run.type != "TASK" }

# Approve when allowlisted.
approve { input.run.command == allowlist[_] }

# Approve with two or more approvals.
approve { count(input.reviews.current.approvals) > 1 }
```

Options for input.run.type include `PROPOSED`, `TRACKED`, `TASK`, `TESTING`, `DESTROY`.

### Combining multiple rules

Usually, you will apply different rules to different types of jobs. Since approval policies are attached to stacks, you'll want to be smart about how you combine different rules. Here's how you can combine two of the above approval flows as an example:

```opa
package spacelift

# First, define all conditions that require explicit
# user approval.
requires_approval { input.run.state == "UNCONFIRMED" }
requires_approval { input.run.type == "TASK" }

# Then, automatically approve all other jobs.
approve { not requires_approval }

# Autoapprove some task commands. We don't check for run type
# because only tasks will the have "command" field set.
task_allowlist := ["ps", "ls", "rm -rf /"]
approve { input.run.command == task_allowlist[_] }

# Two approvals and no rejections to approve.
approve {
  count(input.reviews.current.approvals) > 1
  count(input.reviews.current.rejections) == 0
}
```

### Role-based approval

Sometimes you want to give specific roles (but not others) the power to approve certain workloads. The policy below approves an unconfirmed run or a task when either a Director approves it, or **both** DevOps and Security roles approve it:

```opa
package spacelift

# First, define all conditions that require explicit
# user approval.
requires_approval { input.run.state == "UNCONFIRMED" }
requires_approval { input.run.type == "TASK" }
approve           { not requires_approval }

approvals := input.reviews.current.approvals

# Define what it means to be approved by a Director, DevOps and Security.
director_approval { approvals[_].session.teams[_] == "Director" }
devops_approval   { approvals[_].session.teams[_] == "DevOps" }
security_approval { approvals[_].session.teams[_] == "Security" }

# Approve when a single Director approves:
approve { director_approval }

# Approve when both DevOps and Security approve:
approve { devops_approval; security_approval }
```

### Require private worker pool

You might want to ensure that your runs are always scheduled on a [private worker pool](../worker-pools/README.md#private-worker-pool). You could use an approval policy similar to this ones:

```opa
package spacelift

# Approve any runs on private workers
approve { not input.stack.worker_pool.public }

# Reject any runs on public workers
reject { input.stack.worker_pool.public }
```

You may want to [auto-attach this policy](./README.md#automatically-with-labels) to some, if not all, of your stacks.

### Use more descriptive approvals

Sometimes it is worth adding notes about approval/rejection to see why without Rego code analysis.

```opa
package spacelift

allowlist := ["ps", "ls"]
denylist := ["rm -rf /"]

approve_with_note[note] {
  input.run.type == "TASK"
  input.run.command == allowlist[_]
  note := sprintf("always approve tasks with command %s", [input.run.command])
}

reject_with_note[note] {
  input.run.type == "TASK"
  input.run.command == denylist[_]
  note := sprintf("always reject tasks with command %s", [input.run.command])
}
```
