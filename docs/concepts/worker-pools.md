---
description: >-
  This article explains how you can set up and use on-premise private worker
  pools.
---

# Worker pools

By default, Spacelift uses a managed worker pool hosted and operated by us. This is very convenient, but often you may have special requirements regarding infrastructure, security or compliance, which aren't served by the public worker pool. This is why Spacelift also supports private worker pools, which you can use to host the workers which execute Spacelift workflows on your end.

In order to enjoy the maximum level of flexibility and security with a private worker pool, temporary run state is encrypted end-to-end, so only the workers in your worker pool can look inside it. We use asymmetric encryption to achieve this and only you ever have access to the private key.

## Setting up

### Generate Worker Private Key

To make sure that we have no access to your private key, you will need to generate it on your end, and use it to create a certificate signing request to give to Spacelift. We'll generate a certificate for you, so that workers can use it to authenticate with the Spacelift backend. The following command will generate the key and CSR:

```bash
openssl req -new -newkey rsa:4096 -nodes -keyout spacelift.key -out spacelift.csr
```

!!! warning
    Don't forget to store the `spacelift.key` file (private key) in a secure location. You’ll need it later, when launching workers in your worker pool.

You can set up your worker pool from the Spacelift UI by navigating to Worker Pools section of your account, or you can also create it programmatically using the `spacelift_worker_pool` resource type within the [Spacelift Terraform provider](../vendors/terraform/terraform-provider.md).

### Navigate to Worker Pools

![](<../assets/screenshots/Screen Shot 2022-06-29 at 6.45.15 PM (1).png>)

### Add Worker Pool Entity

Give your worker pool a name, and submit the `spacelift.csr` file in the worker pool creation form. After creation of the worker pool, you’ll receive a **Spacelift token**. This token contains configuration for your worker pool launchers, as well as the certificate we generated for you based on the certificate signing request.

!!! warning
    After clicking create, you will receive a token for the worker pool. Don't forget to save your **Spacelift token** in a secure location as you'll need this later when launching the worker pool.

![Upload the certificate you generated previously and create a worker pool.](<../assets/screenshots/Screen Shot 2022-06-29 at 6.47.40 PM.png>)

![](<../assets/screenshots/Screen Shot 2022-06-29 at 6.49.01 PM.png>)

### Launch Private Worker Pool

