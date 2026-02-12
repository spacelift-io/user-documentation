# Migrating to Approval Policies

!!! info
    This guide helps you migrate from deprecated [initialization policies](./run-initialization-policy.md) and [task policies](./task-run-policy.md) to the more powerful and flexible [approval policies](../approval-policy.md).

## Why migrate?

Approval policies provide a unified, more powerful approach to controlling runs and tasks:

- **Unified policy type**: One policy type for both runs and tasks instead of separate policies
- **Human review workflows**: Support manual approval/rejection with comments, not just automatic decisions
- **Role-based approvals**: Require specific teams or roles to approve changes
- **Richer context**: Access to reviews, run state, creator information, and more
- **Flexible approval logic**: Combine multiple conditions (e.g., "2 approvals + no rejections" or "Director approval OR both DevOps and Security")
- **Better feedback**: Descriptive approval/rejection reasons with `approve_with_note` and `reject_with_note`

## Migration overview

The migration pattern is straightforward:

**Old pattern (init/task policies):**

=== "Rego v1"
    ```opa
    package spacelift

    deny contains "reason" if <condition>
    ```

=== "Rego v0"
    ```opa
    package spacelift

    deny["reason"] { <condition> }
    ```

**New pattern (approval policy):**

=== "Rego v1"
    ```opa
    package spacelift

    reject if <condition>
    approve if not reject
    ```

=== "Rego v0"
    ```opa
    package spacelift

    reject { <condition> }
    approve { not reject }
    ```

## Data input differences

When migrating, be aware of these data structure changes between old and new policy types.

### From initialization policies

When migrating from initialization policies to approval policies, the input data structure changes:

| Old Location (Initialization Policy) | New Location (Approval Policy) | Notes |
|--------------------------------------|--------------------------------|-------|
| `input.commit` | `input.run.commit` | Commit information (author, branch, hash, message) |
| `input.run` | `input.run` | Run metadata - structure largely unchanged |
| `input.stack` | `input.stack` | Stack metadata - structure largely unchanged |
| `input.request.timestamp_ns` | `input.run.created_at` | Timestamp of when the run was created |
| N/A | `input.reviews` | **New**: Contains approval/rejection reviews |
| N/A | `input.run.creator_session` | **New**: Session info for the user who created the run |
| N/A | `input.run.drift_detection` | **New**: Whether this is a drift detection run |

### From task policies

When migrating from task policies to approval policies, the input data structure changes:

| Old Location (Task Policy) | New Location (Approval Policy) | Notes |
|----------------------------|--------------------------------|-------|
| `input.request.command` | `input.run.command` | The task command to execute |
| `input.session` | `input.run.creator_session` | User who created the task run |
| `input.request.timestamp_ns` | `input.run.created_at` | Timestamp of when the task was created |
| `input.request.remote_ip` | `input.run.creator_session.creator_ip` | IP address of the user who created the task |
| `input.stack` | `input.stack` | Stack metadata - structure largely unchanged |
| N/A | `input.reviews` | **New**: Contains approval/rejection reviews |
| N/A | `input.run.type` | **New**: Set to `"TASK"` for task runs |

!!! tip
    The approval policy has access to richer context through `input.reviews`, which enables human review workflows. You can require specific teams or roles to approve runs/tasks, check the number of approvals/rejections, and more.

## Initialization policy migration

Initialization policies prevented runs from starting based on runtime configuration, commit details, or other pre-execution conditions.

### Use case 1: Block dangerous before_init commands

**Scenario**: Prevent users from running dangerous Terraform commands in `before_init` hooks, while allowing safe operations like formatting checks.

**Old initialization policy:**

=== "Rego v1"
    ```opa
    package spacelift

    deny contains sprintf("don't use Terraform please (%s)", [command]) if {
      some command in input.run.runtime_config.before_init
      contains(command, "terraform")
      command != "terraform fmt -check"
    }
    ```

