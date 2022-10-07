# Terraform

## Why use Terraform?

Terraform is a full-featured, battle-tested Infrastructure as Code tool. It has a [vast ecosystem of providers](https://registry.terraform.io/browse/providers){: rel="nofollow"} to interact with many vendors from cloud providers such as AWS, Azure and GCP to monitoring such as New Relic and Datadog, and many many more.

There are also plenty of community-managed [modules](https://registry.terraform.io/browse/modules){: rel="nofollow"} and tools to get you started in no time.

## Why use Spacelift with Terraform?

Spacelift helps you manage the complexities and compliance challenges of using Terraform. It brings with it a GitOps flow, so your infrastructure repository is synced with your Terraform Stacks, and pull requests show you a preview of what they're planning to change. It also has an extensive selection of [policies](../../concepts/policy/README.md), which lets you [automate compliance checks](../../concepts/policy/terraform-plan-policy.md) and [build complex multi-stack workflows](../../concepts/policy/trigger-policy.md).

You can also use Spacelift to mix and match Terraform, Pulumi, and CloudFormation Stacks and have them talk to one another. For example, you can set up Terraform Stacks to provision required infrastructure (like an ECS/EKS cluster with all its dependencies) and then connect that to a CloudFormation Stack which then transactionally deploys your services there using [trigger policies](../../concepts/policy/trigger-policy.md) and the Spacelift provider [run resources](https://registry.terraform.io/providers/spacelift-io/spacelift/latest/docs/resources/run){: rel="nofollow"} for workflow orchestration and [Contexts](../../concepts/configuration/context.md#remote-state-alternative-terraform-specific) to export Terraform outputs as CloudFormation input parameters.

## Does Spacelift support Terraform wrappers?

Yes! We support [Terragrunt](https://terragrunt.gruntwork.io){: rel="nofollow"} and [Cloud Development Kit for Terraform (CDKTF)](https://www.terraform.io/cdktf){: rel="nofollow"}. You can read more about it in the relevant subpages of this document.

## Additional resources

- [Module registry](./module-registry.md)
- [External modules](./external-modules.md)
- [Provider](./terraform-provider.md)
- [State management](./state-management.md)
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
