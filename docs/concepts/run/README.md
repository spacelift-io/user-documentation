# Run

Every job that can touch your Spacelift-managed infrastructure is called a run. There are four main types of runs, and three of them are children of [stacks](../stack/README.md):

- [Task](./task.md): A freeform command you can execute on your infrastructure.
- [Proposed run](./proposed.md): Serves as a preview of introduced changes.
- [Tracked run](./tracked.md): A form of deployment.
- [Module test case](./test-case.md): Executed on an OpenTofu/Terraform module, rather than in Spacelift. Similar to a tracked run.

## Execution model

Runs are executed on a worker node inside a Docker container. Spacelift maintains a number of these worker nodes (called the [public worker pool](../worker-pools/README.md#public-worker-pool)) that are available to all customers, but individual customers are allowed to run our agent on their end, for their exclusive use.

Each Spacelift run involves a handover between _spacelift.io_ and the worker node (the public or private worker pool). After the handover, the worker node is fully responsible for running the job and communicating the results of the job back to _spacelift.io_.

!!! info
    Your worker node (public or private) executes the run and accesses your infrastrucutre, not _spacelift.io_.

## Common run states

Regardless of the type of the job performed, some phases and terminal states are common.

### Queued

Queued is a **passive state**, meaning no operations are performed. Queued runs are not [ready](#ready) for processing, either blocked, waiting for dependencies to finish, or requiring additional action from a user.

Spacelift serializes all state-changing operations to the stack. Both tracked runs and tasks can change the state, so each of them gets an exclusive lock on the stack, blocking other runs from starting.

If your run or task is currently blocked by another run holding a lock on the stack, you'll see a link to the blocker in the run state list:

![Blocker in Spacelift run state list](<../../assets/screenshots/run/blocked-run.png>)

If your queued run isn't blocked by another run and isn't being promoted to the ready state, it could need:

- Approval
- Dependent stacks to finish
- External dependencies to finish

The user can discard a run while it's still queued, transitioning it to the terminal [discarded](#discarded) state.

### Ready

Ready is a **passive state**, meaning no operations are performed. Ready runs are eligible for processing and are waiting for a worker to become available. A run will stay in this state until it's picked up by a worker.

When a worker is available, the state will automatically transition to [preparing](#preparing). The user can discard a run even if it's _ready_, transitioning it to the terminal [discarded](#discarded) state.

### Discarded

Discarded is a **passive state**, meaning no operations are performed. Discarded runs occur when the user manually stops a [queued](#queued) run or task before it can be picked up by the worker.

This is also a **terminal state** meaning that no further state can follow it. Runs that are discarded can't be moved to a different state.

### Preparing

Runs in the preparing state are eligible for processing (not being blocked or awaiting approvals) **and** worker nodes are ready to process them. The preparing state is when the handover and dialog between _spacelift.io_ and the worker happens, for example:

![Run handover](<../../assets/screenshots/run/handover.png>)

Ground Control refers to the bit directly controlled by Spacelift, when we ensure the worker node gets everything required to perform the job, and that the node can take over the execution.

Once the worker is able to pull the Docker image and use it to start the container, the preparing phase is over and the [initialization](#initializing) phase begins. If the process fails for whatever reason, the run is marked as [failed](#failed).

### Initializing

The _initialization_ phase is handled exclusively by the worker and involves running [pre-initialization hooks](../stack/stack-settings.md#customizing-workflow) and vendor-specific initialization processes. For Terraform stacks, it would mean running `terraform init` in the right directory and with the right parameters.

Pre-initialization hooks and the rest of the initialization process all run in the same shell session, so environment variables exported by pre-initialization hooks are accessible to the vendor-specific initialization process. This is often the desired outcome when working with external secret managers like HashiCorp Vault.

If this phase fails, the run is marked as [failed](#failed). Otherwise, the next step is determined by the type of the run being executed.

### Failed

Failed is a **passive state**, meaning no operations are performed. It's also a **terminal state**, so no further state can follow it.

If a run transitions into the _failed_ state, something went wrong. In most cases the issue will be something related to your project like:

- Errors in the source code.
- [Pre-initialization checks](../stack/stack-settings.md#customizing-workflow) failing.
- [Plan policies](../policy/terraform-plan-policy.md) rejecting your change.
- Deployment-time errors.

In rare cases, errors in the Spacelift application code or third party dependencies can also make the job fail. These cases are clearly marked by a notice corresponding to the failure mode, reported through our exception tracker and immediately investigated.

### Stopped

Stopped is a **passive state**, meaning no operations are performed. It's also a **terminal state**, so no further state can follow it.

Some types of runs can be interrupted. You can send a stop signal from the GUI and/or API to the run, which is then passed to the worker handling the job. The worker decides whether to handle or ignore the stop signal.

The stopped state indicates that a run has been stopped while [initializing](#initializing) or [planning](./proposed.md#planning), either manually by the user or by Spacelift (for proposed changes). Proposed changes will automatically be stopped when a newer version of the code is pushed to their branch to limit the number of unnecessary API calls to your resource providers.

Here's an example of a run manually stopped while [initializing](#initializing):

![Stopped run example](<../../assets/screenshots/run/stopped-run.png>)

### Finished

Finished is a **passive state**, meaning no operations are performed. It's also a **terminal state**, so no further state can follow it.

Finished runs were executed successfully, though the success criteria will depend on the type of run.

### Full list of potential run states

| State | Description | Terminal? | Passive? |
| ----- | ----------- | --------- | -------- |
| `NONE` | Stack is created but no initial runs have been triggered. Not offically a run state but is listed in the UI for informational purposes. | ❌ | ❌ |
| `QUEUED` | Queued, waiting for an available worker or for the stack lock to be released by another run. | ❌ | ✅ |
| `CANCELED` | Canceled by the user. | ✅ | ✅ |
| `INITIALIZING` | Run's workspace is currently initializing on the worker. | ❌ | ✅ |
| `PLANNING` | Worker is planning the run. | ❌ | ✅ |
| `FAILED` | Run failed. | ✅ | ✅ |
| `FINISHED` | Finished successfully. | ✅ | ✅ |
| `UNCONFIRMED` | Planned successfully, but run reports changes. Waiting for the user to review. | ❌ | ❌ |
| `DISCARDED` | Run's plan rejected by the user. | ✅ | ✅ |
| `CONFIRMED` | Run's plan confirmed by the user. Waiting for the worker to start processing. | ❌ | ❌ |
| `APPLYING` | Applying the run's changes. | ❌ | ❌ |
| `PERFORMING` | Performing the task requested by the user. | ❌ | ❌ |
| `STOPPED` | Stopped by the user. | ✅ | ✅ |
| `DESTROYING` | Worker performing a destroy operation on the managed resources. | ❌ | ❌ |
| `PREPARING` | Workspace being prepared for the run. | ❌ | ✅ |
| `PREPARING_APPLY` | Workspace being prepared for the change deployment. | ❌ | ✅ |
| `SKIPPED` | Run was skipped. | ✅ | ✅ |
| `REPLAN_REQUESTED` | Pending a replan and should get picked up by the scheduler. | ❌ | ❌ |
| `PENDING` | Deprecated state. | ❌ | ✅ |
| `READY` | Ready to start. | ❌ | ✅ |
| `PENDING_REVIEW` | Proposed run is waiting for post-planning approval policy sign-off. | ❌ | ❌ |

## Log retention

{% if is_saas() %}

Run logs are kept for a configurable retention period. By default, all accounts have a retention period of **60 days**.

### View current retention period

You can view your current run logs retention period in the Spacelift UI. Hover over your name in the bottom left, click **Organization Settings**, then click **Limits**.

### Customizable retention periods

The log retention period can be one of the following:

- 60 days (default)
- 90 days
- 180 days
- 365 days
- 730 days

To modify the retention period settings for your account, contact your customer representative.

### Important considerations

Changing the retention period will not retroactively apply to existing runs. The new retention period will only take effect for runs created **after** the change has been made. Previously created runs will continue to follow the retention period that was active when they were created.

{% else %}

Run logs are kept for a configurable retention period. By default, run logs have a retention period of **60 days**. If you need to customize the log retention period, configure a [custom S3 bucket configuration for the run logs](https://github.com/spacelift-io/terraform-aws-spacelift-selfhosted?tab=readme-ov-file#deploy-with-custom-s3-bucket-retention).

{% endif %}

## Run prioritization

Runs have different priorities based on their type.

The highest priority is assigned to blocking runs (tracked runs, destroy runs, and tasks), followed by proposed runs, and then drift detection runs. Runs of the same type are processed in the order they were created, oldest first.

You can automatically prioritize runs using a [push policy](../policy/push-policy/README.md#prioritization). We only recommend automatic prioritization in special circumstances. For most users, the default prioritization (tracked runs, then proposed runs, then drift detection runs) provides an optimal user experience.

You can manually prioritize a run while it's in a [non-terminal state](#common-run-states) if a private worker pool is processing the run. Spacelift will process prioritized runs before runs from other stacks. However, a stack's standard execution order of run types (tasks, tracked, and proposed runs) will be respected.

The priority of a run can be changed from the run's view and in the worker pool queue view.

### Run view

1. In the Spacelift UI, navigate to **Ship Infra** > **Stacks**.
2. Click on the name of the stack whose run you will prioritize.
3. In the _Tracked runs_ tab, click the name of the run to prioritize.
4. If you are using a private worker pool **and** the run is in a non-terminal state, click **Prioritize**.

![Prioritize run in run view](<../../assets/screenshots/run/prioritize-from-run-view.png>)

### Worker pool queue view

1. In the Spacelift UI, navigate to **Manage Organization** > **Worker Pools**.
2. Click the name of the worker pool assigned to the run.
3. Click **Queue**.
4. Next to the run you will prioritize, click the **three dots**, then click **Prioritize**.

![Prioritize run in worker pool queue](<../../assets/screenshots/run/prioritize-from-worker-pool-view.png>)

## Limit runs

You can limit the number of runs being created for a VCS event.

1. Hover over your name in the bottom left, click **Organization Settings**, then click **Limits**.
2. **Turn on** the _Limit of runs created for a VCS event_ toggle.
3. Use the slider or enter a number in the box to set the maximum number of runs triggered by a VCS event for your account.

![Limit number of runs](<../../assets/screenshots/run/limit-runs.png>)

You can set a maximum number of up to 500 runs.

If the number of runs that are going to be triggered exceeds the limit set in Spacelift, you will be able to see this as the reason for failure in your VCS provider.

## Run verification

For your most sensitive stacks, you can add additional verification of runs based on [arbitrary metadata](./user-provided-metadata.md) you provide to runs when creating or confirming them. This works for any kind of run, including tasks.

1. Metadata is passed to the created or confirmed run through the [API](../../integrations/api.md) or the [spacectl CLI](../spacectl.md).
2. Every time this interaction happens, add a new piece of metadata, which will form a list of metadata blobs inside the run.
3. The metadata blobs are available in policies, including the private-worker side initialization policy.

Using additional verification allows you to sign the runs when you confirm them and later verify this signature inside of the private worker, through the initialization policy. There you can use the `exec` function, which runs an arbitrary binary inside of the Docker image. This binary verifies that the content of the run and signature match and that the signature is a proper signature of somebody from your company.