=== "Rego v0"
    ```opa
    package spacelift

    deny[sprintf("don't use Terraform please (%s)", [command])] {
      command := input.run.runtime_config.before_init[_]
      contains(command, "terraform")
      command != "terraform fmt -check"
    }
    ```

**New approval policy:**

=== "Rego v1"
    ```opa
    package spacelift

    reject if {
      some command in input.run.runtime_config.before_init
      contains(command, "terraform")
      command != "terraform fmt -check"
    }

    approve if not reject
    ```

=== "Rego v0"
    ```opa
    package spacelift

    reject {
      command := input.run.runtime_config.before_init[_]
      contains(command, "terraform")
      command != "terraform fmt -check"
    }

    approve { not reject }
    ```

**Enhanced with approval policy features:**

You can now add descriptive feedback and allow manual override:

=== "Rego v1"
    ```opa
    package spacelift

    dangerous_command if {
      some command in input.run.runtime_config.before_init
      contains(command, "terraform")
      command != "terraform fmt -check"
    }

    # Auto-reject dangerous commands
    reject_with_note contains sprintf("Dangerous terraform command in before_init: %s. Only 'terraform fmt -check' is allowed. If you need to run this command, contact your admin for approval.", [command]) if {
      some command in input.run.runtime_config.before_init
      contains(command, "terraform")
      command != "terraform fmt -check"
    }

    # Allow admin override via manual approval
    approve if {
      dangerous_command
      some approval in input.reviews.current.approvals
      some role in approval.author_roles
      role.slug == "space-admin"
    }

    # Auto-approve safe runs
    approve if not dangerous_command
    ```

=== "Rego v0"
    ```opa
    package spacelift

    dangerous_command {
      command := input.run.runtime_config.before_init[_]
      contains(command, "terraform")
      command != "terraform fmt -check"
    }

    # Auto-reject dangerous commands
    reject_with_note[sprintf("Dangerous terraform command in before_init: %s. Only 'terraform fmt -check' is allowed. If you need to run this command, contact your admin for approval.", [command])] {
      command := input.run.runtime_config.before_init[_]
      contains(command, "terraform")
      command != "terraform fmt -check"
    }

    # Allow admin override via manual approval
    approve {
      dangerous_command
      input.reviews.current.approvals[_].author_roles[_].slug == "space-admin"
    }

    # Auto-approve safe runs
    approve { not dangerous_command }
    ```

### Use case 2: Enforce runner image compliance

**Scenario**: Ensure runs only use approved Docker images to prevent malicious code execution.

**Old initialization policy:**

=== "Rego v1"
    ```opa
    package spacelift

    deny contains sprintf("unexpected runner image (%s)", [image]) if {
      image := input.run.runtime_config.runner_image
      image != "spacelift/runner:latest"
    }
    ```

=== "Rego v0"
    ```opa
    package spacelift

    deny[sprintf("unexpected runner image (%s)", [image])] {
      image := input.run.runtime_config.runner_image
      image != "spacelift/runner:latest"
    }
    ```

**New approval policy:**

=== "Rego v1"
    ```opa
    package spacelift

    reject if input.run.runtime_config.runner_image != "spacelift/runner:latest"

    approve if not reject
    ```

=== "Rego v0"
    ```opa
    package spacelift

    reject { input.run.runtime_config.runner_image != "spacelift/runner:latest" }

    approve { not reject }
    ```

**Enhanced with approval policy features:**

Support multiple approved images and require security team approval for exceptions:

=== "Rego v1"
    ```opa
    package spacelift

    approved_images := {
      "spacelift/runner:latest",
      "spacelift/runner:stable",
      "my-org/custom-runner:v1.0.0",
    }

    image_approved if {
      some img in approved_images
      input.run.runtime_config.runner_image == img
    }

    # Auto-approve runs with approved images
    approve if image_approved

    # Require security team approval for unapproved images
    reject_with_note contains sprintf("Runner image '%s' is not on the approved list. Security team approval required.", [input.run.runtime_config.runner_image]) if {
      not image_approved
      count(input.reviews.current.approvals) == 0
    }

    # Allow with security team approval
    approve if {
      not image_approved
      some approval in input.reviews.current.approvals
      some team in approval.session.teams
      team == "Security"
    }
    ```

