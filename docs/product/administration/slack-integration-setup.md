---
description: Find out how to setup a Slack integration in self-hosted.
---

# Slack integration setup

If you want to use the [Slack integration](https://docs.spacelift.io/integrations/chatops/slack) in your self-hosting instance, you need to create your own Slack app and add its details to the _config.json_ file before running the self-hosting installer. This section explains how to do that, along with describing limitations of the Slack integration in self-hosting.

## Known Limitations

The Slack integration relies on Slack being able to communicate with Spacelift in order to provide support for [Slash commands](https://docs.spacelift.io/integrations/chatops/slack#available-slash-commands). This means that Slack must be able to access your Spacelift load balancer in order for it to be able to make requests to `https://<your-spacelift-domain>/webhooks/slack`.

This means that if you are using an internal load balancer for Spacelift, Slack will not be able to access this endpoint.

## Creating your Slack app

First, create a new Slack app in your workspace by navigating to <https://api.slack.com/apps> and following these instructions:

- Click "Create New App"
- Choose "From an app manifest"
- Select your workspace
- Paste following manifest, replacing `<your-domain>` with the domain you want to host the self-hosted Spacelift instance on.

```json
{
    "display_information": {
        "name": "Spacelift",
        "description": "Taking your infra-as-code to the next level",
        "background_color": "#131417",
        "long_description": "Spacelift is a sophisticated and compliant infrastructure delivery platform for Terraform (including Terragrunt), Pulumi, CloudFormation, Ansible, and Kubernetes.\r\n\r\n• No lock-in. Under the hood, Spacelift uses your choice of Infrastructure as Code providers: open-source projects with vibrant ecosystems and a multitude of existing providers, modules, and tutorials.\r\n\r\n• Works with your Git flow. Spacelift integrates with GitHub (and other VCSes) to provide feedback on commits and Pull Requests, allowing you and your team to preview the changes before they are applied.\r\n\r\n• Drift detection. Spacelift natively detects drift, and can optionally revert it, to provide visibility and awareness to those \"changes\" that will inevitably happen.\r\n\r\n• Policy as a Code. With Open Policy Agent (OPA) Rego, you can programmatically define policies, approval flows, and various decision points within your Infrastructure as Code flow.\r\n\r\n• Customize your runtime. Spacelift uses Docker to run its workflows, which allows you to fully control your execution environment.\r\n\r\n• Share config using contexts. Spacelift contexts are collections of configuration files and environment variables that can be attached to multiple stacks.\r\n\r\n• Look ma, no credentials. Spacelift integrates with identity management systems from major cloud providers; AWS, Azure, and Google Cloud, allowing you to set up limited temporary access to your resources without the need to supply powerful static credentials.\r\n\r\n• Manage programmatically. With the Terraform provider, you can manage Spacelift resources as code.\r\n\r\n• Protect your state. Spacelift supports a sophisticated state backend and can optionally manage the state on your behalf."
    },
    "features": {
        "bot_user": {
            "display_name": "Spacelift",
            "always_online": true
        },
        "slash_commands": [
            {
                "command": "/spacelift",
                "url": "https://<your-domain>/webhooks/slack",
                "description": "Get notified about Spacelift events",
                "usage_hint": "subscribe, unsubscribe or help",
                "should_escape": false
            }
        ]
    },
    "oauth_config": {
        "redirect_urls": [
            "https://<your-domain>/slack_oauth"
        ],
        "scopes": {
            "bot": [
                "channels:read",
                "chat:write",
                "chat:write.public",
                "commands",
                "links:write",
                "team:read",
                "users:read"
            ]
        }
    },
    "settings": {
        "event_subscriptions": {
            "request_url": "https://<your-domain>/webhooks/slack",
            "bot_events": [
                "app_uninstalled"
            ]
        },
        "interactivity": {
            "is_enabled": true,
            "request_url": "https://<your-domain>/webhooks/slack"
        },
        "org_deploy_enabled": false,
        "socket_mode_enabled": false,
        "token_rotation_enabled": false
    }
}
```

## Configuring the Spacelift installer

Once it's done, you just need to copy the relevant information from the "Basic Information" tab of your Slack App to the configuration file:

```json
{
    "slack_config": {
        "enabled": true,
        "client_id": "<client id here>",
        "client_secret": "<client secret here>",
        "signing_secret": "<signing secret here>"
    }
}
```

Once you have populated your configuration, just run the installer as described in the [installation guide](./install.md#running-the-installer).

After the installation script finishes. You can now go to your self-hosted Spacelift instance, to Settings -> Slack and install the Slack app into your workspace.

## Updating the Slack integration

To update the Slack integration for your self-hosted Spacelift instance:

### 1. Modify the Installer Config

Update the config.json file with the new Slack app details:

```json
{
    "slack_config": {
        "enabled": true,
        "client_id": "<new client id here>",
        "client_secret": "<new client secret here>",
        "signing_secret": "<new signing secret here>"
    }
}
```

### 2. Restart the Server

After updating the configuration, re-run the install.sh script to apply the changes. Once the installer finishes, please restart the server ECS service as the configuration is loaded during startup.

Note: If you are using Slack notification policies, ensure the updated channel IDs are reflected in the policies.

## Removing Slack Integration

To remove the Slack integration from your self-hosted Spacelift instance:

### 1. Uninstall the Slack App

Remove the Slack app from your workspace by following Slack's [guide](https://slack.com/intl/en-gb/help/articles/360003125231-Remove-apps-and-customised-integrations-from-your-workspace){: rel="nofollow"}

### 2. Update the Installer Config

Set the Slack configuration in the config.json file to enabled: false and clear the other fields:

```json
{
    "slack_config": {
        "enabled": false,
        "client_id": "",
        "client_secret": "",
        "signing_secret": ""
    }
}
```

### 3. Restart the Server

Re-run the install.sh script to apply the updated configuration. Restart the ECS service to ensure the changes are reflected.
