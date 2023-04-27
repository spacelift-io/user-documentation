# Slack configuration

First, create a new Slack app in your workspace by navigating to [https://api.slack.com/apps](https://api.slack.com/apps) and following these instructions:

- Click "Create New App"
- Choose "From an app manifest"
- Select your workspace
- Paste following manifest, replacing with the domain you want to host the self-hosted Spacelift instance on.

```yaml
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

Next, when running the installation script, you will be asked whether you'd like to configure the Slack App. Type "yes" and when asked for specific values copy them from the "Basic Information" tab of your Slack App.

After the installation script finishes. You can now go to your selfhosted Spacelift instance, to **Settings** -> **Slack** and install the Slack app into your workspace.
