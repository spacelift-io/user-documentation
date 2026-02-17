---
description: This article explains how you can set up and use on-premise VCS Agent Pools.
---

# VCS agent pools

{% if is_saas() %}
!!! Info
    This feature is only available to Enterprise plan. Please check out our [pricing page](https://spacelift.io/pricing){: rel="nofollow"} for more information.
{% endif %}

By default, Spacelift communicates with your VCS provider directly. However, some users may have special requirements regarding infrastructure, security, or compliance, and need to host their VCS system in a way that's only accessible internally where Spacelift can't reach it. This is where VCS agent pools come into play.

A single VCS agent pool is a way for Spacelift to communicate with a single VCS system on your side. You run VCS agents inside of your infrastructure and configure them with your internal VCS system endpoint. They will then connect to a gateway on our backend, and we will be able to access your VCS system through them.

!!! warning "Raw git"

    Raw git does not work with VCS agents. If you are using raw git repositories, you will need to use publicly accessible URLs or implement a workaround like a proxy or tunnel to replace VCS agent functionality.

On the VCS agent there are very conservative checks on what requests are let through and which ones are denied, with an explicit allowlist of paths that are necessary for Spacelift to work. All requests will be logged to standard output with a description about what they were used for.

## Create the VCS agent pool

1. Navigate to _Integrate Services_ > _Integrations_.
2. On the _VCS Agent Pools_ card, click **View**.
3. In the top-right corner, click **Create VCS agent pool**.
    ![Create VCS agent pool](<../assets/screenshots/concepts/vcs-agent-pools/create-vcs-agent-pool.png>)
4. Fill in the pool details:
    ![Creation of VCS agent pool](<../assets/screenshots/Screen Shot 2022-06-21 at 11.29.22 AM.png>)
      - **Name**: Enter a unique, descriptive name for your VCS agent pool.
      - **Description** (optional): Enter a (markdown-supported) description of the agent pool.
5. Click **Create new VCS agent pool**.

A configuration token will be downloaded.

## Running the VCS agent

### Download the VCS agent binaries

The latest version of the VCS agent binaries for Linux are available at Spacelift's CDN:

| Binary name                                                                               | SHA256 checksum                                                                                                 | GPG signature                                                                                                           |
| ----------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| [spacelift-vcs-agent-x86_64](https://downloads.spacelift.io/spacelift-vcs-agent-x86_64)   | [spacelift-vcs-agent-x86_64_SHA256SUMS](https://downloads.spacelift.io/spacelift-vcs-agent-x86_64_SHA256SUMS)   | [spacelift-vcs-agent-x86_64_SHA256SUMS.sig](https://downloads.spacelift.io/spacelift-vcs-agent-x86_64_SHA256SUMS.sig)   |
| [spacelift-vcs-agent-aarch64](https://downloads.spacelift.io/spacelift-vcs-agent-aarch64) | [spacelift-vcs-agent-aarch64_SHA256SUMS](https://downloads.spacelift.io/spacelift-vcs-agent-aarch64_SHA256SUMS) | [spacelift-vcs-agent-aarch64_SHA256SUMS.sig](https://downloads.spacelift.io/spacelift-vcs-agent-aarch64_SHA256SUMS.sig) |

Binaries for other operating systems are available on the [GitHub Releases](https://github.com/spacelift-io/vcs-agent/releases){: rel="nofollow"} page.

#### Checksum verification

```shell
curl https://keys.openpgp.org/vks/v1/by-fingerprint/175FD97AD2358EFE02832978E302FB5AA29D88F7 | gpg --import

gpg --verify spacelift-vcs-agent-x86_64_SHA256SUMS.sig
CHECKSUM=$(cut -f 1 -d ' ' spacelift-vcs-agent-x86_64_SHA256SUMS)
ACTUAL_CHECKSUM=$(sha256sum spacelift-vcs-agent-x86_64 | cut -f 1 -d ' ')

if [ "$CHECKSUM" != "$ACTUAL_CHECKSUM" ]; then
  echo "Invalid checksum!"
  exit 1
else
  echo "Checksum verification succeeded."
fi
```

### Run via Docker

The VCS Agent is also available as a multi-arch (amd64 and arm64) Docker image:

- `public.ecr.aws/spacelift/vcs-agent:latest`
- `public.ecr.aws/spacelift/vcs-agent:<version>`

The available versions are listed on the [GitHub Releases](https://github.com/spacelift-io/vcs-agent/releases){: rel="nofollow"} page.

```shell
docker run -it --rm -e "SPACELIFT_VCS_AGENT_POOL_TOKEN=<VCS TOKEN>" \
  -e "SPACELIFT_VCS_AGENT_TARGET_BASE_ENDPOINT=http://169.254.0.10:7990" \
  -e "SPACELIFT_VCS_AGENT_VENDOR=bitbucket_datacenter" \
  public.ecr.aws/spacelift/vcs-agent
```

### Run the VCS Agent inside a Kubernetes Cluster

We have a [VCS Agent Helm Chart](https://github.com/spacelift-io/spacelift-helm-charts){: rel="nofollow"} that you can use to install the VCS agent on top of your Kubernetes Cluster. After creating a VCS agent pool in Spacelift and generating a token, you can add our Helm chart repo and update your local cache using:

```shell
helm repo add spacelift https://downloads.spacelift.io/helm
helm repo update
```

Assuming your token, VCS endpoint and vendor are stored in the `SPACELIFT_VCS_AGENT_POOL_TOKEN`, `SPACELIFT_VCS_AGENT_TARGET_BASE_ENDPOINT`, and `SPACELIFT_VCS_AGENT_VENDOR` environment
variables, you can install the chart using the following command:

```shell
helm upgrade vcs-agent spacelift/vcs-agent --install --set "credentials.token=$SPACELIFT_VCS_AGENT_POOL_TOKEN,credentials.endpoint=$SPACELIFT_VCS_AGENT_TARGET_BASE_ENDPOINT,credentials.vendor=$SPACELIFT_VCS_AGENT_VENDOR"
```

## Configure and run the VCS agent

A number of configuration variables is available to customize how your VCS Agent behaves.

| CLI Flag                 | Environment Variable                       | Status   | Default Value | Description                                                                                                                             |
| ------------------------ | ------------------------------------------ | -------- | ------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `--target-base-endpoint` | `SPACELIFT_VCS_AGENT_TARGET_BASE_ENDPOINT` | Required |               | The internal endpoint of your VCS system, including the protocol, as well as port, if applicable. (e.g., `http://169.254.0.10:7990`)    |
| `--token`                | `SPACELIFT_VCS_AGENT_POOL_TOKEN`           | Required |               | The token you’ve received from Spacelift during VCS Agent Pool creation                                                                 |
| `--vendor`               | `SPACELIFT_VCS_AGENT_VENDOR`               | Required |               | The vendor of your VCS system. Currently available options are `azure_devops`, `gitlab`, `bitbucket_datacenter` and `github_enterprise` |
| `--allowed-projects`     | `SPACELIFT_VCS_AGENT_ALLOWED_PROJECTS`     | Optional | `.*`          | Regexp matching allowed projects for API calls. Projects are in the form: 'group/repository'.                                           |
| `--bugsnag-api-key`      | `SPACELIFT_VCS_AGENT_BUGSNAG_API_KEY`      | Optional |               | Override the Bugsnag API key used for error reporting.                                                                                  |
| `--parallelism`          | `SPACELIFT_VCS_AGENT_PARALLELISM`          | Optional | `4`           | Number of streams to create. Each stream can handle one request simultaneously.                                                         |
| `--debug-print-all`      | `SPACELIFT_VCS_AGENT_DEBUG_PRINT_ALL`      | Optional | `false`       | Makes vcs-agent print out all the requests and responses.                                                                               |
|                          | `HTTPS_PROXY`                              | Optional |               | Hostname or IP address of the proxy server, including the protocol, as well as port, if applicable. (e.g., `http://10.10.1.1:8888`)     |
|                          | `NO_PROXY`                                 | Optional |               | Comma-separated list of host names that shouldn't go through any proxy is set in.                                                       |

Once all required configuration is complete, your VCS agent should connect to the Spacelift backend and start handling connections.

![Running the VCS agent](<../assets/screenshots/image (51).png>)

The _VCS Agent Pools_ page displays the number of active connections used by your pool.

![VCS Agent Pool Connections](<../assets/screenshots/image (47).png>)

Whenever you need to specify an endpoint inside of Spacelift that should use your VCS agent pool, you should write it this way: `private://<vcs-agent-pool-name>/possible/path`

![VCS agent integration example](<../assets/screenshots/Screen Shot 2022-06-21 at 11.34.18 AM.png>)

When trying to use this integration, such as by opening the stack creation form, you'll get a detailed log of the requests:

![Access Log example](<../assets/screenshots/image (50).png>)

### Configure direct network access

!!! tip
    VCS agents are intended for version control systems (VCS) that **cannot** be accessed over the internet from the Spacelift backend.

    If your VCS can be accessed over the internet, possibly after allowing the Spacelift backend IP addresses, then you do not need to use VCS agents.

When using private workers with a privately accessible version control system, your private workers need direct network access to your VCS.

Additionally, you need to inform the private workers of the target network address for each of your VCS agent pools by setting up the following variables:

- `SPACELIFT_PRIVATEVCS_MAPPING_NAME_<NUMBER>`: Name of the VCS agent pool.
- `SPACELIFT_PRIVATEVCS_MAPPING_BASE_ENDPOINT_<NUMBER>`: IP address or hostname, with protocol, for the VCS system.

There can be multiple VCS systems, so replace `<NUMBER>` with an integer. Start from `0` and increment it by one for each new VCS system.

Here is an example that configures access to two VCS systems:

```bash
export SPACELIFT_PRIVATEVCS_MAPPING_NAME_0=bitbucket_pool
export SPACELIFT_PRIVATEVCS_MAPPING_BASE_ENDPOINT_0=http://192.168.2.2
export SPACELIFT_PRIVATEVCS_MAPPING_NAME_1=github_pool
export SPACELIFT_PRIVATEVCS_MAPPING_BASE_ENDPOINT_1=https://internal-github.net
```

See the [VCS Agents](./worker-pools/kubernetes-workers.md#using-vcs-agents-with-kubernetes-workers) section in the Kubernetes workers docs for information on how to configure VCS agents with Kubernetes-based workers.

## Worker pool settings

{% if is_saas() %}
VCS agents are only supported when using private worker pools.
{% endif %}
Since your source code is downloaded directly by Spacelift workers, you need to configure them to [directly access your VCS instance](#configure-direct-network-access).

## Passing metadata tags

When the VCS agent from a VCS agent pool is connecting to the gateway, you can send some tags that will allow you to uniquely identify the process or machine for the purpose of debugging. Any environment variables using `SPACELIFT_METADATA_` prefix will be passed on.

For example, if you're running Spacelift VCS Agents in EC2, you can do the following just before you execute the VCS Agent binary:

```bash
export SPACELIFT_METADATA_instance_id=$(ec2-metadata --instance-id | cut -d ' ' -f2)
```

This will set your EC2 instance ID as _instance_id_ tag in your VCS agent connections.

## Debug information

Sometimes, it is helpful to display additional information to troubleshoot an issue. When that is needed, set the following environment variables:

```shell
export GODEBUG=http2debug=2
export GRPC_GO_LOG_SEVERITY_LEVEL=info
export GRPC_GO_LOG_VERBOSITY_LEVEL=99
```

You may want to tweak the values to increase or decrease verbosity.
