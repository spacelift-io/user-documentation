# Plan policy

## Purpose

Plan policies are evaluated during a planning phase after a vendor-specific change preview command (e.g. `terraform plan`) executes successfully. The body of the change is exported to JSON and parts of it are combined with Spacelift metadata to form the data input to the policy.

Plan policies are the only ones with access to the actual changes to the managed resources, making them the best place to **enforce organizational rules and best practices** as well as do automated code review.

There are two types of rules here that Spacelift will care about: **deny** and **warn**. Each of them must come with an appropriate message that will be shown in the logs.

- **Deny rules**: Print in red. Automatically fail the run.
- **Warn rules**: Print in yellow. At most, mark the run for human review if the change affects the tracked branch and the stack is set to [autodeploy](../stack/README.md).

This simple policy will show both types of rules in action:

=== "Rego v1"
    ```opa
    package spacelift

    deny contains "you shall not pass" if {
      true # true means "match everything"
    }

    warn contains "hey, you look suspicious" if {
      true
    }
    ```

=== "Rego v0"
    ```opa
    package spacelift

    deny["you shall not pass"] {
      true # true means "match everything"
    }

    warn["hey, you look suspicious"] {
      true
    }
    ```

If you create this policy, attach it to a stack, and [trigger a run](../run/tracked.md#triggering-manually), you will see something like this:

![Failing plan policy](<../../assets/screenshots/Revert__Attempt_to_create_an_IAM_user_agains_a_policy___10_____11__·_We_test_in_prod.png>)

It works, but it's not terribly useful unless you want to block all changes to your stack in a really clumsy way.

Let's dig deeper into the [data input document](#data-input) that each plan policy receives, two possible [use cases](#use-cases) ([rule enforcement](#organizational-rule-enforcement) and [automated code review](#automated-code-review)) and some [examples](#examples).

## Data input

This is the data input schema each policy request will receive. If the policy is executed for the first time, the `previous_run` field will be missing.

!!! tip "Official Schema Reference"
    For the most up-to-date and complete schema definition, please refer to the [official Spacelift policy contract schema](https://app.spacelift.io/.well-known/policy-contract.json){: rel="nofollow"} under the `PLAN` policy type.

```json
{
  "spacelift": {
    "commit": {
      "author": "string - GitHub login if available, name otherwise",
      "branch": "string - branch to which the commit was pushed",
      "created_at": "number  - creation Unix timestamp in nanoseconds",
      "hash": "string - the commit hash",
      "message": "string - commit message"
    },
    "request": {
      "timestamp_ns": "number - current Unix timestamp in nanoseconds"
    },
    "previous_run": {
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
      "commit": {
        "author": "string - GitHub login if available, name otherwise",
        "branch": "string - branch to which the commit was pushed",
        "created_at": "number  - creation Unix timestamp in nanoseconds",
        "hash": "string - the commit hash",
        "message": "string - commit message"
      },
      "created_at": "number - creation Unix timestamp in nanoseconds",
      "drift_detection": "boolean - is this a drift detection run",
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
      "type": "string - type of the run",
      "updated_at": "number - last update Unix timestamp in nanoseconds",
      "user_provided_metadata": [
        "string - blobs of metadata provided using spacectl or the API when interacting with this run"
      ]
    },
    "run": {
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
      "commit": {
        "author": "string - GitHub login if available, name otherwise",
        "branch": "string - branch to which the commit was pushed",
        "created_at": "number  - creation Unix timestamp in nanoseconds",
        "hash": "string - the commit hash",
        "message": "string - commit message"
      },
      "created_at": "number - creation Unix timestamp in nanoseconds",
      "drift_detection": "boolean - is this a drift detection run",
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
      "type": "string - type of the run",
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
      "name": "string - name of the stack",
      "repository": "string - name of the source GitHub repository",
      "state": "string - current state of the stack",
      "terraform_version": "string or null - last Terraform version used to apply changes",
      "tracked_commit": {
        "author": "string - GitHub login if available, name otherwise",
        "branch": "string - branch to which the commit was pushed",
        "created_at": "number  - creation Unix timestamp in nanoseconds",
        "hash": "string - the commit hash",
        "message": "string - commit message"
      },
      "worker_pool": {
        "id": "string - the worker pool ID, if it is private",
        "labels": ["string - list of arbitrary, user-defined selectors, if the worker pool is private"],
        "name": "string - name of the worker pool, if it is private",
        "public": "boolean - is the worker pool public"
      }
    }
  },
  "terraform": {
    "resource_changes": [
      {
        "address": "string - full address of the resource, including modules",
        "type": "string - type of the resource, eg. aws_iam_user",
        "locked_by": "optional string - if the stack is locked, this is the name of the user who did it",
        "name": "string - name of the resource, without type",
        "namespace": "string - repository namespace, only relevant to GitLab repositories",
        "project_root": "optional string - project root as set on the Stack, if any",
        "provider_name": "string - provider managing the resource, eg. aws",
        "change": {
          "actions": ["string - create, update, delete or no-op"],
          "before": "optional object - content of the resource",
          "after": "optional object - content of the resource"
        }
      }
    ],
    "terraform_version": "string"
  }
}
```

### Aliases

In addition to our [helper functions](./README.md#helper-functions), we provide aliases for commonly used parts of the input data:

| Alias                 | Description                                                                   |
| --------------------- | ----------------------------------------------------------------------------- |
| `affected_resources`  | List of the resources that will be created, deleted, and updated by Terraform |
| `created_resources`   | List of the resources that will be created by Terraform                       |
| `deleted_resources`   | List of the resources that will be deleted by Terraform                       |
| `recreated_resources` | List of the resources that will be deleted and then created by Terraform      |
| `updated_resources`   | List of the resources that will be updated by Terraform                       |

## String sanitization

Sensitive properties in `"before"` and `"after"` objects will be sanitized to protect secret values. Sanitization hashes the value with the sha256 algorithm and takes the last 8 bytes of the hash.

If you need to compare a string property to a constant, use the `sanitized(string)` helper function.

=== "Rego v1"
    ```opa
    package spacelift

    deny contains "must not target the forbidden endpoint: forbidden.endpoint/webhook" if {
      some resource in input.terraform.resource_changes

      actions := {"create", "delete", "update"}
      some action in resource.change.actions
      actions[action]

      resource.change.after.endpoint == sanitized("forbidden.endpoint/webhook")
    }
    ```

=== "Rego v0"
    ```opa
    package spacelift

    deny["must not target the forbidden endpoint: forbidden.endpoint/webhook"] {
      resource := input.terraform.resource_changes[_]

      actions := {"create", "delete", "update"}
      actions[resource.change.actions[_]]

      resource.change.after.endpoint == sanitized("forbidden.endpoint/webhook")
    }
    ```

## Custom inputs

Sometimes you need to pass some additional data to your policy input. For example, you may want to pass the result of a third-party API to tool call to the `configuration` data from the Terraform plan. To use custom inputs:

1. Generate a JSON file with the data you need at the root of your project.
2. The file name must follow the pattern `$key.custom.spacelift.json` and represent a valid JSON _object_.
      - The file name is case-sensitive.
3. The object will be merged with the rest of the input data, as `input.third_party_metadata.custom.$key`.

Below are two examples, one exposing Terraform configuration and the other exposing the result of a third-party security tool.

!!! Tip
    To learn more about integrating security tools with Spacelift using custom inputs, refer to our [blog post](https://spacelift.io/blog/integrating-security-tools-with-spacelift){: rel="nofollow"}.

### Exposing Terraform configuration to the plan policy

To expose the Terraform configuration to the plan policy to ensure that only the "blessed" modules are used to provision resources, add this command to the list of [`after_plan` hooks](../stack/stack-settings.md#customizing-workflow):

```bash
terraform show -json spacelift.plan | jq -c '.configuration' > configuration.custom.spacelift.json
```

The data will be available in the policy input as `input.third_party_metadata.custom.configuration`. This depends on the `jq` tool being available in the runner image. It is installed by default on our standard image.

### Passing custom tool output to the plan policy

For this example, we will generate warnings (from the open-source Terraform security scanner [_tfsec_](https://github.com/aquasecurity/tfsec){: rel="nofollow"}) as JSON and have them reported and processed using the plan policy.

Run `tfsec` as a [`before_init` hook](../stack/stack-settings.md#customizing-workflow) and save the output to a file:

```bash
tfsec -s --format=json . > tfsec.custom.spacelift.json
```

The data will be available in the policy input as `input.third_party_metadata.custom.tfsec`. This depends on the `tfsec` tool being available in the runner image, which you will need to install either directly on the image or as part of your `before_init` hook.

Some vulnerability scanning tools, like `tfsec`, will return a non-zero exit code when they encounter vulnerabilities, which will result in a stack failure. The majority of these tools provide a soft scanning option that will show all the vulnerabilities without considering the command as failed, which we will use instead.

If your tool doesn't offer soft scanning, append `|| true` at the end of the command, which always returns a zero exit code.

## Use cases

Since plan policies have access to the infrastructure changes that are about to be introduced, you can run all sorts of checks against those changes. There are two main use cases for those checks:

- [Organizational rule enforcement](terraform-plan-policy.md#organizational-rule-enforcement) to prevent rules that go against organizational policies.
- [Automated code review](terraform-plan-policy.md#automated-code-review) to augment human decision-making.

### Organizational rule enforcement

In every organization, there are some things you do not touch, such as:

- A particular line of code surrounded by comments warning, if you change it, the site will go down and the on-call personnel will be after you.
- Potential security vulnerabilities that can expose all your infrastructure to the wrong crowd.

Spacelift can turn these organizational hard rules into policies that can't be broken. You will most likely want to exclusively use **deny** rules.

In this example, we introduce a simple rule: never create static AWS credentials.

=== "Rego v1"
    ```opa
    package spacelift

    # The message here is dynamic and captures resource address to provide
    # appropriate context to anyone affected by this policy. For the sake of your
    # sanity and that of your colleagues, always add a message when denying a change.
    deny contains sprintf(message, [resource.address]) if {
      message := "static AWS credentials are evil (%s)"

      some resource in input.terraform.resource_changes
      some action in resource.change.actions
      action == "create"

      # This is what decides whether the rule captures a resource.
      # There may be an arbitrary number of conditions, and they all must
      # succeed for the rule to take effect.
      resource.type == "aws_iam_access_key"
    }
    ```

=== "Rego v0"
    ```opa
    package spacelift

    # The message here is dynamic and captures resource address to provide
    # appropriate context to anyone affected by this policy. For the sake of your
    # sanity and that of your colleagues, always add a message when denying a change.
    deny[sprintf(message, [resource.address])] {
      message := "static AWS credentials are evil (%s)"

      resource := input.terraform.resource_changes[_]
      resource.change.actions[_] == "create"

      # This is what decides whether the rule captures a resource.
      # There may be an arbitrary number of conditions, and they all must
      # succeed for the rule to take effect.
      resource.type == "aws_iam_access_key"
    }
    ```

This slightly more sophisticated policy states that when some resources are recreated, they should be [created before they're destroyed](https://developer.hashicorp.com/terraform/language/meta-arguments/lifecycle#create_before_destroy){: rel="nofollow"} or an outage will follow. We found this to be an issue with [`aws_batch_compute_environment`](https://www.terraform.io/docs/providers/aws/r/batch_compute_environment.html){: rel="nofollow"}, among other resources.

=== "Rego v1"
    ```opa
    package spacelift

    # This is what Rego calls a set. You can add further elements to it as necessary.
    always_create_first := {"aws_batch_compute_environment"}

    deny contains sprintf(message, [resource.address]) if {
      message := "always create before deleting (%s)"
      some resource in input.terraform.resource_changes

      # Make sure the type is on the list.
      always_create_first[resource.type]

      some i_create, i_delete
      resource.change.actions[i_create] == "create"
      resource.change.actions[i_delete] == "delete"

      i_delete < i_create
    }
    ```

=== "Rego v0"
    ```opa
    package spacelift

    # This is what Rego calls a set. You can add further elements to it as necessary.
    always_create_first := { "aws_batch_compute_environment" }

    deny[sprintf(message, [resource.address])] {
      message  := "always create before deleting (%s)"
      resource := input.terraform.resource_changes[_]

      # Make sure the type is on the list.
      always_create_first[resource.type]

      some i_create, i_delete
      resource.change.actions[i_create] == "create"
      resource.change.actions[i_delete] == "delete"


      i_delete < i_create
    }
    ```

While in most cases you'll want your rules to only look at resources affected by the change, you're not limited to doing so. You can look at all resources and force teams to remove certain resources. Here's an example where until AWS resources are all removed in one go, no further changes can take place:

=== "Rego v1"
    ```opa
    package spacelift

    deny contains sprintf(message, [resource.address]) if {
      message := "we've moved to GCP, find an equivalent there (%s)"
      some resource in input.terraform.resource_changes

      resource.provider_name == "aws"

      # If you're just deleting, all good.
      resource.change.actions != ["delete"]
    }
    ```

=== "Rego v0"
    ```opa
    package spacelift

    deny[sprintf(message, [resource.address])] {
      message  := "we've moved to GCP, find an equivalent there (%s)"
      resource := input.terraform.resource_changes[_]

      resource.provider_name == "aws"

      # If you're just deleting, all good.
      resource.change.actions != ["delete"]
    }
    ```

### Automated code review

In addition to enforcing hard rules, plan policy rules can help humans understand changes better and make informed decisions on what looks good and what does not.

**Warn** rules look like this:

![Warn rules in action](<../../assets/screenshots/Revert__Attempt_to_create_an_IAM_user_agains_a_policy___10_____11__·_We_test_in_prod (1).png>)

The warn rule won't fail your plan and can provide great help to a human reviewer, especially when multiple changes are introduced. Also, if a stack is set to [autodeploy](../stack/README.md), the presence of a single warning is enough to flag the run for a human review.

The best way to use warn and deny rules together depends on your preferred Git workflow. We've found short-lived feature branches with Pull Requests to the tracked branch to work relatively well. In this scenario, the `type` of the run is important: _PROPOSED_ for commits to feature branches, and _TRACKED_ on commits to the tracked branch. Your rules should use this mechanism to balance comprehensive feedback on Pull Requests and the flexibility of being able to deploy things that humans deem appropriate.

As a general rule when using plan policies for code review, **deny** when run type is _PROPOSED_ and **warn** when it is _TRACKED_. Denying tracked runs unconditionally may be a good idea for most egregious violations, but when this approach is taken to an extreme it can make your life difficult.

We suggest that you _at most_ **deny** when the run is _PROPOSED_, which will send a failure status to the GitHub commit, then give the reviewer a chance to approve the change anyways. If you want a human to take another look before those changes go live, either set [stack autodeploy](../stack/README.md) to _false_ or explicitly **warn** about potential violations. Here's an example of how to reuse the same rule to **deny** or **warn** depending on the run type:

=== "Rego v1"
    ```opa
    package spacelift

    proposed := input.spacelift.run.type == "PROPOSED"

    deny contains reason if { proposed; some reason in iam_user_created }
    warn contains reason if { not proposed; some reason in iam_user_created }

    iam_user_created contains sprintf("do not create IAM users: (%s)", [resource.address]) if {
      some resource in input.terraform.resource_changes
      some action in resource.change.actions
      action == "create"

      resource.type == "aws_iam_user"
    }
    ```

=== "Rego v0"
    ```opa
    package spacelift

    proposed := input.spacelift.run.type == "PROPOSED"

    deny[reason] { proposed; reason := iam_user_created[_] }
    warn[reason] { not proposed; reason := iam_user_created[_] }

    iam_user_created[sprintf("do not create IAM users: (%s)", [resource.address])] {
      resource := input.terraform.resource_changes[_]
      resource.change.actions[_] == "create"

      resource.type == "aws_iam_user"
    }
    ```

Predictably, this fails when committed to a non-tracked (feature) branch:

![Fail plan policy when committed to non-tracked branch](<../../assets/screenshots/Attempt_to_create_an_IAM_user_agains_a_policy_·_We_test_in_prod.png>)

...but as a GitHub repo admin you can still merge it if you've set your branch protection rules accordingly:

![Can still merge failed run](<../../assets/screenshots/Attempt_to_create_an_IAM_user_against_a_policy_by_marcinwyszynski_·_Pull_Request__10_·_spacelift-io_marcinw-end-to-end.png>)

If we squash and merge:

![Plan policy stopping the run to wait for human user](<../../assets/screenshots/Attempt_to_create_an_IAM_user_agains_a_policy___10__·_We_test_in_prod.png>)

The run stopped to await a human decision. At this point, we still have a choice to either [confirm](../run/README.md#discarded) or [discard](../run/README.md#discarded) the run. In the latter case, you will likely want to revert the commit that caused the problem, otherwise all subsequent runs will be affected.

## Examples

!!! tip
    We maintain a [library of example policies](https://github.com/spacelift-io/spacelift-policies-example-library/tree/main/examples/plan){: rel="nofollow"} that are ready to use or alter to meet your specific needs.

    If you cannot find what you are looking for below or in the library, please reach out to [our support](../../product/support/README.md#contact-support) and we will craft a policy to do exactly what you need.

### Require human review when resources are changed

Adding resources may cost a lot of money, but it's usually safe from an operational perspective. Let's use a `warn` rule to allow changes with only added resources to get automatically applied, and require all others to get a human review:

=== "Rego v1"
    ```opa
    package spacelift

    warn contains sprintf(message, [action, resource.address]) if {
      message := "action '%s' requires human review (%s)"
      review := {"update", "delete"}

      some resource in input.terraform.resource_changes
      some action in resource.change.actions

      review[action]
    }
    ```

=== "Rego v0"
    ```opa
    package spacelift

    warn[sprintf(message, [action, resource.address])] {
      message := "action '%s' requires human review (%s)"
      review  := {"update", "delete"}

      resource := input.terraform.resource_changes[_]
      action   := resource.change.actions[_]

      review[action]
    }
    ```

### Automatically deploy changes from selected individuals

Sometimes changes introduced by trusted individuals can be deployed automatically, especially if they already went through code review. This example allows commits from allowlisted individuals to be deployed automatically (and assumes the stack is set to [autodeploy](../stack/README.md)):

=== "Rego v1"
    ```opa
    package spacelift

    warn contains sprintf(message, [author]) if {
      message := "%s is not on the allowlist - human review required"
      author := input.spacelift.commit.author
      allowlisted := {"alice", "bob", "charlie"}

      not allowlisted[author]
    }
    ```

=== "Rego v0"
    ```opa
    package spacelift

    warn[sprintf(message, [author])] {
      message     := "%s is not on the allowlist - human review required"
      author      := input.spacelift.commit.author
      allowlisted := { "alice", "bob", "charlie" }

      not allowlisted[author]
    }
    ```

### Require commits to be reasonably sized

Massive changes make reviewers miserable. In this example, we automatically fail all changes that affect more than 50 resources but allow them to be deployed with mandatory human review:

=== "Rego v1"
    ```opa
    package spacelift

    proposed := input.spacelift.run.type == "PROPOSED"

    deny contains msg if { proposed; some msg in too_many_changes }
    warn contains msg if { not proposed; some msg in too_many_changes }

    too_many_changes contains msg if {
      threshold := 50

      res := input.terraform.resource_changes
      ret := count([r | some r in res; r.change.actions != ["no-op"]])
      msg := sprintf("more than %d changes (%d)", [threshold, ret])

      ret > threshold
    }
    ```

=== "Rego v0"
    ```opa
    package spacelift

    proposed := input.spacelift.run.type == "PROPOSED"

    deny[msg] { proposed; msg := too_many_changes[_] }
    warn[msg] { not proposed; msg := too_many_changes[_] }

    too_many_changes[msg] {
      threshold := 50

      res := input.terraform.resource_changes
      ret := count([r | r := res[_]; r.change.actions != ["no-op"]])
      msg := sprintf("more than %d changes (%d)", [threshold, ret])

      ret > threshold
    }
    ```

### Back-of-the-envelope blast radius

This is a fancy contrived example building on top of the previous one. However, rather than looking at the total number of affected resources, it attempts to create a metric called a "blast radius": how much the change will affect the whole stack.

It assigns special multipliers to some types of resources changed and treats different types of changes differently: deletes and updates are more "expensive" because they affect live resources, while new resources are generally safer and thus "cheaper". Per our [automated code review](terraform-plan-policy.md#automated-code-review) pattern, we will fail Pull Requests with changes violating this policy, but require human action through **warnings** when these changes hit the tracked branch.

=== "Rego v1"
    ```opa
    package spacelift

    proposed := input.spacelift.run.type == "PROPOSED"

    deny contains msg if { proposed; some msg in blast_radius_too_high }
    warn contains msg if { not proposed; some msg in blast_radius_too_high }

    blast_radius_too_high contains sprintf("change blast radius too high (%d/100)", [blast_radius]) if {
      blast_radius := sum([blast |
                            some resource in input.terraform.resource_changes
                            blast := blast_radius_for_resource(resource)])

      blast_radius > 100
    }

    blast_radius_for_resource(resource) := ret if {
      blasts_radii_by_action := {"delete": 10, "update": 5, "create": 1, "no-op": 0}

      ret := sum([value |
                        some action in resource.change.actions
                        action_impact := blasts_radii_by_action[action]
                        type_impact := blast_radius_for_type(resource.type)
                        value := action_impact * type_impact])
    }

    # Let's give some types of resources special blast multipliers.
    blasts_radii_by_type := {"aws_ecs_cluster": 20, "aws_ecs_user": 10, "aws_ecs_role": 5}

    # By default, blast radius has a value of 1.
    blast_radius_for_type(type) := 1 if {
        not blasts_radii_by_type[type]
    }

    blast_radius_for_type(type) := ret if {
        blasts_radii_by_type[type] = ret
    }
    ```

=== "Rego v0"
    ```opa
    package spacelift

    proposed := input.spacelift.run.type == "PROPOSED"

    deny[msg] { proposed; msg := blast_radius_too_high[_] }
    warn[msg] { not proposed; msg := blast_radius_too_high[_] }

    blast_radius_too_high[sprintf("change blast radius too high (%d/100)", [blast_radius])] {
      blast_radius := sum([blast |
                            resource := input.terraform.resource_changes[_];
                            blast := blast_radius_for_resource(resource)])

      blast_radius > 100
    }

    blast_radius_for_resource(resource) = ret {
      blasts_radii_by_action := { "delete": 10, "update": 5, "create": 1, "no-op": 0 }

        ret := sum([value | action := resource.change.actions[_]
                        action_impact := blasts_radii_by_action[action]
                        type_impact := blast_radius_for_type(resource.type)
                        value := action_impact * type_impact])
    }

    # Let's give some types of resources special blast multipliers.
    blasts_radii_by_type := { "aws_ecs_cluster": 20, "aws_ecs_user": 10, "aws_ecs_role": 5 }

    # By default, blast radius has a value of 1.
    blast_radius_for_type(type) = 1 {
        not blasts_radii_by_type[type]
    }

    blast_radius_for_type(type) = ret {
        blasts_radii_by_type[type] = ret
    }
    ```

### Cost management

Thanks to our Infracost integration, [you can take cost information into account](../../vendors/terraform/infracost.md#plan-policies) when deciding whether to ask for human approval or to block changes entirely.
