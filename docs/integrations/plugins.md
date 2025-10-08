# Plugins

!!! warning
    Plugins support is currently in closed **beta** while we ensure stability of the platform and API's. Reach out to your Spacelift CSM for access.

Plugins are a way to extend the functionality of Spacelift.
They allow you to integrate with third-party services, automate tasks, and enhance your workflows.
Spacelift supports a variety of plugins, which can be used to perform actions such as sending notifications, managing resources, or integrating with external systems.
You can also develop your own custom plugins using our plugin SDK [spaceforge](https://github.com/spacelift-io/plugins)

## Available Plugins

Navigate to the Plugins -> Templates section in the Spacelift UI to see the available plugins.

![templates_home.png](../assets/screenshots/integrations/plugins/templates_home.png)

You're able to search for plugins on this screen and install it into your account.
You can also create plugins yourself using the `Create Template` button.

### Infracost

The [Infracost](https://www.infracost.io/) plugin helps you estimate the cost impact of your Terraform infrastructure changes before they're deployed.

**Use Cases:**

- Get cost estimates for pull requests and plan changes
- Set budget alerts and cost thresholds
- Compare costs across different infrastructure configurations
- Generate cost reports for stakeholders

**Prerequisites:**

- [Infracost API key](https://www.infracost.io/docs/#2-get-api-key) from your Infracost account
- Terraform configurations with supported cloud providers (AWS, Azure, GCP)

**Troubleshooting:**

- **API key issues**: Ensure your Infracost API key is valid and has sufficient quota
- **Unsupported resources**: Check [Infracost's supported resources](https://www.infracost.io/docs/supported_resources/) list
- **Network connectivity**: Ensure your workers can reach Infracost API endpoints

### SOPS

The [SOPS](https://sops.github.io/) plugin enables secure secret management by encrypting/decrypting files during your Terraform runs.

**Use Cases:**

- Decrypt encrypted Terraform variable files
- Manage secrets across multiple environments
- Integrate with cloud KMS services (AWS KMS, Azure Key Vault, GCP KMS)
- Maintain encrypted secrets in version control

**Prerequisites:**

- SOPS-encrypted files in your repository
- Appropriate cloud credentials for your chosen encryption backend
- SOPS configuration file (`.sops.yaml`) in your repository

**Sample .sops.yaml:**

```yaml
creation_rules:
  - path_regex: \.dev\.tf$
    kms: 'arn:aws:kms:us-east-1:123456789012:key/dev-key-id'
  - path_regex: \.prod\.tf$
    kms: 'arn:aws:kms:us-east-1:123456789012:key/prod-key-id'
```

**Troubleshooting:**

- **Permission errors**: Verify IAM roles have KMS decrypt permissions
- **File format issues**: Ensure encrypted files are in supported formats (YAML, JSON, dotenv)
- **Key rotation**: Update SOPS configuration when rotating encryption keys

### WIZ

The [WIZ](https://www.wiz.io/) plugin integrates cloud security scanning into your infrastructure deployment pipeline.

**Use Cases:**

- Scan infrastructure configurations for security vulnerabilities
- Enforce security policies before deployment
- Generate security compliance reports
- Identify misconfigurations and policy violations

**Prerequisites:**

- WIZ platform account and API credentials
- Cloud resources configured for WIZ scanning
- Security policies defined in WIZ platform

**Plan Policy Integration:**

The plugin can be configured to fail runs based on:

- Critical security findings
- Policy compliance violations
- Risk score thresholds
- Specific vulnerability types

Simply write your plan policy to use the `input.third_party_metadata.custom.wiz` object.

**Troubleshooting:**

- **Authentication failures**: Verify WIZ API credentials are correct and active
- **Scan timeouts**: Increase timeout values for large infrastructure scans
- **Policy conflicts**: Review WIZ policy configurations if scans are failing unexpectedly

### Changing the plugin template

Some plugin templates come with default values that you might want to change.
Note that when a template is installed, the resulting policies, webhooks, contexts, etc will be locked in the UI.
Management of these resources is done via the plugins screen.

So to change a plugin template, you can click the "..." button next to the plugin template and select "New template from this".
![new_template_from_this.png](../assets/screenshots/integrations/plugins/new_template_from_this.png)

After that, you can create a new template with the desired changes and install that into your account.

## Installing Plugins

To install a plugin, navigate to the Plugins -> Templates section in the Spacelift UI and click "..." -> Install.
When installing a plugin you will be provided a number of options.

- `Installation Name` is the name of the plugin installation. This is used to identify the plugin in the Spacelift UI.
- `Stack Label` is the `autoattach` label that will be used to automatically attach the plugin to stacks.
- `Space` is the space where the plugin will be installed. This is used to scope the plugin to a specific space.
- `labels` are arbitrary labels that can be used to filter in the Spacelift UI.

Below the options, you will see dynamically configured options that are pulled in from the template.
For instance, the Infracost plugin template has the `Infracost API Key` option, which is required to use the plugin.
If you need more information about what a specific paramenter is doing hover over the information icon.

![install_plugin.png](../assets/screenshots/integrations/plugins/install_plugin.png)

After a plugin is installed, it will move to the `Account Plugins` tab where you can see details about that specific plugin.

## Using a plugin

Using a plugin is very simple, plugins can **only** attach via the `autoattach` label.
The value you provided in the `Stack Label` field will be used as the `autoattach` label.
If you installed Infracost with the `infracost` stack label, you can attach it to a stack by adding the `infracost` label to the stack.
You can also use the `*` wildcard in the stack label to attach the plugin to all stacks in a space.

## Plugin Outputs

Plugins may output information that is useful for you to see. If a plugin produces outputs, they will be visible in the `Plugin Outputs` tab of the run details page.
An example of the `Wiz` plugin output is shown below:

![plugin_outputs.png](../assets/screenshots/integrations/plugins/plugin_outputs.png)

## Plugin Development

### Getting Started with Custom Plugins

Custom plugins allow you to extend Spacelift's functionality to meet your specific needs. The [spaceforge](https://github.com/spacelift-io/plugins) SDK provides templates and tools for creating, testing, and publishing plugins.

### Plugin Architecture

Spacelift plugins are packaged as yaml files. Each plugin defines:

- **Execution phases**: When the plugin runs (e.g., before_init, after_plan, after_apply)
- **Input parameters**: Configuration options exposed during installation
- **Output artifacts**: Files, logs, or data produced by the plugin
- **Dependencies**: Required tools, libraries, or external services

### Plugin Lifecycle

1. **Installation**: Plugin template is installed into your account with specific configuration
2. **Attachment**: Plugin automatically attaches to stacks via autoattach labels
3. **Execution**: Plugin runs during appropriate run phases based on its configuration
4. **Output**: Plugin generates logs, artifacts, or external integrations
5. **Cleanup**: Temporary resources are cleaned up after execution

### Contributing to the Plugin Ecosystem

#### Community Contributions

The Spacelift plugin ecosystem thrives on community contributions. Here's how you can get involved:

**Plugin Templates:**

- Contribute new plugin templates to the [spaceforge repository](https://github.com/spacelift-io/plugins)
- Improve existing plugin documentation and examples
- Submit bug fixes and feature enhancements

**Contribution Process:**

1. **Fork the repository**: Create your own fork of the spaceforge repo
2. **Create feature branch**: `git checkout -b feature/my-awesome-plugin`
3. **Develop and test**: Follow the development guidelines and test thoroughly
4. **Submit pull request**: Include clear description and test results
5. **Review process**: Core maintainers will review and provide feedback

#### Plugin Submission Guidelines

**Quality Standards:**

- **Documentation**: Comprehensive README with setup instructions
- **Security**: Follow security best practices, no hardcoded secrets
- **Compatibility**: Test with supported Spacelift features and IaC tool versions

#### Plugin Categories

**Popular Plugin Categories:**

- **Security & Compliance**: Vulnerability scanning, policy enforcement, compliance reporting
- **Cost Management**: Cost estimation, budget alerts, resource optimization
- **Notifications**: Slack, Discord, email, webhooks for run status updates
- **Monitoring & Observability**: Metrics collection, log aggregation, alerting
- **CI/CD Integration**: GitHub Actions, GitLab CI, Jenkins pipeline triggers
- **Cloud Services**: Provider-specific integrations and automation
- **Testing**: Infrastructure testing, compliance validation, performance testing
