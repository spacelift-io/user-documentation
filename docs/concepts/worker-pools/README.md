---
description: >-
  This article explains how you can set up and use worker pools.
---

# Worker pools

{% if is_saas() %}
!!! Info
    This feature is only available on the Starter+ plan and above. Please check out our [pricing page](https://spacelift.io/pricing){: rel="nofollow"} for more information.

By default, Spacelift uses a public worker pool hosted and operated by us. While this works for many users, you may have special requirements regarding infrastructure, security, or compliance that aren't served by the public worker pool. Spacelift also supports private worker pools, which you can use to host the workers that execute Spacelift workflows on your end.

To enjoy the maximum level of flexibility and security with a private worker pool, temporary run state is encrypted end-to-end, so only the workers in your worker pool can look inside it. We use asymmetric encryption to achieve this and only you have access to the private key.
{% endif %}

!!! tip
    A worker is a logical entity that processes a single [run](../run/README.md) at a time. As a result, your number of workers is equal to your maximum concurrency.

    Typically, a virtual server (AWS EC2 or Azure/GCP VM) hosts a single worker to keep things simple and avoid coordination and resource management overhead.

    Containerized workers can share the same virtual server because the management is handled by the orchestrator.

## Shared responsibility model

Spacelift shares the responsibility for overall worker maintenance with you. How you use public and private workers depends on the level of configuration your organization needs and the level of responsibility you can take on. There are some worker permissions you can only manage with [private workers](#private-worker-pool).

In your infrastructure, responsibility is broken down into chunks:

![Shared responsibility model](<../../assets/screenshots/worker-pools-shared-responsibility-models.png>)

### Public vs private worker comparison

Private workers offer more customization options, but your organization is responsible for maintaining them by configuring compute resources, network access rules, and worker updates. With public workers, maintenance falls on Spacelift's side.

| Private workers | Public workers |
| --------------- | -------------- |
| Offer more customization but require more responsibility from client | Offer less customization but require less responsibility |
| Deployed in client infrastructure | Deployed in Spacelift's infrastructure |
| Assumes client's cloud provider IAM role | Needs trust relations between Spacelift's cloud provider and client's |
| All actions taken from client's infrastructure | All actions taken from Spacelift's infrastructure |
| Private or public Docker repository | Only public Docker repository |

## Setting up

### 1. Generate worker private key

We use asymmetric encryption to ensure that any temporary run state can only be accessed by workers in a given worker pool. To support this, you need to:

1. Generate a private key that can be used for this purpose.
2. Use the private key to create a certificate signing request (CSR) to give to Spacelift.

Spacelift will generate a certificate for you so workers can authenticate with the Spacelift backend. The following command will generate the key and CSR:

```bash
openssl req -new -newkey rsa:4096 -nodes -keyout spacelift.key -out spacelift.csr
```

!!! warning "Store your private key"
    Save your `spacelift.key` file (private key) in a secure location. You’ll need it when launching workers in your worker pool.

You can set up your worker pool from the Spacelift UI on the _Manage Organization_ > _Worker Pools_ tab. You can also create it programmatically using the `spacelift_worker_pool` resource type within the [Spacelift Terraform provider](../../vendors/terraform/terraform-provider.md).

### 2. Add worker pool entity

1. Navigate to _Manage Organization_ > _Worker Pools_.
2. Click **Create worker pool**.
3. Enter worker pool details:
        ![Upload the certificate you generated previously and create a worker pool](<../../assets/screenshots/worker_pools_create.png>)
      - **Name**: Enter a unique, descriptive name for your worker pool.
      - **Certificate**: Drag and drop or browse and upload the `spacelift.csr` file you generated.
      - **Space**: Select the space to create the worker pool in.
      - **Description** (optional): Enter a (markdown-supported) description of the worker pool.
      - **Configure drift detection run limits**: Enable to either disable drift detection entirely or set a limit on concurrent drift detection runs that can execute on the worker pool.
        ![Configure drift detection run limits](<../../assets/screenshots/config-drift-detection-run-limits.png>)
      - **Labels**: Add labels to help sort and filter your worker pools.
4. Click **Create**.

When the worker pool is created, you'll receive a base64-encoded **Spacelift worker pool token** containing configuration for your worker pool launchers and the certificate generated from the CSR.

!!! warning "Store your worker pool token"
    Save your **Spacelift token** in a secure location. You'll need it when launching the worker pool.

### 3. Launch worker pool

You can run workers using Docker or inside a Kubernetes cluster:

- Set up [Docker-based workers](docker-based-workers.md).
- Set up [Kubernetes workers](kubernetes-workers.md).

## Configuration options

A number of configuration variables are available to customize how your worker pool launcher behaves. Some are shared and some are [specific to Docker-based workers](#docker-only-options).

### Shared options

| Configuration variable | Details |
| ---------------------- | ------- |
| `SPACELIFT_MASK_ENVS` | Comma-delimited list of allowlisted environment variables that are passed to the workers but should never appear in the logs. |
| `SPACELIFT_SENSITIVE_OUTPUT_UPLOAD_ENABLED` | If set to `true`, the launcher will upload sensitive run outputs to the Spacelift backend. Required if you want to use sensitive outputs for [stack dependencies](../stack/stack-dependencies.md). |
| `SPACELIFT_RUN_LOGS_ON_STANDARD_OUTPUT_ENABLED` | If set to `true`, the launcher will write run logs to standard output in the same structured format as the rest of the logs. Some useful fields are `run_ulid`, `stack_id`, `ts`, and `msg`. You can easily manage run logs and ship them anywhere you want. |
| `SPACELIFT_LAUNCHER_RUN_INITIALIZATION_POLICY` | File that contains the run initialization policy that will be parsed/used. If the run initialized policy cannot be validated at startup, the worker pool will exit with an appropriate error. See the [Kubernetes-specific configuration](#kubernetes-specific-configuration) section for more information. |
| `SPACELIFT_LAUNCHER_LOGS_TIMEOUT` | Custom timeout (the default is _7 minutes_) for killing jobs not producing any logs. This is a duration flag, expecting a duration-formatted value, e.g. `1000s`. See the [Kubernetes-specific configuration](#kubernetes-specific-configuration) section for more information. |
| `SPACELIFT_LAUNCHER_RUN_TIMEOUT` | Custom maximum run time (default is _70 minutes_). This is a duration flag, expecting a duration-formatted value, e.g. `120m`. See the [Kubernetes-specific configuration](#kubernetes-specific-configuration) section for more information. |
| `SPACELIFT_DEBUG` | If set to `true`, this will output the exact commands Spacelift runs to the worker logs. |

!!! warning
    [Server-side initialization policies](../../concepts/policy/deprecated/run-initialization-policy.md) are being deprecated. In comparisin, this policy is a worker-side initialization policy and can be set by using the `SPACELIFT_LAUNCHER_RUN_INITIALIZATION_POLICY` flag.

    For a limited time, Spacelift will be running both types of initialization policy checks. We're planning to move the pre-flight checks to the worker node, thus allowing customers to block suspicious looking jobs on their end.

### Docker-only options

| Configuration variable | Details |
| ---------------------- | ------- |
| `SPACELIFT_DOCKER_CONFIG_DIR` | If set, the value of this variable will point to the directory containing Docker configuration, which includes credentials for private Docker registries. Private workers can populate this directory by executing `docker login` before the launcher process is started. |
| `SPACELIFT_WHITELIST_ENVS` | Comma-delimited list of environment variables to pass from the launcher's environment to the workers' environment. They can be prefixed with `ro_` to only be included in read-only runs or `wo_` to only be included in write-only runs. |
| `SPACELIFT_WORKER_EXTRA_MOUNTS` | Additional files or directories to be mounted to the launched worker Docker containers during **either read or write runs**, as a comma-separated list of mounts in the form of `/host/path:/container/path`. |
| `SPACELIFT_WORKER_NETWORK` | Network ID/name to connect the launched worker containers. Defaults to `bridge`. |
| `SPACELIFT_WORKER_RUNTIME` | Runtime to use for worker container. |
| `SPACELIFT_WORKER_RO_EXTRA_MOUNTS` | Additional directories to be mounted to the worker Docker container during **read-only runs**, as a comma separated list of mounts in the form of `/host/path:/container/path`. |
| `SPACELIFT_WORKER_WO_EXTRA_MOUNTS` | Additional directories to be mounted to the worker Docker container during **write-only runs**, as a comma separated list of mounts in the form of `/host/path:/container/path`. |
| `SPACELIFT_DEFAULT_RUNNER_IMAGE` | If set, this will override the default runner image used for non-Ansible runs. The default is `public.ecr.aws/spacelift/runner-terraform:latest`. This will not override a custom runner image on a stack and will only take effect if no custom image is set. |
| `SPACELIFT_DEFAULT_ANSIBLE_RUNNER_IMAGE` | If set, this will override the default runner image used for Ansible runs. The default is `public.ecr.aws/spacelift/runner-ansible:latest`. This will not override a custom runner image on a stack and will only take effect if no custom image is set. |

### Kubernetes-specific configuration

There is more detailed information available in the Kubernetes workers documentation for certain configuration options:

- Set up [initialization policies](./kubernetes-workers.md#initialization-policies).
- Configure [timeouts](./kubernetes-workers.md#timeouts).

### Passing metadata tags

Passing custom metadata tags is currently only supported for [Docker-based workers](./docker-based-workers.md). Kubernetes workers send through some metadata, including the name of the Worker resource in Kubernetes along with the version of the controller used to create the worker, but do not support user-provided custom metadata.

When the launcher from a worker pool is registering with the mothership, you can send along some tags that will allow you to uniquely identify the process/machine for the purpose of draining or debugging. Any environment variables using `SPACELIFT_METADATA_` prefix will be passed on. For example, if you're running Spacelift workers in EC2, you can do the following just before you execute the launcher binary:

```bash
export SPACELIFT_METADATA_instance_id=$(ec2-metadata --instance-id | cut -d ' ' -f2)
```

This will set your EC2 instance ID as `instance_id` tag in your worker.

{% if is_self_hosted() %}
See [injecting custom commands during instance startup](./docker-based-workers.md#injecting-custom-commands-during-instance-startup) for information about how to do this when using our CloudFormation template.
{% endif %}

{% if is_saas() %}

### Provider caching

You can cache providers on your private workers to speed up your runs because your workers don't need to download providers from the internet every time a run is executed. Provider caching is supported in Spacelift with a little configuration on the worker side:

1. **On the worker**: Export the [`SPACELIFT_WORKER_EXTRA_MOUNTS`](#docker-only-options) variable with the path to the directory where the providers will be stored.
2. **In the stack**: Where you want to enable provider caching, set the `TF_PLUGIN_CACHE_DIR` environment variable to the path you specified in the `SPACELIFT_WORKER_EXTRA_MOUNTS` variable.

The `SPACELIFT_WORKER_EXTRA_MOUNTS` directory on the host _should_ use shared storage that is accessible by all workers in the pool. This can be a shared filesystem, a network drive, or a cloud storage service. If you choose not to use a shared storage solution, you might run into an issue where the `plan` phase succeeds but the `apply` phase fails due to the provider cache not being available.

To avoid this, you can run `tofu init` (if using OpenTofu) or `terraform init` (if using Terraform) as a `before-apply` hook, which will populate the cache on that node. Once the cache is populated, re-initialization should be quick.
{% endif %}

## Network security

Private workers need to be able to make outbound connections in order to communicate with Spacelift and access any resources required by your runs. If you have policies in place that require limits on the outbound traffic allowed from your workers, use the following lists as a guide.

### AWS Services

Your worker needs access to the following AWS services in order to function correctly. You can refer to the [AWS documentation](https://docs.aws.amazon.com/general/latest/gr/aws-ip-ranges.html){: rel="nofollow"} for their IP address ranges.

{% if is_saas() %}

Give private workers access to:

- The public Elastic Container Registry (if using Spacelift's default runner image).
- `app.spacelift.io`, `registry.spacelift.io`, `<your account name>.app.spacelift.io`, and `downloads.spacelift.io` which point at CloudFront.
- `worker-iot.spacelift.io`. This points at the [AWS IoT Core endpoints](https://docs.aws.amazon.com/general/latest/gr/iot-core.html){: rel="nofollow"} for worker communication via MQTT.
    - !!! info "US Regional URLs"
          If your account is in the US region, your workers need access to `app.us.spacelift.io`, `registry.us.spacelift.io`, `<your account name>.app.us.spacelift.io`, `downloads.us.spacelift.io`, and `worker-iot.us.spacelift.io` instead.
- [Amazon S3](https://docs.aws.amazon.com/general/latest/gr/s3.html){: rel="nofollow"} for uploading run logs.

!!! tip "Failover"
    Allow access to the IoT Core and S3 endpoints in both the `eu-west-1` and `eu-central-1` regions. Typically we use services in `eu-west-1`, however in the case of a full regional outage of `eu-west-1` we would failover to the `eu-central-1` region.

{% else %}

Give private workers access to:

- The public Elastic Container Registry (if using Spacelift's default runner image).
- Your Self-Hosted server, for example `https://spacelift.myorg.com`.
- The [AWS IoT Core endpoints](https://docs.aws.amazon.com/general/latest/gr/iot-core.html){: rel="nofollow"} in your installation region for worker communication via MQTT.
- [Amazon S3](https://docs.aws.amazon.com/general/latest/gr/s3.html){: rel="nofollow"} in your installation region for uploading run logs.

{% endif %}

### Other

In addition, you will also need to allow access to the following:

- Your VCS provider.
- Any custom container registries if using custom runner images.
- Any other infrastructure required as part of your runs.
{% if is_saas() %}- `keys.openpgp.org`, which is required to download the PGP key used to sign Spacelift binaries.{% endif %}

## Hardware recommendations

Hardware requirements for workers will vary depending on the stack size (how many resources managed, resource type, etc.), but we recommend:

- **Memory**: 2GB minimum
- **Compute power**: 2 vCPUs minimum
- **Server types**:
    - AWS: **t3.small** instance type
    - Azure: **Standard_A2_V2** virtual machine
    - GCP: **e2-medium** instance type

## Using worker pools

Worker pools must be explicitly attached to [stacks](../stack/README.md) and/or [modules](../../vendors/terraform/module-registry.md) to process their workloads. This can be done in the _Behavior_ section of stack and module settings:

![Editing the existing stack](<../../assets/screenshots/stack/settings/stack-behavior_worker-pools.png>)

![Setting up a new module](<../../assets/screenshots/module/settings/module-behavior_worker-pools.png>)

## Worker pool management views

You can view the activity and status of every aspect of your worker pool in the worker pool detail view.

1. Navigate to _Manage Organization_ > _Worker Pools_.
2. Click the name of the worker pool you'd like to manage or review.
3. Use the tabs to navigate through the pool:
      - [**Workers**](#workers): Displays the workers in the pool, their IDs, any metadata tags, and when they were created.
      - [**Queue**](#queue): Displays any [runs](../run/README.md) that are in the worker pool's queue for processing.
      - [**Used by**](#used-by): Displays the stacks and/or modules the worker pool is attached to.

![Worker pool management view used by tab](<../../assets/screenshots/worker-pool-management-screen.png>)

### Private worker pool

While Spacelift manages the workers in the public worker pool, you are responsible for managing the workers in a private worker pool.

![private worker pool management view](<../../assets/screenshots/management-view-private-worker-pool.png>)

#### Workers

The _Workers_ tab lists all workers for the worker pool and their statuses.

##### Status

A worker can have one of three possible statuses:

- `DRAINED`: The worker is not accepting new work.
- `BUSY`: The worker is currently processing or about to process a run.
- `IDLE`: The worker is available to start processing new runs.

#### Queue

The _Queue_ tab lists all runs that can be scheduled and are currently in progress. In-progress runs will be the first entries in the list without any filtering.

!!! info
    A [tracked run](../run/tracked.md) that is waiting on another tracked run, or a run that has a [dependency](../stack/stack-dependencies.md) on other runs might not show up in the queue.

### Available Actions

#### Cycle

Cycling the worker pool sends a self-destruct signal to all the workers in this pool. The process can take up to 20 seconds to complete. When you click **Cycle**, you will be prompted to confirm this action as it cannot be undone.

![private worker pool cycle action view](<../../assets/screenshots/CycleWorkerPool.png>)

#### Reset

When you reset your worker pool, a new token is generated for your pool. Any workers using the old token will no longer be able to connect, so you will need to update the credentials for the workers connected to that pool.

You can use **Reset** to secure your workers if the certificate was compromised. Once your worker pool is reset, [generate a new certificate](#1-generate-worker-private-key).

![private worker pool reset action view](<../../assets/screenshots/ResetWorkerPool.png>)

#### Used by

The _Used by_ tab lists all [stacks](../stack/README.md) and/or [modules](../../vendors/terraform/module-registry.md) using the private worker pool.

{% if is_saas() %}

### Public worker pool

The public worker pool is a worker pool managed by Spacelift. Due to security and compliance requirements, we do not list the workers of the public worker pool.

![public worker pool management view](<../../assets/screenshots/management-view-public-worker-pool.png>)

#### Queue

The _Queue_ tab lists all runs that can be scheduled and are currently in progress. In-progress runs will be the first entries in the list without any filtering.

!!! info
    A [tracked run](../run/tracked.md) that is waiting on another tracked run, or a run that has a [dependency](../stack/stack-dependencies.md) on other runs might not show up in the queue.

#### Used by

The _Used by_ tab lists all [stacks](../stack/README.md) and/or [modules](../../vendors/terraform/module-registry.md) using the public worker pool.

{% endif %}

## Troubleshooting

### Spacelift doesn't show completed local runs

Sometimes, the run completes locally in 10 minutes. But on Spacelift, it takes over 30 minutes, with no new activity appearing in the logs for the entire duration. If debug logging is on then the logs only show `Still running...` for that duration.

This issue might be related to the instance size and its CPU limitations. Monitor CPU and memory usage and make adjustments as needed.
