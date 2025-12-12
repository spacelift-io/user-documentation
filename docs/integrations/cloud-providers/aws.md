---
description: >-
  This page describes Spacelift's native integration with AWS, which allows
  users to generate short-lived credentials for runs and tasks orchestrated by
  Spacelift.
---

# Amazon Web Services (AWS)

The AWS integration allows Spacelift [runs](../../concepts/run/README.md) or [tasks](../../concepts/run/task.md) to automatically [assume an IAM role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use.html){: rel="nofollow"} in your AWS account, and in the process, generate a set of _temporary credentials_. These credentials are then exposed as [computed environment variables](../../concepts/configuration/environment.md#computed-values) during the run/task that takes place on the Spacelift stack where the integration is attached.

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_SECURITY_TOKEN`
- `AWS_SESSION_TOKEN`

These temporary credentials are enough for both the [AWS Terraform provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#environment-variables){: rel="nofollow"} and the [Amazon S3 state backend](https://www.terraform.io/docs/backends/types/s3.html){: rel="nofollow"} to generate a fully authenticated AWS session without further configuration.

To use the AWS integration, you need to set it up and attach it to any stacks that need it.

## Spacelift UI setup

See [Integrate Spacelift with Amazon Web Services](../../getting-started/integrate-cloud/AWS.md) to configure your AWS IAM role, trust policy, and the integration within Spacelift.

## Programmatic setup

You can also use the [Spacelift Terraform provider](../../vendors/terraform/terraform-provider.md) in order to create an AWS Cloud integration from a [stack with Space admin role attachment](../../concepts/authorization/assigning-roles-stacks.md), including the trust relationship. Note that in order to do that, your stack will require AWS credentials itself, and ones powerful enough to be able to deal with IAM.

Here's an example of what it might look like to create an AWS cloud integration programmatically:

```terraform
data "aws_caller_identity" "current" {}

locals {
  role_name = "example-role"
  role_arn  = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/${local.role_name}"
}

resource "spacelift_stack" "this" {
  name         = "Example Stack"
  repository   = "your-awesome-repo"
  branch       = "main"
}

resource "spacelift_aws_integration" "this" {
  name = local.role_name

  # We need to set this manually rather than referencing the role to avoid a circular dependency
  role_arn                       = local.role_arn
  generate_credentials_in_worker = false
}

# The spacelift_aws_integration_attachment_external_id data source is used to help generate a trust policy for the integration
data "spacelift_aws_integration_attachment_external_id" "this" {
  integration_id = spacelift_aws_integration.this.id
  stack_id       = spacelift_stack.this.id
  read           = true
  write          = true
}

resource "aws_iam_role" "this" {
  name = local.role_name

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      jsondecode(data.spacelift_aws_integration_attachment_external_id.this.assume_role_policy_statement),
    ]
  })
}

resource "aws_iam_role_policy_attachment" "this" {
  policy_arn = "arn:aws:iam::aws:policy/PowerUserAccess"
  role       = aws_iam_role.this.name
}

resource "spacelift_aws_integration_attachment" "this" {
  integration_id = spacelift_aws_integration.this.id
  stack_id       = spacelift_stack.this.id
  read           = true
  write          = true

  # The role needs to exist before we attach since we test role assumption during attachment.
  depends_on = [
    aws_iam_role.this
  ]
}
```

!!! info
    Please always refer to the [provider documentation](https://github.com/spacelift-io/terraform-provider-spacelift){: rel="nofollow"} for the most up-to-date documentation.

### Attach a role to multiple stacks

The previous example explained how to use the `spacelift_aws_integration_attachment_external_id` data-source to generate the assume role policy for using the integration with a single stack, but what if you want to attach the integration to multiple stacks? The simplest option would be to create multiple instances of the data-source (one for each stack) but you can also use a Terraform `for_each` condition to reduce the amount of code required:

```terraform
locals {
  role_name        = "multi-stack-integration"
  role_arn         = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/${local.role_name}"

  # Define the stacks we want to attach the integration to
  stacks_to_attach = ["stack-1", "stack-2", "stack-3"]
}

data "aws_caller_identity" "current" {}
data "spacelift_account" "current" {}

resource "spacelift_aws_integration" "integration" {
  name = local.role_name
  role_arn                       = local.role_arn
  generate_credentials_in_worker = false
}

# Generate the External IDs required for creating our AssumeRole policy
data "spacelift_aws_integration_attachment_external_id" "integration" {
  for_each = toset(local.stacks_to_attach)

  integration_id = spacelift_aws_integration.integration.id
  stack_id       = each.key
  read           = true
  write          = true
}

