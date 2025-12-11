# Push policy

{% if is_saas() %}
!!! hint
    This feature is only available to paid Spacelift accounts. Please check out our [pricing page](https://spacelift.io/pricing){: rel="nofollow"} for more information.
{% endif %}

Git push policies are triggered on a per-stack basis to determine the action that should be taken for each individual [stack](../../stack/README.md) or [module](../../../vendors/terraform/module-registry.md) in response to a Git push or Pull Request notification. There are three possible outcomes:

- **track**: Set the new head commit on the [stack](../../stack/README.md) or [module](../../../vendors/terraform/module-registry.md) and create a [tracked run](../../run/tracked.md) (one that can be [applied](../../run/tracked.md#applying)).
- **propose**: Create a [proposed run](../../run/proposed.md) against a proposed version of infrastructure.
- **ignore**: Do not schedule a new run.

You can create sophisticated, custom-made setups using push policies. We can think of two main (not mutually exclusive) use cases:

- Ignore changes to certain paths. This is something you'd find useful both with classic monorepos and repositories containing multiple Terraform projects under different paths.
- Apply only a subset of changes, such as only commits tagged in a certain way.

## Git push policy and tracked branch

Each stack and module points at a particular Git branch called a [tracked branch](../../stack/stack-settings.md#vcs-integration-and-repository). By default, any push to the tracked branch that changes a file in the project root triggers a tracked [run](../../run/README.md) that can be [applied](../../run/tracked.md#applying). This logic can be changed entirely by a Git push policy, but the tracked branch is always reported as part of the stack input to the policy evaluator and can be used as a point of reference.

![The tracked branch head commit is behind the head commit of the stack.](<../../../assets/screenshots/Screenshot 2022-07-05 at 14-48-52 Runs · example stack.png>)

When a push policy does not track a new push, the head commit of the stack/module will not be set to the tracked branch head commit. Sync the tracked branch head commit with the head commit of the stack/module by navigating to that stack and pressing the sync button.

## Push and Pull Request events

Spacelift can currently react to two types of events: _push_ and _pull request_ (also called _merge request_ by GitLab). Push events are the default; even if you don't have a push policy set up, we will respond to those events. Pull request events are supported for some VCS providers and are generally received when you open, synchronize (push a new commit), label, or merge the pull request.

In some cases, Spacelift can receive both _push_ and _pull request_ events at the same time. Review the [data input schema](#data-input-schema) and [how rules are evaluated](#how-rules-are-evaluated) to ensure your push policies perform as expected.

There are some valid reasons to use _pull request_ events in addition or instead of push ones. For example, when making decisions based on the paths of affected files, push events are often confusing:

- They contain affected files for all commits in a push, not just the head commit.
- They are not context-aware, making it hard to work with pull requests; if a given push is ignored on an otherwise relevant PR, then the Spacelift status check is not provided.

Here are a few samples of PR-driven policies from real-life use cases, each reflecting a slightly different way of structuring your workflow.

First, let's only trigger proposed runs if a PR exists, and allow any push to the tracked branch to trigger a tracked run:

```opa
package spacelift

track   { input.push.branch == input.stack.branch }
propose { not is_null(input.pull_request) }
ignore  { not track; not propose }
```

If you want to enforce that tracked runs are _always_ created from PR merges (and not from direct pushes to the tracked branch), you can tweak the above policy accordingly to ignore all non-PR events:

```opa
package spacelift

track   { is_pr; input.push.branch == input.stack.branch }
propose { is_pr }
ignore  { not is_pr }
is_pr   { not is_null(input.pull_request) }
```

Here's another example where you respond to a particular PR label ("deploy") to automatically deploy changes:

```opa
package spacelift

track   { is_pr; labeled }
propose { true }
is_pr   { not is_null(input.pull_request) }
labeled { input.pull_request.labels[_] == "deploy" }
```

!!! info
    When a run is triggered from a **GitHub** Pull Request and the Pull Request is **mergeable** (meaning there are no merge conflicts), we check out the code for something called the "potential merge commit". This virtual commit represents the potential result of merging the Pull Request into its base branch and should provide higher quality, less confusing feedback.

### Deduplicating events

If you're using pull requests in your flow, Spacelift might receive duplicate events. For example, if you push to a feature branch and then open a pull request, Spacelift first receives a _push_ event, then a separate _pull request (opened)_ event. When you push another commit to that feature branch, we again receive two events: _push_ and _pull request (synchronized)_. When you merge the pull request, we get two more: _push_ and _pull request (closed)_.

Push policies could resolve to the same actionable (not _ignore_) outcome (e.g. _track_ or _propose_). In those cases, instead of creating two separate runs, we debounce the events by deduplicating runs created by them on a per-stack basis.

The deduplication key consists of the commit SHA and run type. If your policy returns two different actionable outcomes for two different events associated with a given SHA, both runs will be created. In practice, this would be an unusual corner case and a reason to revisit your workflow.

When events are deduplicated and you're sampling policy evaluations, you may notice that there are two samples for the same SHA, each with different input. You can generally assume that the first one creates a run.

## Canceling in-progress runs

You can use push policies to pre-empt any in-progress runs with the new run. The input document includes the `in_progress` key, which contains an array of runs that are currently either still [queued](../../run/README.md#queued), [ready](../../run/README.md#ready), or [awaiting human confirmation](../../run/tracked.md#unconfirmed). You can use it in conjunction with the cancel rule like this:

```opa
cancel[run.id] { run := input.in_progress[_] }
```

Of course, you can use a more sophisticated approach and only choose to cancel a certain type of run, or runs in a particular state. For example, this rule will only cancel proposed runs that are currently queued (waiting for the worker):

```opa
cancel[run.id] {
  run := input.in_progress[_]
  run.type == "PROPOSED"
  run.state == "QUEUED"
}
```

You can also compare branches and cancel proposed runs in queued state pointing to a specific branch:

```opa
cancel[run.id] {
  run := input.in_progress[_]
  run.type == "PROPOSED"
  run.state == "QUEUED"
  run.branch == input.pull_request.head.branch
}
```

### Cancelation restrictions

There are some restrictions on cancelation:

- Module test runs cannot be canceled. Only proposed and tracked stack runs can be canceled.
- Cancelation works based on a new run pre-empting existing runs. What this means is that if your push policy does not result in any runs being triggered, the cancelation will have no effect.
- A run can only cancel other runs of the _same type_. For example a proposed run can only cancel other proposed runs, not tracked runs.
- Cancelation is _best effort_ and not guaranteed. If the run is picked up by the worker or approved by a human in the meantime, the cancelation itself is canceled.

## Configuring Ignore event behavior

### Customize VCS check messages for Ignored Run events

To customize the messages sent back to your VCS when Spacelift runs are ignored, use the `message` function within your Push policy. See the [example policy](#example-policy) for reference.

### Customize check status for Ignored Run events

By default, ignored runs on a stack will return a `skipped` status check event, rather than a fail event. If you want ignored run events to have a `failed` status check on your VCS, set the `fail` function value to `true` in your Push policy.

### Example policy

The following push policy does not trigger any run within Spacelift. Using this policy, we can ensure that the status check within our VCS (in this case, GitHub) fails and returns the message "I love bacon."

```opa
fail { true }
message["I love bacon"] { true }
```

With this policy, users would see this behavior within their GitHub status check:

![GitHub status check behavior](<../../../assets/screenshots/Screen Shot 2022-06-13 at 2.07.31 PM.png>)

!!! info
    This behavior (customization of the message and failing of the check within the VCS), is only applicable when runs **do not take place within Spacelift.**

## Tag-driven Terraform module release flow

You can use a simple push policy to manage your Terraform module versions using git tags and push your module to the Spacelift module registry using git tag events. Use the `module_version` block within a push policy attached your module, and then set the version using the tag information from the git push event.

For example, this push policy will trigger a tracked run when a tag event is detected, then parses the tag event data and uses that value for the module version. We remove a git tag prefixed with `v` as the Terraform module registry only supports versions in a numeric `X.X.X` format.

For this policy, you will need to provide a mock, non-existent version for proposed runs. This precaution has been taken to ensure that pull requests do not encounter check failures due to the existence of versions that are already in use.

```opa
package spacelift

module_version := version {
    version := trim_prefix(input.push.tag, "v")
    not propose
}

module_version := "<X.X.X>" {
    propose
}

propose {
  not is_null(input.pull_request)
  }
```

To add a track rule to your push policy, this will start a tracked run when the module version is not empty and the push branch is the same as the one the module branch is tracking:

```opa
track {
  module_version != ""
  input.push.branch == input.module.branch
 }
```

## Allow forks

By default, Spacelift doesn't trigger runs when a forked repository opens a pull request against your repository. This is to prevent a security incident. For example, if your infrastructure were open source, someone could fork it, implement unwanted code, then open a pull request for the original repository that would automatically run.

!!! info
    The cause is very similar to GitHub Actions, where they don't expose repository secrets when forked repositories open pull requests.

If you want to allow forks to trigger runs, you can explicitly do it with `allow_fork` rule. For example, if you trust certain people or organizations, this rule allows a forked repository to run **only** if the owner of the forked repo is `johnwayne` or `microsoft`:

```opa
propose { true }
allow_fork {
  validOwners := {"johnwayne", "microsoft"}
  validOwners[input.pull_request.head_owner]
}
```

The `head_owner` field means different things in different VCS providers:

| VCS provider                    | Meaning of `head_owner` field                        | Where to find it                                                                                                     |
| ------------------------------- | ---------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| **GitHub/GitHub Enterprise**    | The organization or person who owns the forked repo. | In the URL: `https://github.com/<head_owner>/<forked_repository>`.                                                   |
| **GitLab**                      | The group of the repository.                         | In the URL: `https://gitlab.com/<head_owner>/<forked_repository>`.                                                   |
| **Azure DevOps**                | The ID of the forked repo's project (a UUID).        | Open `https://dev.azure.com/<organization>/_apis/projects` in your browser to see all projects and their unique IDs. |
| **Bitbucket Cloud**             | Workspace.                                           | In the URL: `https://www.bitbucket.org/<workspace>/<forked_repository>`                                              |
| **Bitbucket Datacenter/Server** | The project key of the repo.                         | The display name of the project and its abbreviation (all caps).                                                     |

## Approval and mergeability

The `pull_request` property on the input to a push policy contains the following fields:

- `approved`: Indicates whether the PR has been approved.
- `mergeable`: Indicates whether the PR can be merged.
- `undiverged`: Indicates that the PR branch is not behind the target branch.

This push policy will automatically deploy a PR's changes once it has been approved, any required checks have completed, and the PR has a `deploy` label added to it:

```rego
package spacelift

# Trigger a tracked run if a change is pushed to the stack branch
track {
  affected
  input.push.branch == input.stack.branch
}

# Trigger a tracked run if a PR is approved, mergeable, undiverged and has a deploy label
track {
  is_pr
  is_clean
  is_approved
  is_marked_for_deploy
}

# Trigger a proposed run if a PR is opened
propose {
  is_pr
}

is_pr {
  not is_null(input.pull_request)
}

is_clean {
  input.pull_request.mergeable
  input.pull_request.undiverged
}

is_approved {
  input.pull_request.approved
}

is_marked_for_deploy {
  input.pull_request.labels[_] == "deploy"
}
```

Each source control provider has slightly different features, and because of this, the exact definition of `approved` and `mergeable` varies slightly.

### GitHub / GitHub Enterprise <!-- markdownlint-disable-line MD024 -->

- `approved`: The PR has at least one approval, and also meets any minimum approval requirements for the repo.
- `mergeable`: The PR branch has no conflicts with the target branch, and any branch protection rules have been met.

### GitLab <!-- markdownlint-disable-line MD024 -->

- `approved`: The PR has at least one approval. If approvals are required, it is only `true` when all required approvals have been made.
- `mergeable`: The PR branch has no conflicts with the target branch, any blocking discussions have been resolved, and any required approvals have been made.

### Azure DevOps <!-- markdownlint-disable-line MD024 -->

- `approved`: The PR has at least one approving review (including approved with suggestions).
- `mergeable`: The PR branch has no conflicts with the target branch, and any blocking policies are approved.

!!! info
    We are unable to calculate divergence across forks in Azure DevOps, so the `undiverged` property will always be `false` for PRs created from forks.

### Bitbucket Cloud <!-- markdownlint-disable-line MD024 -->

- `approved`: The PR has at least one approving review from someone other than the PR author.
- `mergeable`: The PR branch has no conflicts with the target branch.

### Bitbucket Datacenter/Server <!-- markdownlint-disable-line MD024 -->

- `approved`: The PR has at least one approving review from someone other than the PR author.
- `mergeable`: The PR branch has no conflicts with the target branch.

## Data input schema

As input, Git push policy receives the following:

!!! tip "Official Schema Reference"
    For the most up-to-date and complete schema definition, please refer to the [official Spacelift policy contract schema](https://app.spacelift.io/.well-known/policy-contract.json){: rel="nofollow"} under the `GIT_PUSH` policy type.

```json
{
  "in_progress": [{
    "based_on_local_workspace": "boolean - whether the run stems from a local preview",
    "branch": "string - the branch this run is based on",
    "created_at": "number - creation Unix timestamp in nanoseconds",
    "triggered_by": "string or null - user or trigger policy who triggered the run, if applicable",
    "type": "string - run type: proposed, tracked, task, etc.",
    "state": "string - run state: queued, unconfirmed, etc.",
    "updated_at": "number - last update Unix timestamp in nanoseconds",
    "user_provided_metadata": ["string - blobs of metadata provided using spacectl or the API when interacting with this run"]
  }],
  "pull_request": {
    "action": "string - opened, reopened, closed, merged, edited, labeled, synchronize, unlabeled",
    "action_initiator": "string",
    "approved": "boolean - indicates whether the PR has been approved",
    "author": "string",
    "base": {
      "affected_files": ["string"],
      "author": "string",
      "branch": "string",
      "created_at": "number (timestamp in nanoseconds)",
      "message": "string",
      "tag": "string"
    },
    "closed": "boolean",
    "diff": ["string - list of files changed between base and head commit"],
    "draft": "boolean - indicates whether the PR is marked as draft",
    "head": {
      "affected_files": ["string"],
      "author": "string",
      "branch": "string",
      "created_at": "number (timestamp in nanoseconds)",
      "message": "string",
      "tag": "string"
    },
    "head_owner": "string",
    "id": "number",
    "labels": ["string"],
    "mergeable": "boolean - indicates whether the PR can be merged",
    "title": "string",
    "undiverged": "boolean - indicates whether the PR is up to date with the target branch"
  },
  "push": {
    // For Git push events, this contains the pushed commit.
    // For Pull Request events,
    // this contains the head commit or merge commit if available (merge event).
    "affected_files": ["string"],
    "author": "string",
    "branch": "string",
    "created_at": "number (timestamp in nanoseconds)",
    "message": "string",
    "tag": "string"
  },
  "stack": {
    "additional_project_globs": ["string - list of arbitrary, user-defined selectors"],
    "administrative": "boolean",
    "roles": [{
      "id": "string - the role slug, eg. space-admin",
      "name": "string - the role name"
    }],
    "autodeploy": "boolean",
    "branch": "string",
    "id": "string",
    "labels": ["string - list of arbitrary, user-defined selectors"],
    "locked_by": "optional string - if the stack is locked, this is the name of the user who did it",
    "name": "string",
    "namespace": "string - repository namespace, only relevant to GitLab repositories",
    "project_root": "optional string - project root as set on the Stack, if any",
    "repository": "string",
    "state": "string",
    "terraform_version": "string or null",
    "tracked_commit": {
      "author": "string",
      "branch": "string",
      "created_at": "number (timestamp in nanoseconds)",
      "hash": "string",
      "message": "string"
    },
    "worker_pool": {
      "public": "boolean - indicates whether the worker pool is public or not"
    }
  },
  "vcs_integration": {
    "id": "string - ID of the VCS integration",
    "name": "string - name of the VCS integration",
    "provider": "string - possible values are AZURE_DEVOPS, BITBUCKET_CLOUD, BITBUCKET_DATACENTER, GIT, GITHUB, GITHUB_ENTERPRISE, GITLAB",
    "description": "string - description of the VCS integration",
    "is_default": "boolean - indicates whether the VCS integration is the default one or Space-level",
    "space": {
      "id": "string",
      "labels": ["string"],
      "name": "string"
    },
    "labels": ["string - list of arbitrary, user-defined selectors"],
    "updated_at": "number (timestamp in nanoseconds)",
    "created_at": "number (timestamp in nanoseconds)"
  }
}
```

### New module version schema

When triggered by a _new module version_, this is the schema of the data input that each policy request will receive:

```json

{
  "module": { // Module for which the new version was released
    "administrative": "boolean - is the stack administrative",
    "branch": "string - tracked branch of the module",
    "labels": ["string - list of arbitrary, user-defined selectors"],
    "current_version": "Newly released module version",
    "id": "string - unique ID of the module",
    "name": "string - name of the stack",
    "namespace": "string - repository namespace, only relevant to GitLab repositories",
    "project_root": "optional string - project root as set on the Module, if any",
    "repository": "string - name of the source GitHub repository",
    "space": {
        "id": "string",
        "labels": ["string"],
        "name": "string"
      },
    "terraform_version": "string or null - last Terraform version used to apply changes",
    "worker_pool": {
      "id": "string - the worker pool ID, if it is private",
      "labels": ["string - list of arbitrary, user-defined selectors, if the worker pool is private"],
      "name": "string - name of the worker pool, if it is private",
      "public": "boolean - is the worker pool public"
    }
  },
  "pull_request": {
    "action": "string - opened, reopened, closed, merged, edited, labeled, synchronize, unlabeled",
    "action_initiator": "string",
    "approved": "boolean - indicates whether the PR has been approved",
    "author": "string",
    "base": {
      "affected_files": ["string"],
      "author": "string",
      "branch": "string",
      "created_at": "number (timestamp in nanoseconds)",
      "message": "string",
      "tag": "string"
    }
  },
  "vcs_integration": {
    "id": "bitbucket-for-payments-team",
    "name": "Bitbucket for Payments Team",
    "provider": "BITBUCKET_CLOUD",
    "description": "### Payments Team BB integration\n\nThis integration should be **only** used by the Payments Integrations team. If you need access, drop [Joe](https://mycorp.slack.com/users/432JOE435) a message on Slack.",
    "is_default": false,
    "labels": ["bitbucketcloud", "paymentsorg"],
    "space": {
      "id": "paymentsteamspace-01HN0BF3GMYZQ4NYVNQ1RKQ9M7",
      "labels": [],
      "name": "PaymentsTeamSpace"
    },
    "created_at": 1706187931079960000,
    "updated_at": 1706274820310231000
  }
}
```

### How rules are evaluated

Based on this input, the policy may define boolean `track`, `propose` and `ignore` rules.

- The positive outcome of at least one `ignore` rule causes the push to be ignored, no matter the outcome of other rules.
- The positive outcome of at least one `track` rule triggers a _tracked_ run.
- The positive outcome of at least one `propose` rule triggers a _proposed_ run.

If no rules are matched, the default is to **ignore** the push. Always supply an exhaustive set of policies, making sure that they define what to **track** and what to **propose** in addition to defining what they **ignore**.

You can also define an auxiliary rule called `ignore_track`, which overrides a positive outcome of the `track` rule but does not affect other rules, most notably `propose`. This can be used to turn some of the pushes that would otherwise be applied into test runs.

## Examples

!!! tip
    We maintain a [library of example policies](https://github.com/spacelift-io/spacelift-policies-example-library/tree/main/examples/push){: rel="nofollow"} ready to use or alter to meet your specific needs.

    If you cannot find what you are looking for below or in the library, please reach out to [our support](../../../product/support/README.md#contact-support) and we will craft a policy to do exactly what you need.

### Ignoring certain paths

Ignoring changes to certain paths is something you'd find useful both with classic monorepos and repositories containing multiple OpenTofu/Terraform projects under different paths. When evaluating a push, we determine the list of affected files by looking at all the files touched by any of the commits in a given push.

!!! info
    This list may include false positives, for example in a situation where you delete a given file in one commit, bring it back in another commit, then push multiple commits at once. This is a safer default than trying to figure out the exact scope of each push.

Imagine a situation where you only want to look at changes to Terraform definitions (in HCL or [JSON](https://www.terraform.io/docs/configuration/syntax-json.html){: rel="nofollow"}) inside one the `production/` or `modules/` directory, and have `track` and `propose` use their default settings:

```opa
package spacelift

track   { input.push.branch == input.stack.branch }
propose { input.push.branch != "" }
ignore  { not affected }

affected {
  some i, j, k

  tracked_directories := {"modules/", "production/"}
  tracked_extensions := {".tf", ".tf.json"}

  path := input.push.affected_files[i]

  startswith(path, tracked_directories[j])
  endswith(path, tracked_extensions[k])
}
```

To keep the example readable we had to define `ignore` in a negative way, per [the Anna Karenina principle](https://en.wikipedia.org/wiki/Anna_Karenina_principle){: rel="nofollow"}.

### Status checks and ignored pushes

By default when the push policy instructs Spacelift to ignore a certain change, no commit status check is sent back to the VCS. This behavior is explicitly designed to prevent noise in monorepo scenarios where a large number of stacks are linked to the same Git repo.

However, you may still be interested in learning that the push was ignored, or getting a commit status check for a given stack when it's set as required by [GitHub's branch protection](https://docs.github.com/en/github/administering-a-repository/managing-a-branch-protection-rule){: rel="nofollow"} rules or your internal organization rules.

In that case, you can use the `notify` rule to override default notification settings. So if you want to notify your VCS vendor even when a commit is ignored, you can define it like this:

```opa
package spacelift

# other rules (including ignore), see above

notify { ignore }
```

!!! info
    The `notify` rule (_false_ by default) only applies to ignored pushes, so you can't set it to `false` to silence commit status checks for [proposed runs](../../run/proposed.md).

### Applying from a tag

Another use case for a Git push policy would be to apply from a newly created _tag_ rather than from a branch. This can be useful in multiple scenarios. For example, a staging/QA environment could be deployed every time a certain tag type is applied to a tested branch, thereby providing inline feedback on a GitHub Pull Request from the actual deployment rather than a plan/test. You could also constrain production to only apply from tags unless a run is explicitly triggered by the user.

Here's an example:

```opa
package spacelift

track   { re_match(`^\d+\.\d+\.\d+$`, input.push.tag) }
propose { input.push.branch != input.stack.branch }
```

### Set head commit without triggering a run

The `track` decision sets the new head commit on the affected stack or [module](../../../vendors/terraform/module-registry.md). This head commit is used when a tracked run is manually triggered or a [task](../../run/task.md) is started on the stack. In this case, you normally want to have a new tracked run, so that's what we do by default.

However, sometimes you want to trigger tracked runs in a specific order or under specific circumstances either manually or using a [trigger policy](../trigger-policy.md). So what you want is an option to set the head commit without triggering a run. The boolean `notrigger` rule will work in conjunction with the `track` decision and prevent the tracked run from being created.

`notrigger` does not depend in any way on the `track` rule; they're entirely independent. Spacelift will only look at `notrigger` if `track` evaluates to _true_ when interpreting the result of the policy.

Here's an example of using the two rules together to always set the new commit on the stack, but not trigger a run. You would use this when the run is always triggered [manually](../../run/tracked.md#triggering-manually), through [the API](../../../integrations/api.md), or using a [trigger policy](../trigger-policy.md):

```opa
track     { input.push.branch == input.stack.branch }
propose   { not track }
notrigger { true }
```

### Default Git push policy

If no Git push policies are attached to a stack or a module, the default behavior is equivalent to this policy:

```opa
package spacelift

track {
  affected
  input.push.branch == input.stack.branch
}

propose { affected }
propose { affected_pr }

ignore  {
    not affected
    not affected_pr
}
ignore  { input.push.tag != "" }

affected {
    filepath := input.push.affected_files[_]
    startswith(normalize_path(filepath), normalize_path(input.stack.project_root))
}

affected {
    filepath := input.push.affected_files[_]
    glob_pattern := input.stack.additional_project_globs[_]
    glob.match(glob_pattern, ["/"], normalize_path(filepath))
}

affected_pr {
    filepath := input.pull_request.diff[_]
    startswith(normalize_path(filepath), normalize_path(input.stack.project_root))
}

affected_pr {
    filepath := input.pull_request.diff[_]
    glob_pattern := input.stack.additional_project_globs[_]
    glob.match(glob_pattern, ["/"], normalize_path(filepath))
}

# Helper function to normalize paths by removing leading slashes
normalize_path(path) = trim(path, "/")
```

### Waiting for CI/CD artifacts

There are cases where you want pushes to your repo to trigger a run in Spacelift, but only after a CI/CD pipeline (or a part of it) has completed. An example would be when you want to trigger an infra deploy **after** some Docker image has been built and pushed to a registry.

You can use push policies' [external dependencies](run-external-dependencies.md) feature to achieve this.

### Prioritization

Although we generally recommend using our default scheduling order (tracked runs and tasks, then proposed runs, then drift detection runs), you can use push policies to prioritize certain runs over others. For example, you may want to prioritize runs triggered by a certain user or a certain branch.

Use the boolean `prioritize` rule to mark a run as prioritized:

```opa
package spacelift

# other rules (including ignore), see above

prioritize { input.stack.labels[_] == "prioritize" }
```

This example will prioritize runs on any stack that has the `prioritize` label set. **Run prioritization only works for private worker pools**. An attempt to prioritize a run on a public worker pool using this policy will not work.

### Stack locking

Stack locking can be particularly useful in workflows heavily reliant on pull requests. The push policy enables you to lock and unlock a stack based on specific criteria using the `lock` and `unlock` rules.

`lock` rule behavior when a non-empty string is returned:

- Lock the stack if it's currently unlocked.
- No change if the stack is already locked by the same owner.
- Reject any runs if the stack is locked by a different owner and you attempt to lock it.

`unlock` rule behavior when a non-empty string is returned:

- No change if the stack is currently unlocked.
- Unlock the stack if it's locked by the same owner.
- No change if the stack is locked by a different owner.

!!! info
    Runs are only rejected if the push policy rules result in an attempt to acquire a lock on an already locked stack with a different lock key. If the `lock` rule is undefined or results in an empty string, runs will not be rejected.

This example policy snippet locks a stack when a pull request is opened or synchronized, and unlocks it when the pull request is closed or merged. Add `import future.keywords` to your policy to use this exact snippet.

``` opa
lock_id := sprintf("PR_ID_%d", [input.pull_request.id])

lock := lock_id {
    input.pull_request.action in ["opened", "synchronize"]
}

unlock := lock_id {
    input.pull_request.action in ["closed", "merged"]
}
```

You can customize selectively locking and unlocking the stacks whose project root or project globs are set to track the files in the pull request:

``` opa
lock_id := sprintf("PR_ID_%d", [input.pull_request.id])

lock := lock_id if {
    input.pull_request.action in ["opened", "synchronize"]
    affected_pr
}

unlock := lock_id if {
    input.pull_request.action in ["closed", "merged"]
    affected_pr
}

affected_pr if {
    some filepath in input.pull_request.diff
    startswith(filepath, input.stack.project_root)
}

affected_pr if {
    some filepath in input.pull_request.diff
    some glob_pattern in input.stack.additional_project_globs
    glob.match(glob_pattern, ["/"], filepath)
}
```

You can also lock and unlock through [comments](../../run/pull-request-comments.md):

``` opa
unlock := lock_id {
    input.pull_request.action == "commented"
    input.pull_request.comment == concat(" ", ["/spacelift", "unlock", input.stack.id])
}
```

You can then unlock your stack by commenting something such as:

```text
/spacelift unlock my-stack-id
```
