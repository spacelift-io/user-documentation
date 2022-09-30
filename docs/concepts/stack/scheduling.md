# Scheduling

!!! info
    Scheduling is currently in beta. If you are interested in trying out this feature reach out to us through our support channel or slack.

## What is scheduling?

Scheduling allows you to trigger a stack deletion or task at a specific time or periodically based on the cron rules defined.

The terraform provider and the API are (currently) the only ways to create scheduling configurations. We will add the UI for this feature in the upcoming weeks.

## Scheduled Delete Stack (TTL)

!!! info
    Note that, at least currently, scheduling only works on private workers.

A delete stack schedule allows you to delete the stack and (optionally) its resources at the specific timestamp (UNIX timestamp).

```
resource "spacelift_stack" "k8s-core" {
  // ...
}

resource "spacelift_scheduled_task" "k8s-core-delete" {
  stack_id = spacelift_stack.k8s-core.id

  at               = "1663336895"
  delete_resources = true
}
```

## Scheduled Tasks

!!! info
    Note that, at least currently, scheduling only works on private workers.

A scheduled task enables you to run a command at a specific timestamp or periodically based on the cron rules defined.

The following example shows that you can destroy and create resources at the beginning and the end of the workday.

```
// create the resources of a stack on a given schedule
resource "spacelift_scheduled_task" "k8s-core-create" {
  stack_id = spacelift_stack.k8s-core.id

  command = "terraform apply -auto-approve"
  every = ["0 7 * * 1-5"]
  timezone = "CET"
}

// destroy the resources of a stack on a given schedule
resource "spacelift_scheduled_task" "k8s-core-destroy" {
  stack_id = spacelift_stack.k8s-core.id

  command = "terraform destroy -auto-approve"
  every = ["0 21 * * 1-5"]
  timezone = "CET"
}
```