=== "Rego v0"
    ```opa
    package spacelift

    approved_images := {
      "spacelift/runner:latest",
      "spacelift/runner:stable",
      "my-org/custom-runner:v1.0.0",
    }

    image_approved {
      approved_images[input.run.runtime_config.runner_image]
    }

    # Auto-approve runs with approved images
    approve { image_approved }

    # Require security team approval for unapproved images
    reject_with_note[sprintf("Runner image '%s' is not on the approved list. Security team approval required.", [input.run.runtime_config.runner_image])] {
      not image_approved
      count(input.reviews.current.approvals) == 0
    }

    # Allow with security team approval
    approve {
      not image_approved
      input.reviews.current.approvals[_].session.teams[_] == "Security"
    }
    ```

### Use case 3: Enforce workflow requirements

**Scenario**: Require that `terraform fmt -check` always runs first in the `before_init` sequence.

**Old initialization policy:**

=== "Rego v1"
    ```opa
    package spacelift

    deny contains "please always run formatting check first" if not formatting_first

    formatting_first if {
      input.run.runtime_config.before_init[i] == "terraform fmt -check"
      i == 0
    }
    ```

=== "Rego v0"
    ```opa
    package spacelift

    deny["please always run formatting check first"] { not formatting_first }

    formatting_first {
      input.run.runtime_config.before_init[i] == "terraform fmt -check"
      i == 0
    }
    ```

**New approval policy:**

=== "Rego v1"
    ```opa
    package spacelift

    reject if not formatting_first

    approve if not reject

    formatting_first if {
      input.run.runtime_config.before_init[i] == "terraform fmt -check"
      i == 0
    }
    ```

=== "Rego v0"
    ```opa
    package spacelift

    reject { not formatting_first }

    approve { not reject }

    formatting_first {
      input.run.runtime_config.before_init[i] == "terraform fmt -check"
      i == 0
    }
    ```

**Enhanced with approval policy features:**

Provide clearer feedback and allow overrides for emergency situations:

=== "Rego v1"
    ```opa
    package spacelift

    formatting_first if {
      count(input.run.runtime_config.before_init) > 0
      input.run.runtime_config.before_init[0] == "terraform fmt -check"
    }

    no_before_init if count(input.run.runtime_config.before_init) == 0

    # Auto-approve if formatting check is first or no before_init commands
    approve if formatting_first
    approve if no_before_init

    # Reject with helpful message
    reject_with_note contains "The 'terraform fmt -check' command must run first in before_init hooks. Current first command: " + first_command if {
      not formatting_first
      not no_before_init
      count(input.run.runtime_config.before_init) > 0
      first_command := input.run.runtime_config.before_init[0]
      count(input.reviews.current.approvals) == 0
    }

    # Allow DevOps lead to override in emergencies
    approve if {
      not formatting_first
      not no_before_init
      some approval in input.reviews.current.approvals
      some team in approval.session.teams
      team == "DevOps-Lead"
    }
    ```

=== "Rego v0"
    ```opa
    package spacelift

    formatting_first {
      count(input.run.runtime_config.before_init) > 0
      input.run.runtime_config.before_init[0] == "terraform fmt -check"
    }

    no_before_init { count(input.run.runtime_config.before_init) == 0 }

    # Auto-approve if formatting check is first or no before_init commands
    approve { formatting_first }
    approve { no_before_init }

    # Reject with helpful message
    reject_with_note[msg] {
      not formatting_first
      not no_before_init
      count(input.run.runtime_config.before_init) > 0
      first_command := input.run.runtime_config.before_init[0]
      count(input.reviews.current.approvals) == 0
      msg := concat("", ["The 'terraform fmt -check' command must run first in before_init hooks. Current first command: ", first_command])
    }

    # Allow DevOps lead to override in emergencies
    approve {
      not formatting_first
      not no_before_init
      input.reviews.current.approvals[_].session.teams[_] == "DevOps-Lead"
    }
    ```

