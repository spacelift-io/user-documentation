---
description: Slack configuration.
---

# Slack

The Spacelift Slack integration relies on a Slack app being created to allow you to link Spacelift to your Slack workspace. There are two ways you can do this:

1. Dynamically via your organization settings.
2. Statically via the environment.

To find out how to dynamically configure your Slack app via the frontend, take a look at our [Slack integration documentation](../../../integrations/chatops/slack.md#create-slack-app). This page explains how to configure Slack statically via the environment.

## Networking

Please note that in order for Slack to send messages to Spacelift (for example Slash Commands), Slack needs to be able to access your Spacelift server. This means that if you want the full functionality of the integration to work your Spacelift server needs to be accessible via the public internet.

## Create Slack app

Before you can configure Slack, you need to create a Slack app in your workspace. This app provides credentials necessary for Spacelift and Slack to communicate, and also tells Slack about certain endpoints in Spacelift that it needs to use.

Create a new Slack app in your workspace by navigating to <https://api.slack.com/apps> and following these instructions:

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
    "redirect_urls": ["https://<your-domain>/slack_oauth"],
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
      "bot_events": ["app_uninstalled"]
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

## Configuration

The following table contains the environment variables required for the Slack integration to work:

| Environment variable      | Description                                            |
| ------------------------- | ------------------------------------------------------ |
| `SLACK_APP_CLIENT_ID`     | Corresponds to the _Client ID_ of your Slack app.      |
| `SLACK_APP_CLIENT_SECRET` | Corresponds to the _Client Secret_ of your Slack app.  |
| `SLACK_SECRET`            | Corresponds to the _Signing Secret_ of your Slack app. |
