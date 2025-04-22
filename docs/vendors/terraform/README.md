# OpenTofu and Terraform

## What is Terraform?

[Terraform](https://developer.hashicorp.com/terraform) is a full-featured, battle-tested Infrastructure as Code tool. It has a [vast ecosystem of providers](https://registry.terraform.io/browse/providers){: rel="nofollow"} to interact with many vendors from cloud providers such as AWS, Azure and GCP to monitoring such as New Relic and Datadog, and many many more.

There are also plenty of community-managed [modules](https://registry.terraform.io/browse/modules){: rel="nofollow"} and tools to get you started in no time.

## What is OpenTofu?

[OpenTofu](https://opentofu.org) is an open-source fork of Terraform that emerged when HashiCorp changed Terraform's license from MPL v2.0 to the Business Source License (BSL) in August 2023. It was started by a coalition of companies (including us!) to maintain a fully open-source alternative and is now managed by the Linux Foundation.

OpenTofu is fully compatible with Terraform and aims to maintain that compatibility while adding new features and improvements. It uses the same HCL configuration language, supports the same [providers](https://search.opentofu.org/providers) and [modules](https://search.opentofu.org/modules), and can work with existing Terraform state files.

For users concerned about license changes or who prefer an open-source solution backed by a vendor-neutral foundation, OpenTofu provides a compelling alternative while offering the same core functionality and ecosystem benefits as Terraform. The compatibiilty matrix between these two tools is independently maintained [here](https://cani.tf).

## Why use Spacelift with OpenTofu or Terraform?

Spacelift helps you manage the complexities and compliance challenges of using OpenTofu/Terraform. It brings with it a GitOps flow, so your infrastructure repository is synced with your OpenTofu/Terraform Stacks, and pull requests show you a preview of what they're planning to change. It also has an extensive selection of [policies](../../concepts/policy/README.md), which lets you [automate compliance checks](../../concepts/policy/terraform-plan-policy.md) and [build complex multi-stack workflows](../../concepts/policy/trigger-policy.md).

You can also use Spacelift to mix and match OpenTofu, Terraform, Pulumi, and CloudFormation Stacks and have them talk to one another. For example, you can set up OpenTofu/Terraform Stacks to provision required infrastructure (like an ECS/EKS cluster with all its dependencies) and then connect that to a CloudFormation Stack which then transactionally deploys your services there using [trigger policies](../../concepts/policy/trigger-policy.md) and the Spacelift provider [run resources](https://search.opentofu.org/provider/spacelift-io/spacelift/latest/docs/resources/run){: rel="nofollow"} for workflow orchestration and [Contexts](../../concepts/configuration/context.md#remote-state-alternative-terraform-specific) to export OpenTofu/Terraform outputs as CloudFormation input parameters.

## Does Spacelift support OpenTofu/Terraform wrappers?

Yes! We support [Terragrunt](https://terragrunt.gruntwork.io){: rel="nofollow"} and [Cloud Development Kit for Terraform (CDKTF)](https://www.terraform.io/cdktf){: rel="nofollow"}. You can read more about it in the relevant subpages of this document.

## Additional resources

- [Module registry](./module-registry.md)
- [Provider registry (beta)](./provider-registry.md)
- [External modules](./external-modules.md)
- [Provider](./terraform-provider.md)
- [State management](./state-management.md)
- [External state access](./external-state-access.md)
- [Terragrunt](./terragrunt.md)
- [Version management](./version-management.md)
- [Handling .tfvars](./handling-tfvars.md)
- [CLI Configuration](./cli-configuration.md)
- [Cost Estimation](./infracost.md)
- [Resource Sanitization](./resource-sanitization.md)
- [Storing Complex Variables](./storing-complex-variables.md)
- [Debugging Guide](./debugging-guide.md)
- [Dependency Lock File](./dependency-lock-file.md)
- [Cloud Development Kit for Terraform (CDKTF)](./cdktf.md)