### Use case 4: Branch naming conventions

**Scenario**: Enforce that feature branches follow a naming convention like `feature/*` or `fix/*`.

**Old initialization policy:**

=== "Rego v1"
    ```opa
    package spacelift

    deny contains sprintf("invalid feature branch name (%s)", [branch]) if {
      branch := input.commit.branch
      input.run.type == "PROPOSED"
      not re_match("^(fix|feature)\\/.*", branch)
    }
    ```

=== "Rego v0"
    ```opa
    package spacelift

    deny[sprintf("invalid feature branch name (%s)", [branch])] {
      branch := input.commit.branch
      input.run.type == "PROPOSED"
      not re_match("^(fix|feature)\\/.*", branch)
    }
    ```

**New approval policy:**

=== "Rego v1"
    ```opa
    package spacelift

    reject if {
      branch := input.run.commit.branch
      input.run.type == "PROPOSED"
      not re_match("^(fix|feature)\\/.*", branch)
    }

    approve if not reject
    ```

=== "Rego v0"
    ```opa
    package spacelift

    reject {
      branch := input.run.commit.branch
      input.run.type == "PROPOSED"
      not re_match("^(fix|feature)\\/.*", branch)
    }

    approve { not reject }
    ```

**Enhanced with approval policy features:**

Support ticket references and allow manual approval for hotfixes:

=== "Rego v1"
    ```opa
    package spacelift

    valid_branch_name if {
      branch := input.run.commit.branch
      input.run.type == "PROPOSED"
      re_match("^(fix|feature)\\/[A-Z]+-[0-9]+-.+", branch)  # e.g., feature/JIRA-123-add-widget
    }

    hotfix_branch if {
      branch := input.run.commit.branch
      input.run.type == "PROPOSED"
      re_match("^hotfix\\/.*", branch)
    }

    # Auto-approve valid branch names
    approve if valid_branch_name

    # Auto-approve tracked runs (not feature branches)
    approve if input.run.type != "PROPOSED"

    # Reject invalid branch names
    reject_with_note contains sprintf("Invalid branch name '%s'. Feature branches must follow format: 'feature/TICKET-123-description' or 'fix/TICKET-123-description'", [input.run.commit.branch]) if {
      input.run.type == "PROPOSED"
      not valid_branch_name
      not hotfix_branch
      count(input.reviews.current.approvals) == 0
    }

    # Allow hotfix branches with lead approval
    approve if {
      hotfix_branch
      some approval in input.reviews.current.approvals
      some team in approval.session.teams
      team == "Engineering-Lead"
    }
    ```

=== "Rego v0"
    ```opa
    package spacelift

    valid_branch_name {
      branch := input.run.commit.branch
      input.run.type == "PROPOSED"
      re_match("^(fix|feature)\\/[A-Z]+-[0-9]+-.+", branch)
    }

    hotfix_branch {
      branch := input.run.commit.branch
      input.run.type == "PROPOSED"
      re_match("^hotfix\\/.*", branch)
    }

    # Auto-approve valid branch names
    approve { valid_branch_name }

    # Auto-approve tracked runs (not feature branches)
    approve { input.run.type != "PROPOSED" }

    # Reject invalid branch names
    reject_with_note[sprintf("Invalid branch name '%s'. Feature branches must follow format: 'feature/TICKET-123-description' or 'fix/TICKET-123-description'", [input.run.commit.branch])] {
      input.run.type == "PROPOSED"
      not valid_branch_name
      not hotfix_branch
      count(input.reviews.current.approvals) == 0
    }

    # Allow hotfix branches with lead approval
    approve {
      hotfix_branch
      input.reviews.current.approvals[_].session.teams[_] == "Engineering-Lead"
    }
    ```

