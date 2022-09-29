---
description: This article explains how you can set up and use on-premise VCS Agent Pools.
---

# VCS Agent Pools

By default, Spacelift communicates with your VCS provider directly. This is usually sufficient, but some users may have special requirements regarding infrastructure, security or compliance, and need to host their VCS system in a way that's only accessible internally, where Spacelift can't reach it. This is where VCS Agent Pools come into play.

A single VCS Agent Pool is a way for Spacelift to communicate with a single VCS system on your side. You run VCS Agents inside of your infrastructure and configure them with your internal VCS system endpoint. They will then connect to a gateway on our backend, and we will be able to access your VCS system through them.

On the Agent there are very conservative checks on what requests are let through and which ones are denied, with an explicit allowlist of paths that are necessary for Spacelift to work. All requests will be logged to standard output with a description about what they were used for.

## Create the VCS Agent Pool

Navigate to VCS Agent Pools using the Spacelift navigation sidebar. Click **Add VCS Agent Pool.**

![](../assets/screenshots/Screen Shot 2022-06-21 at 11.31.39 AM.png)

Give your VCS Agent Pool a name and description, and you're done! A configuration token will be downloaded.

![Creation of VCS Agent Pool](../assets/screenshots/Screen Shot 2022-06-21 at 11.29.22 AM.png)

## Download the VCS Agent binary

The latest version of the VCS Agent binary can be downloaded from [here](https://downloads.spacelift.io/spacelift-vcs-agent).

## Configure and run the VCS Agent

A number of configuration variables is available to customize how your VCS Agent behaves. The ones marked as required are … well … required.

| CLI Flag                 | Environment Variable                       | Status | Default Value | Description                                                  |
| ------------------------ | ------------------------------------------ |------ | ------------- | ------------------------------------------------------------ |
| `--target-base-endpoint` | `SPACELIFT_VCS_AGENT_TARGET_BASE_ENDPOINT` | Required |  | The internal endpoint of your VCS system, including the protocol, as well as port, if applicable. (e.g., `http://169.254.0.10:7990`) |
| `--token`                | `SPACELIFT_VCS_AGENT_POOL_TOKEN`           | Required |  | The token you’ve received from Spacelift during VCS Agent Pool creation |
| `--vendor`               | `SPACELIFT_VCS_AGENT_VENDOR`               | Required |  | The vendor of your VCS system. Currently available options are `gitlab`, `bitbucket_datacenter` and `github_enterprise` |
| `--allowed-projects` | `SPACELIFT_VCS_AGENT_ALLOWED_PROJECTS` | Optional | `.*` | Regexp matching allowed projects for API calls. Projects are in the form: 'group/repository'. |
| `--bugsnag-api-key` | `SPACELIFT_VCS_AGENT_BUGSNAG_API_KEY` | Optional |  | Override the Bugsnag API key used for error reporting. |
| `--parallelism` | `SPACELIFT_VCS_AGENT_PARALLELISM` | Optional | `4` | Number of streams to create. Each stream can handle one request simultaneously. |
|  | `HTTPS_PROXY` | Optional |  | Hostname or IP address of the proxy server, including the protocol, as well as port, if applicable. (e.g., `http://10.10.1.1:8888`) |
| | `NO_PROXY` | Optional | | Comma-separated list of host names that shouldn't go through any proxy is set in. |

Congrats! Your VCS Agent should now connect to the Spacelift backend and start handling connections.

![Running the VCS Agent](<../assets/screenshots/image (51).png>)

Within the VCS Agent Pools page, you will be able to see the number of active connections used by your pool.

![VCS Agent Pool Connections](<../assets/screenshots/image (47).png>)

!!! warning
    Now whenever you need to specify an endpoint inside of Spacelift which should use your VCS Agent Pool, you should write it this way: `private://my-vcs-agent-pool-name/possible/path`

![](<../assets/screenshots/Screen Shot 2022-06-21 at 11.34.18 AM.png>)

When trying to use this integration, i.e. by opening the Stack creation form, you'll get a detailed log of the requests:

![Access Log example](<../assets/screenshots/image (50).png>)

### Passing Metadata Tags

When the VCS Agent from a VCS Agent Pool is connecting to the gateway, you can send along some tags that will allow you to uniquely identify the process / machine for the purpose of debugging. Any environment variables using `SPACELIFT_METADATA_` prefix will be passed on. As an example, if you're running Spacelift VCS Agents in EC2, you can do the following just before you execute the VCS Agent binary:

```bash
export SPACELIFT_METADATA_instance_id=$(ec2-metadata --instance-id | cut -d ' ' -f2)
```

Doing so will set your EC2 instance ID as _instance_id_ tag in your VCS Agent connections.

### Private Workers

VCS agents are only supported when using private worker pools. Because your source code is downloaded directly by Spacelift workers, you need to configure your workers to know how to reach your VCS instance. Information on how to do this is provided on the [worker pools](worker-pools.md#vcs-agents) page.
