# Scheduling

## What is scheduling?

{% if is_saas() %}
!!! Info
    This feature is only available on the Business plan and above. Please check out our [pricing page](https://spacelift.io/pricing){: rel="nofollow"} for more information.
{% endif %}

Scheduling allows you to trigger a stack deletion or task at a specific time or periodically based on the cron rules defined.

![](../../assets/screenshots/stack/scheduling/page-view.png)

## Scheduled Delete Stack (TTL)

A Delete Stack schedule allows you to delete the stack and (optionally) its resources at the specific timestamp (UNIX timestamp).

Add a schedule with the Delete Stack type from the Scheduling section of your stack.

Actions when the schedule defines that the resources should be deleted:

- a destruction run will be triggered at the specified time.
- after this run is successful, the stack will be deleted.

When the resources should not be deleted, we will delete the stack at the specified time.

![](../../assets/screenshots/stack/scheduling/create-delete-stack.png)

## Scheduled Task

A scheduled task enables you to run a command at a specific timestamp or periodically based on the cron rules defined.

Add a schedule with the Task type from the Scheduling section of your stack.
After creating this schedule, a task will be triggered with the defined command (at a specific timestamp or periodically based on the cron rules defined).

![](../../assets/screenshots/stack/scheduling/create-task.png)

## Scheduled Run

You can also set up a schedule based on which a tracked run will be created.

![](../../assets/screenshots/stack/scheduling/create-run.png)

Additionally, if you mark **Attach custom runtime config**, you will be able to attach a custom runtime config to the schedule, similarly to when [triggering a run with custom runtime config](../run/tracked.md#triggering-runs-with-a-custom-runtime-config).