## Task policy migration

Task policies controlled which commands could be executed as [tasks](../../run/task.md), preventing dangerous operations or restricting access based on user roles.

### Use case 1: Command allowlisting

**Scenario**: Only allow non-admins to run safe commands like `terraform taint` and `terraform untaint`.

**Old task policy:**

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

**New approval policy:**

=== "Rego v1"
    ```opa
    package spacelift

    reject if {
      input.run.type == "TASK"
      command := input.run.command
      not input.run.creator_session.admin
      not regex.match("^terraform\\s(un)?taint\\s[\\w\\-\\.]*$", command)
    }

    approve if not reject
    ```

=== "Rego v0"
    ```opa
    package spacelift

    reject {
      input.run.type == "TASK"
      command := input.run.command
      not input.run.creator_session.admin
      not regex.match("^terraform\\s(un)?taint\\s[\\w\\-\\.]*$", command)
    }

    approve { not reject }
    ```

**Enhanced with approval policy features:**

Add a broader allowlist and require team lead approval for other commands:

=== "Rego v1"
    ```opa
    package spacelift

    # Always approve non-task runs
    approve if input.run.type != "TASK"

    # Admins can run any task
    approve if {
      input.run.type == "TASK"
      input.run.creator_session.admin
    }

    # Safe commands allowed for everyone
    safe_commands := [
      "^terraform\\s(un)?taint\\s[\\w\\-\\.]*$",
      "^terraform\\sstate\\slist$",
      "^terraform\\sstate\\sshow\\s[\\w\\-\\.]*$",
      "^terraform\\soutput$",
    ]

    safe_command if {
      input.run.type == "TASK"
      some pattern in safe_commands
      regex.match(pattern, input.run.command)
    }

    approve if safe_command

    # Require team lead approval for other commands
    reject_with_note contains sprintf("Command '%s' requires team lead approval", [input.run.command]) if {
      input.run.type == "TASK"
      not input.run.creator_session.admin
      not safe_command
      count(input.reviews.current.approvals) == 0
    }

    approve if {
      input.run.type == "TASK"
      not safe_command
      some approval in input.reviews.current.approvals
      some team in approval.session.teams
      team == "Team-Lead"
    }
    ```

=== "Rego v0"
    ```opa
    package spacelift

    # Always approve non-task runs
    approve { input.run.type != "TASK" }

    # Admins can run any task
    approve {
      input.run.type == "TASK"
      input.run.creator_session.admin
    }

    # Safe commands allowed for everyone
    safe_commands := [
      "^terraform\\s(un)?taint\\s[\\w\\-\\.]*$",
      "^terraform\\sstate\\slist$",
      "^terraform\\sstate\\sshow\\s[\\w\\-\\.]*$",
      "^terraform\\soutput$",
    ]

    safe_command {
      input.run.type == "TASK"
      regex.match(safe_commands[_], input.run.command)
    }

    approve { safe_command }

    # Require team lead approval for other commands
    reject_with_note[sprintf("Command '%s' requires team lead approval", [input.run.command])] {
      input.run.type == "TASK"
      not input.run.creator_session.admin
      not safe_command
      count(input.reviews.current.approvals) == 0
    }

    approve {
      input.run.type == "TASK"
      not safe_command
      input.reviews.current.approvals[_].session.teams[_] == "Team-Lead"
    }
    ```

### Use case 2: Time-based restrictions

**Scenario**: Prevent tasks from running on weekends.

**Old task policy:**

=== "Rego v1"
    ```opa
    package spacelift

    deny contains "no tasks on weekends" if {
      today := time.weekday(input.request.timestamp_ns)
      weekend := {"Saturday", "Sunday"}
      weekend[today]
    }
    ```

=== "Rego v0"
    ```opa
    package spacelift

    deny["no tasks on weekends"] {
      today := time.weekday(input.request.timestamp_ns)
      weekend := {"Saturday", "Sunday"}
      weekend[today]
    }
    ```

