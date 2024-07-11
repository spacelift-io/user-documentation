---
description: Managing Terragrunt Stacks through Spacelift.
---
# Terragrunt

!!! warning
    Terragrunt support is currently in **beta** and has some important limitations to take into consideration. Please see our documentation [here](limitations.md) for more information.

## Why use Terragrunt?

Terragrunt serves as a valuable companion to Terraform, functioning as a thin wrapper that offers a suite of additional tools, ultimately enhancing the management and deployment of your infrastructure configurations.

### Improved Management of Configurations

Working with complex Terraform configurations often becomes challenging. Terragrunt intervenes here by offering a structured approach to managing these configurations. It also provides you with a mechanism to manage dependencies between various infrastructure components effectively.

### Efficient Handling of Remote State

In an infrastructure setup, managing remote state and its associated configurations is critical. Terragrunt brings in utilities that can handle remote state locking and configuration adeptly, effectively reducing the chances of race conditions and configuration errors.

### Enhanced Reusability and Maintainability

If you're working with Infrastructure-as-Code (IaC) across multiple environments, Terragrunt's capability to reuse configurations can be a game-changer. This not only simplifies the management process but also makes the infrastructure deployments more maintainable.

All these features combine to offer enhanced efficiency and reliability in your infrastructure deployments when using Terragrunt.

## Why use Spacelift with Terragrunt?

Integrating Spacelift with Terragrunt yields a robust and streamlined solution for Infrastructure-as-Code (IaC) management and deployment. Spacelift's platform is designed for IaC and therefore greatly complements Terragrunt's capabilities.

Firstly, Spacelift's automation capabilities can bring significant benefits when paired with Terragrunt. You can automate and streamline the deployment of your complex Terraform configurations managed by Terragrunt, making your infrastructure management efficient and seamless.

Spacelift provides a centralized platform for managing your IaC setup. Combined with Terragrunt's ability to effectively handle complex Terraform configurations and dependencies, you end up with a well-organized and optimized IaC environment that is easier to navigate and manage.

Lastly, Spacelift is designed to integrate smoothly with your existing tech stack. Its compatibility with Terragrunt means that it can fit into your existing workflow without requiring substantial changes, ensuring a smooth transition and consistent operations.

## Additional Resources

- [Getting Started](getting-started.md)
- [Run-all](run-all.md)
- [Limitations](limitations.md)
- [Terragrunt Tool](terragrunt-tool.md)
- [Reference](reference.md)