resource "aws_iam_role" "role" {
  name = local.role_name

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow",
        "Principal" = {
          "AWS" : data.spacelift_account.current.aws_account_id
        },
        "Action" = "sts:AssumeRole",
        "Condition" = {
          "StringEquals" = {
            # Allow the external ID for any of the stacks to assume our role
            "sts:ExternalId" = [for i in values(data.spacelift_aws_integration_attachment_external_id.integration) : i.external_id],
          }
        }
      }
    ],
  })
}
```

This will generate a trust relationship that looks something like this:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::<principal>:root"
            },
            "Action": "sts:AssumeRole",
            "Condition": {
                "StringEquals": {
                    "sts:ExternalId": [
                        "spacelifter@01GE7K9SR2DQBCRQ90DH70JF6Y@stack-1@write",
                        "spacelifter@01GE7K9SR2DQBCRQ90DH70JF6Y@stack-2@write",
                        "spacelifter@01GE7K9SR2DQBCRQ90DH70JF6Y@stack-3@write"
                    ]
                }
            }
        }
    ]
}
```

{% if is_saas() %}
!!! info

    Make sure to replace:

    - `spacelifter` with your actual Spacelift account name.
    - `<principal>` based on your environment:
        - for [spacelift.io](https://spacelift.io), use `324880187172`.
        - for [us.spacelift.io](https://us.spacelift.io), use `577638371743`.
{% endif %}

## Auto-attach integrations

AWS integrations can now be auto-attached to stacks and modules. To do so, include a label in your integration following this format `autoattach:<your_label>`. Then select the `Enable auto-attach` toggle and click `Set up`.

![](<../../assets/screenshots/integrations/cloud-providers/aws/auto-attach-aws-form.png>)

You will immediately see the stacks and modules that already have your label in the Auto-attached section. To auto-attach your new integration to another stack or module, simply add `<your_label>` to it and we will attach the integration for you. This follows the same behavior as other _auto-attachable_ resources.

![](<../../assets/screenshots/integrations/cloud-providers/aws/auto-attach-aws-list.png>)

!!! info
    You have to enable auto-attach on each integration individually to prevent clashes with previous labels in your account.

## Are my credentials safe?

Assuming roles and generating credentials **on private worker** is perfectly safe. Those credentials are never leaked to us in any shape or form.

As for the trust relationship established between the Spacelift account and your AWS account for the purpose of dynamically generating short-lived credentials, this is considered much safer than storing static credentials in your stack environment. Unlike user keys that you'd normally have to use, role credentials are dynamically created and short-lived. We use the default expiration which is **1 hour**, and do not store them anywhere. Leaking them **accidentally** through the logs is not an option either because we mask AWS credentials.

The most tangible safety feature of the AWS integration is the breadcrumb trail it leaves in [CloudTrail](https://aws.amazon.com/cloudtrail/){: rel="nofollow"}. Every resource change can be mapped to an individual Terraform [run](../../concepts/run/README.md) or [task](../../concepts/run/task.md) whose ID automatically becomes the username as the [`sts:AssumeRole`](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html){: rel="nofollow"} API call with that ID as `RoleSessionName`. In conjunction with AWS tools like [Config](https://aws.amazon.com/config/){: rel="nofollow"}, it can be a very powerful compliance tool.

Let's have a look at a CloudTrail event showing an IAM role being created by what seems to be a Spacelift run:

![](<../../assets/screenshots/integrations/cloud-providers/aws/cloud-trail-management-console.png>)

`01DSJ63P40BAZY4VW8BXXG7M4K` is a run ID we can then trace back even further.

## Roles assuming other roles

The AWS Terraform provider allows you to [assume an IAM role during setup](https://www.terraform.io/docs/providers/aws/index.html#assume-role){: rel="nofollow"}, effectively doing the same thing over again. This approach is especially useful if you want to control resources in multiple AWS accounts from a single Spacelift stack. This is totally fine; in IAM, roles can assume other roles, though you need to set up the trust relationship between the role you have Spacelift assume and the role for each provider instance to assume.

One thing you want to watch is the guaranteed ability to map the change to a particular [run](../../concepts/run/README.md) or [task](../../concepts/run/task.md) that we described in the [previous section](#are-my-credentials-safe). One way of fixing this would be to use the `TF_VAR_spacelift_run_id` [computed environment variable](../../concepts/configuration/environment.md#computed-values) available to each Spacelift workflow. It's already a [Terraform variable](https://www.terraform.io/docs/configuration/variables.html#environment-variables){: rel="nofollow"}, so you can set it up like this:

```terraform
variable "spacelift_run_id" {}

# That's our default provider with credentials generated by Spacelift.
provider "aws" {}

# That's where Terraform needs to run sts:AssumeRole with your
# Spacelift-generated credentials to obtain ones for the second account.
provider "aws" {
  alias = "second-account"

  assume_role {
    role_arn     = "<up-to-you>"
    session_name = var.spacelift_run_id
    external_id  = "<up-to-you>"
  }
}
```
