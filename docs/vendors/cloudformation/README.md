---
description: Managing CloudFormation Stacks through Spacelift.
---

# AWS CloudFormation

You can find more details in the subpages:

- [Getting Started](getting-started.md)
- [Reference](reference.md)
- [Integrating with AWS Serverless Application Model (SAM)](integrating-with-sam.md)
- [Integrating with the Serverless Framework](integrating-with-the-serverless-framework.md)

## Why use CloudFormation?

CloudFormation is an excellent Infrastructure-as-Code tool that supports transactional deploys (automatically rolling back on failure), has a rich construct library, and does not require separate state management like Terraform or Pulumi.

Even if you don't want to write YAML/JSON files directly, there are multiple frameworks that let you write your CloudFormation config in more ergonomic, general-purpose languages.

## Why use Spacelift with CloudFormation?

Spacelift helps you manage the complexities and compliance challenges of using CloudFormation. It brings with it a GitOps flow, so your infrastructure repository is synced with your CloudFormation Stacks, and pull requests show you a preview of what they're planning to change. It also has an extensive selection of [policies](../../concepts/policy/README.md), which lets you [automate compliance checks](../../concepts/policy/terraform-plan-policy.md) and [build complex multi-stack workflows](../../concepts/policy/trigger-policy.md).

You can also use Spacelift to mix and match OpenTofu/Terraform, Pulumi, and CloudFormation Stacks and have them talk to one another. For example, you can set up OpenTofu Stacks to provision required infrastructure (like an ECS/EKS cluster with all its dependencies) and then connect that to a CloudFormation Stack which then transactionally deploys your services there using [trigger policies](../../concepts/policy/trigger-policy.md) and the Spacelift provider [run resources](https://search.opentofu.org/provider/spacelift-io/spacelift/latest/docs/resources/run){: rel="nofollow"} for workflow orchestration and [Contexts](../../concepts/configuration/context.md#remote-state-alternative-terraform-specific) to export OpenTofu outputs as CloudFormation input parameters.

## Does Spacelift support CloudFormation frameworks?

Yes! We support [AWS CDK](https://github.com/aws/aws-cdk){: rel="nofollow"}, [AWS Serverless Application Model (SAM)](https://aws.amazon.com/serverless/sam/){: rel="nofollow"}, and the [Serverless Framework](https://www.serverless.com/){: rel="nofollow"}. You can read more about it in the relevant subpages of this document.

## Template bucket limitations

Spacelift uses a user-provided S3 bucket to upload templates to as part of applying your changes. When creating this bucket, please make sure that the bucket name does not contain any periods (`.`). Using a bucket name containing periods will cause the template upload to fail.
