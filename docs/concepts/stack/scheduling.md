# Scheduling stack actions

{% if is_saas() %}
!!! Info
    This feature is only available on the Business plan and above. Please check out our [pricing page](https://spacelift.io/pricing){: rel="nofollow"} for more information.
{% endif %}

If you are using [private workers](../../concepts/worker-pools/README.md#private-worker-pool), you can schedule stack deletion or other tasks at a specific time or periodically based on cron rules you define. If your stack is using public workers, you can still create the schedules, but they **will not trigger** until the stack is using private workers.

![Scheduling tab](<../../assets/screenshots/stack/scheduling/page-view.png>)

## Schedule stack deletion

You can schedule when a stack should be deleted (and, optionally, its resources).

1. Click the stack you would like to delete.
2. Click **Create schedule**, then **Stack deletion**.
3. Select a date and time for deletion, either in your local timezone or UTC.
4. Choose whether Spacelift retains or deletes the stack's resources.
5. Click **Create**.

If you chose to delete the stack's resources, a destruction run will trigger on the stack at the specified time, and then the stack will be deleted when that is successful. If you chose to keep the stack's resources, the stack will be deleted at the specified time.

![Schedule stack deletion](<../../assets/screenshots/stack/scheduling/create-delete-stack.png>)

## Schedule drift detection

You can schedule [drift detection](./drift-detection.md) on your stack to find differences between the desired and actual states of your infrastructure.

1. Click the stack you would like to check for drift.
2. Click **Create schedule**, then **Drift detectionn**.
3. Set the cron expression(s) for how often you'd like to perform drift detection.
4. Select the desired _timezone_.
5. Select additional options:
      1. **Reconcile**: Enable Spacelift to automatically create and trigger [reconciliation runs](./drift-detection.md#to-reconcile-or-not-to-reconcile) to resolve drift.
      2. **Ignore state**: Enable to allow Spacelift to perform drift detection on stacks regardless of state. If disabled, drift detection will only run on stacks with the _Finished_ state.
6. Click **Create**.

![Schedule drift detection](<../../assets/screenshots//stack/scheduling/schedule-drift-detection.png>)

## Schedule task

You can schedule tasks to run commands on a stack at a specified timestamp or periodically based on cron rules you define.

1. Click the stack you would like to schedule a task on.
2. Click **Create schedule**, then **Task**.
3. Enter the task command you would like to run.
4. Choose a specific date and time, or set a cron rule for recurring tasks.
5. Select the desired _timezone_.
6. Click **Create**.

![Schedule task](<../../assets/screenshots/stack/scheduling/create-task.png>)

## Schedule run

You can also set up a schedule based on when a tracked run will be created.

1. Click the stack you would like to schedule a run on.
2. Click **Create schedule**, then **Run**.
3. (Optionally) Enter a name for the run schedule.
4. **Attach custom runtime config**: Click the slider to enable this setting, then enter a [custom runtime config](../run//tracked.md#triggering-runs-with-a-custom-runtime-config).
5. Choose a specific date and time, or set a cron rule for recurring tasks.
6. Select the desired _timezone_.
7. Click **Create**.

![Schedule run](<../../assets/screenshots/stack/scheduling/create-run.png>)