The launcher binaries are available here: [x86_64](https://downloads.spacelift.io/spacelift-launcher-x86_64) (amd64 CPU), [aarch64](https://downloads.spacelift.io/spacelift-launcher-aarch64) (arm64 CPU). In order to work, it expects to be able to write to the local Docker socket. Unless you're using a Docker-based container scheduler like Kubernetes or ECS, please make sure that Docker is installed.

Finally, you can run the launcher binary by setting two environment variables:

- `SPACELIFT_TOKEN` - the token you’ve received from Spacelift on worker pool creation
- `SPACELIFT_POOL_PRIVATE_KEY` - the contents of the private key file you generated, in base64.

!!! info
    You need to encode the _entire_ private key using base-64, making it a single line of text. The simplest approach is to just run `cat spacelift.key | base64 -w 0` in your command line. For Mac users, the command is `cat spacelift.key | base64 -b 0`.

Congrats! Your launcher should now connect to the Spacelift backend and start handling runs.

!!! tip
    In general, arm64-based virtual machines are cheaper than amd64-based ones, so if your cloud provider supports them, we recommend using them. If you choose to do so, and you're using [custom runner images](../concepts/stack/stack-settings.md#runner-image), make sure they're compatible with ARM64. All Spacelift provided runner images are compatible with both CPU architectures.

### Terraform Modules and Helm Chart

For AWS, Azure and GCP users we've prepared an easy way to run Spacelift worker pools. [This repository](https://github.com/spacelift-io/spacelift-worker-image) contains the code for Spacelift's base images, and the following repositories contain Terraform modules to customize and deploy worker pools to AWS, Azure or GCP:

- AWS: [terraform-aws-spacelift-workerpool-on-ec2](https://github.com/spacelift-io/terraform-aws-spacelift-workerpool-on-ec2).
- Azure: [terraform-azure-spacelift-workerpool](https://github.com/spacelift-io/terraform-azure-spacelift-workerpool).
- GCP: [terraform-google-spacelift-workerpool](https://github.com/spacelift-io/terraform-google-spacelift-workerpool).

In addition, the [spacelift-workerpool-k8s](https://github.com/spacelift-io/spacelift-workerpool-k8s) repository contains a Helm chart for deploying workers to Kubernetes.

!!! tip
    Since the Launcher is getting downloaded during the instance startup, it is recommended to recycle the worker pool every once in a while to ensure that it is up to date. You don't want to miss out on the latest features and bug fixes! You can do this by draining all the workers one-by-one in the UI, then terminating the instances in your cloud provider.

    It is also recommended to check the above repositories for updates from time to time.

!!! info
    AWS ECS is supported when using the EC2 launch type but Spacelift does not currently provide a Terraform module for this setup.

### Configuration options

A number of configuration variables is available to customize how your launcher behaves:

- `SPACELIFT_DOCKER_CONFIG_DIR` - if set, the value of this variable will point to the directory containing Docker configuration, which includes credentials for private Docker registries. Private workers can populate this directory for example by executing `docker login` before the launcher process is started;
- `SPACELIFT_MASK_ENVS`- comma-delimited list of whitelisted environment variables that are passed to the workers but should never appear in the logs;
- `SPACELIFT_WORKER_NETWORK` - network ID/name to connect the launched worker containers, defaults to `bridge`;
- `SPACELIFT_WORKER_EXTRA_MOUNTS` - additional files or directories to be mounted to the launched worker docker containers, as a comma-separated list of mounts in the form of `/host/path:/container/path`;
- `SPACELIFT_WORKER_RUNTIME` - runtime to use for worker container;
- `SPACELIFT_WHITELIST_ENVS` - comma-delimited list of environment variables to pass from the launcher's own environment to the workers' environment;
- `SPACELIFT_LAUNCHER_LOGS_TIMEOUT` - custom timeout (the default is _7 minutes_) for killing jobs not producing any logs. This is a duration flag, expecting a duration-formatted value, eg `1000s` ;
- `SPACELIFT_LAUNCHER_RUN_INITIALIZATION_POLICY` - file that contains the run initialization policy that will be parsed/used; If the run initialized policy can not be validated at the startup the worker pool will exit with an appropriate error;
- `SPACELIFT_LAUNCHER_RUN_TIMEOUT` - custom maximum run time - the default is _70 minutes_. This is a duration flag, expecting a duration-formatted value, eg. `120m` ;

### Passing metadata tags

When the launcher from a private worker pool is registering with the mothership, you can send along some tags that will allow you to uniquely identify the process/machine for the purpose of draining or debugging. Any environment variables using `SPACELIFT_METADATA_` prefix will be passed on. As an example, if you're running Spacelift workers in EC2, you can do the following just before you execute the launcher binary:

```bash
export SPACELIFT_METADATA_instance_id=$(ec2-metadata --instance-id | cut -d ' ' -f2)
```

Doing so will set your EC2 instance ID as `instance_id` tag in your worker.

### VCS Agents

VCS Agents are intended for users who have privately accessible version control systems (VCS), if your VCS is not private, then you do not need to use a VCS Agent.

 When using private workers with a privately accessible version control system, you will need to ensure that your private workers have direct network access to your Version Control System. Additionally, you will need to inform the private workers of the target network address for each of your VCS Agent Pools. To do this, setup a variable mapping similar to the following example below, for each private VCS you are seeking to integrate.

```bash
export SPACELIFT_PRIVATEVCS_MAPPING_NAME_0=bitbucket_pool
export SPACELIFT_PRIVATEVCS_MAPPING_BASE_ENDPOINT_0=http://192.168.2.2
export SPACELIFT_PRIVATEVCS_MAPPING_NAME_1=github_pool
export SPACELIFT_PRIVATEVCS_MAPPING_BASE_ENDPOINT_1=https://internal-github.net
// ...
```

### Network Security

Private workers need to be able to make outbound connections in order to communicate with Spacelift, as well as to access any resources required by your runs. If you have policies in place that require you to limit the outbound traffic allowed from your workers, you can use the following lists as a guide.

#### AWS Services

Your worker needs access to the following AWS services in order to function correctly. You can refer to the [AWS documentation](https://docs.aws.amazon.com/general/latest/gr/aws-ip-ranges.html) for their IP address ranges.

- Access to the public Elastic Container Registry if using our default runner image.
- Access to `app.spacelift.io`, `<your account name>.app.spacelift.io`, and `downloads.spacelift.io` which point at CloudFront.
- Access to the [AWS IoT Core endpoints](https://docs.aws.amazon.com/general/latest/gr/iot-core.html) in eu-west-1 for worker communication via MQTT.
- Access to [Amazon S3](https://docs.aws.amazon.com/general/latest/gr/s3.html) in eu-west-1 for uploading run logs.

#### Other

In addition, you will also need to allow access to the following:

- Your VCS provider.
- Access to any custom container registries you use if using custom runner images.
- Access to any other infrastructure required as part of your runs.
- Access to `keys.openpgp.org` - required to download the PGP key used to sign Spacelift binaries.

## Using worker pools

Worker pools must be explicitly attached to [stacks](stack/README.md) and/or [modules](../vendors/terraform/module-registry.md) in order to start processing their workloads. This can be done in the Behavior section of stack and module settings:

![Example when editing the existing stack](../assets/screenshots/Edit_stack_·_Managed_stack.png)

![Example when setting up a new module](<../assets/screenshots/New_module_·_marcinwyszynski (1).png>)