**New approval policy:**

=== "Rego v1"
    ```opa
    package spacelift

    reject if {
      input.run.type == "TASK"
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
      input.run.type == "TASK"
      today := time.weekday(input.run.created_at)
      weekend := {"Saturday", "Sunday"}
      weekend[today]
    }

    approve { not reject }
    ```

**Enhanced with approval policy features:**

Allow emergency tasks with proper approval:

=== "Rego v1"
    ```opa
    package spacelift

    # Always approve non-task runs
    approve if input.run.type != "TASK"

    is_weekend if {
      today := time.weekday(input.run.created_at)
      weekend := {"Saturday", "Sunday"}
      weekend[today]
    }

    is_business_hours if {
      hour := floor(time.clock([input.run.created_at, "America/New_York"])[0])
      hour >= 9
      hour < 17
      not is_weekend
    }

    # Auto-approve during business hours
    approve if {
      input.run.type == "TASK"
      is_business_hours
    }

    # Require on-call approval outside business hours
    reject_with_note contains "Tasks outside business hours require on-call engineer approval" if {
      input.run.type == "TASK"
      not is_business_hours
      count(input.reviews.current.approvals) == 0
    }

    approve if {
      input.run.type == "TASK"
      not is_business_hours
      some approval in input.reviews.current.approvals
      some team in approval.session.teams
      team == "On-Call"
    }
    ```

=== "Rego v0"
    ```opa
    package spacelift

    # Always approve non-task runs
    approve { input.run.type != "TASK" }

    is_weekend {
      today := time.weekday(input.run.created_at)
      weekend := {"Saturday", "Sunday"}
      weekend[today]
    }

    is_business_hours {
      hour := floor(time.clock([input.run.created_at, "America/New_York"])[0])
      hour >= 9
      hour < 17
      not is_weekend
    }

    # Auto-approve during business hours
    approve {
      input.run.type == "TASK"
      is_business_hours
    }

    # Require on-call approval outside business hours
    reject_with_note["Tasks outside business hours require on-call engineer approval"] {
      input.run.type == "TASK"
      not is_business_hours
      count(input.reviews.current.approvals) == 0
    }

    approve {
      input.run.type == "TASK"
      not is_business_hours
      input.reviews.current.approvals[_].session.teams[_] == "On-Call"
    }
    ```

### Use case 3: Command validation by resource criticality

**Scenario**: Allow simple state operations on all resources, but require approval for changes to critical infrastructure.

**Old task policy (limited approach):**

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

**New approval policy (enhanced approach):**

=== "Rego v1"
    ```opa
    package spacelift

    # Always approve non-task runs
    approve if input.run.type != "TASK"

    # Critical resources that need extra protection
    critical_resources := [
      "^aws_db_instance\\.",
      "^aws_rds_cluster\\.",
      "^aws_security_group\\.main",
      "^aws_iam_role\\.admin",
    ]

    affects_critical_resource if {
      some pattern in critical_resources
      regex.match(pattern, input.run.command)
    }

    # Read-only commands allowed for everyone
    readonly_commands := [
      "^terraform\\sstate\\slist",
      "^terraform\\sstate\\sshow\\s",
      "^terraform\\soutput",
    ]

    is_readonly if {
      some pattern in readonly_commands
      regex.match(pattern, input.run.command)
    }

    # Auto-approve read-only commands
    approve if {
      input.run.type == "TASK"
      is_readonly
    }

    # Auto-approve non-critical resource changes
    approve if {
      input.run.type == "TASK"
      not is_readonly
      not affects_critical_resource
    }

    # Require Infrastructure team approval for critical resources
    reject_with_note contains sprintf("Command '%s' affects critical infrastructure and requires Infrastructure team approval", [input.run.command]) if {
      input.run.type == "TASK"
      affects_critical_resource
      count(input.reviews.current.approvals) == 0
    }

    approve if {
      input.run.type == "TASK"
      affects_critical_resource
      some approval in input.reviews.current.approvals
      some team in approval.session.teams
      team == "Infrastructure"
    }
    ```

=== "Rego v0"
    ```opa
    package spacelift

    # Always approve non-task runs
    approve { input.run.type != "TASK" }

    # Critical resources that need extra protection
    critical_resources := [
      "^aws_db_instance\\.",
      "^aws_rds_cluster\\.",
      "^aws_security_group\\.main",
      "^aws_iam_role\\.admin",
    ]

    affects_critical_resource {
      regex.match(critical_resources[_], input.run.command)
    }

    # Read-only commands allowed for everyone
    readonly_commands := [
      "^terraform\\sstate\\slist",
      "^terraform\\sstate\\sshow\\s",
      "^terraform\\soutput",
    ]

    is_readonly { regex.match(readonly_commands[_], input.run.command) }

    # Auto-approve read-only commands
    approve {
      input.run.type == "TASK"
      is_readonly
    }

    # Auto-approve non-critical resource changes
    approve {
      input.run.type == "TASK"
      not is_readonly
      not affects_critical_resource
    }

    # Require Infrastructure team approval for critical resources
    reject_with_note[sprintf("Command '%s' affects critical infrastructure and requires Infrastructure team approval", [input.run.command])] {
      input.run.type == "TASK"
      affects_critical_resource
      count(input.reviews.current.approvals) == 0
    }

    approve {
      input.run.type == "TASK"
      affects_critical_resource
      input.reviews.current.approvals[_].session.teams[_] == "Infrastructure"
    }
    ```

## Combined patterns

One of the most powerful features of approval policies is the ability to handle both runs and tasks in a single policy, with unified approval logic.

### Unified approval workflow

This policy combines initialization and task policy concerns with a consistent approval workflow:

=== "Rego v1"
    ```opa
    package spacelift

    # ===================
    # Run Protection Rules
    # ===================

    # Dangerous before_init commands
    dangerous_before_init if {
      some command in input.run.runtime_config.before_init
      contains(command, "terraform destroy")
    }

    # Unapproved runner images
    approved_images := {
      "spacelift/runner:latest",
      "spacelift/runner:stable",
      "my-org/custom-runner:v1.0.0",
    }

    unapproved_image if {
      not input.run.runtime_config.runner_image in approved_images
    }

    # ===================
    # Task Protection Rules
    # ===================

    # Destructive commands
    destructive_task if {
      input.run.type == "TASK"
      destructive_patterns := [
        "terraform\\sdestroy",
        "terraform\\sstate\\srm",
        "rm\\s-rf",
      ]
      some pattern in destructive_patterns
      regex.match(pattern, input.run.command)
    }

    # ===================
    # Approval Logic
    # ===================

    # Auto-approve safe operations
    approve if {
      not dangerous_before_init
      not unapproved_image
      not destructive_task
    }

    # For dangerous operations, require:
    # - 2 approvals AND
    # - At least one approval from Infrastructure team AND
    # - No rejections
    approve if {
      or([dangerous_before_init, unapproved_image, destructive_task])
      count(input.reviews.current.approvals) >= 2
      count(input.reviews.current.rejections) == 0
      some approval in input.reviews.current.approvals
      some team in approval.session.teams
      team == "Infrastructure"
    }

    # Provide clear rejection feedback
    reject_with_note contains "Dangerous before_init command detected. Requires 2 approvals including Infrastructure team." if {
      dangerous_before_init
      count(input.reviews.current.approvals) < 2
    }

    reject_with_note contains sprintf("Unapproved runner image '%s'. Requires 2 approvals including Infrastructure team.", [input.run.runtime_config.runner_image]) if {
      unapproved_image
      count(input.reviews.current.approvals) < 2
    }

    reject_with_note contains sprintf("Destructive task command '%s'. Requires 2 approvals including Infrastructure team.", [input.run.command]) if {
      destructive_task
      count(input.reviews.current.approvals) < 2
    }
    ```

=== "Rego v0"
    ```opa
    package spacelift

    # ===================
    # Run Protection Rules
    # ===================

    # Dangerous before_init commands
    dangerous_before_init {
      command := input.run.runtime_config.before_init[_]
      contains(command, "terraform destroy")
    }

    # Unapproved runner images
    approved_images := {
      "spacelift/runner:latest",
      "spacelift/runner:stable",
      "my-org/custom-runner:v1.0.0",
    }

    unapproved_image { not approved_images[input.run.runtime_config.runner_image] }

    # ===================
    # Task Protection Rules
    # ===================

    # Destructive commands
    destructive_task {
      input.run.type == "TASK"
      destructive_patterns := [
        "terraform\\sdestroy",
        "terraform\\sstate\\srm",
        "rm\\s-rf",
      ]
      regex.match(destructive_patterns[_], input.run.command)
    }

    # ===================
    # Approval Logic
    # ===================

    # Auto-approve safe operations
    approve {
      not dangerous_before_init
      not unapproved_image
      not destructive_task
    }

    # For dangerous operations, require:
    # - 2 approvals AND
    # - At least one approval from Infrastructure team AND
    # - No rejections
    approve {
      count(input.reviews.current.approvals) >= 2
      count(input.reviews.current.rejections) == 0
      input.reviews.current.approvals[_].session.teams[_] == "Infrastructure"
    }

    # Provide clear rejection feedback
    reject_with_note["Dangerous before_init command detected. Requires 2 approvals including Infrastructure team."] {
      dangerous_before_init
      count(input.reviews.current.approvals) < 2
    }

    reject_with_note[sprintf("Unapproved runner image '%s'. Requires 2 approvals including Infrastructure team.", [input.run.runtime_config.runner_image])] {
      unapproved_image
      count(input.reviews.current.approvals) < 2
    }

    reject_with_note[sprintf("Destructive task command '%s'. Requires 2 approvals including Infrastructure team.", [input.run.command])] {
      destructive_task
      count(input.reviews.current.approvals) < 2
    }
    ```

## Migration checklist

Use this checklist when migrating your policies:

- **Identify all initialization and task policies** attached to your stacks
- **For each policy:**
    - Review the use case and requirements
    - Convert `deny` rules to `reject` rules
    - Add `approve if not reject` rule
    - Update data input references (see [Data input differences](#data-input-differences))
    - Consider enhancements:
        - Add descriptive feedback with `reject_with_note` and `approve_with_note`
        - Add manual approval workflows for exceptions
        - Add role-based approval requirements
        - Combine related policies into a unified approval policy
    - Test the new policy using the [policy workbench](./README.md#policy-workbench)
    - Use the `sample` rule to capture real evaluation data
- **Deploy the new approval policy**
    - Attach to the same stacks as the old policy
    - Monitor initial runs to ensure correct behavior
- **Remove old policies** once the new approval policy is validated
- **Update documentation** for your team about the new approval workflows

## Testing your migration

Use Spacelift's [policy workbench](./README.md#policy-workbench) to test your new approval policies before deploying them:

1. Add a `sample` rule to your approval policy to capture evaluations:

    === "Rego v1"
        ```opa
        sample if true  # Capture all evaluations
        ```

    === "Rego v0"
        ```opa
        sample { true }  # Capture all evaluations
        ```

2. Attach the policy to a test stack
3. Trigger a test run or task
4. Open the policy workbench and review the captured input
5. Adjust your policy logic as needed
6. Simulate with different inputs to verify behavior
7. Remove or refine the `sample` rule before production deployment

## Getting help

If you need assistance with your migration:

- Review the [approval policy documentation](../approval-policy.md) for detailed information.
- Check the [policy examples library](https://github.com/spacelift-io/spacelift-policies-example-library){: rel="nofollow"}.
- Use the [policy workbench](./README.md#policy-workbench) to test and debug policies.
- Contact [Spacelift support](../../../product/support/README.md#contact-support) for custom policy assistance.
