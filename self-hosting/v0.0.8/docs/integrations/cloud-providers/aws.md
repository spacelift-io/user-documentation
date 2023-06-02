---
description: >-
  This page describes Spacelift's native integration with AWS, which allows
  users to generate short-lived credentials for runs and tasks orchestrated by
  Spacelift.
---

# Amazon Web Services (AWS)

## Let's Explain

The AWS integration allows either Spacelift [runs](../../concepts/run/README.md) or [tasks](../../concepts/run/task.md) to automatically [assume an IAM role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use.html) in your AWS account, and in the process, generate a set of **temporary credentials.** These credentials are then exposed as [computed environment variables](../../concepts/configuration/environment.md#computed-values) during the run/task that takes place on the particular Spacelift stack that the integration is attached to.

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_SECURITY_TOKEN`
- `AWS_SESSION_TOKEN`

This is enough for both the [AWS Terraform provider](https://www.terraform.io/docs/providers/aws/index.html#environment-variables){: rel="nofollow"} and/or [Amazon S3 state backend](https://www.terraform.io/docs/backends/types/s3.html){: rel="nofollow"} to generate a fully authenticated AWS session without further configuration. However, you will likely need to select one of the available regions with the former.

### Usage

To utilize the AWS integration, you need to set up at least one cloud integration, and then attach that integration to any stacks that need it. Please follow the [Setup Guide](#setup-guide) for more information on this process.

## Trust Policy

When setting up a Spacelift AWS Cloud Integration you need to specify the ARN of an IAM Role to use. The Trust Policy for this role must be configured to allow Spacelift to assume the role and generate temporary credentials.

When completing the role assumption, Spacelift will pass extra information in the `ExternalId` attribute, allowing you to optionally add additional layers of security to your role.

**External ID Format:** `<spacelift-account-name>@<integration-id>@<stack-slug>@<read|write>`

- `<spacelift-account-name>`: the name of the Spacelift account that initiated the role assumption.
- `<integration-id>`: the ID of the AWS Cloud Integration that initiated the role assumption.
- `<stack-slug>`: the slug of the stack that the AWS Cloud Integration is attached to, that initiated the role assumption.
- `<read|write>`: set to either `read` or `write` based upon the event occurring that has initiated the role assumption. The [Planning phase](../../concepts/run/proposed.md#planning) utilizes `read` while the [Applying phase](../../concepts/run/tracked.md#applying) utilizes `write`.

## Setup Guide

Prerequisites:

- The ability to create IAM Roles in your AWS account.
- Admin access to your Spacelift account.

### Setup a Role in AWS

Before creating the Spacelift AWS integration, you need to have an [AWS IAM Role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html){: rel="nofollow"} within your AWS account that the cloud integration will use.

Within your AWS account, navigate to AWS IAM and click the **Create role** button.

![Within AWS IAM, click Create role](<../../assets/screenshots/Screen Shot 2022-07-21 at 2.48.55 PM.png>)

#### Configure Trust Policy

Next, we want to configure the [Trust Policy](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-custom.html){: rel="nofollow"} for the role to allow Spacelift to assume the role.

Here's an example trust policy statement you can use, that allows any stack within your Spacelift account to use this IAM Role:

```json
{
  "Version": "2012-10-17",
  "Statement": [
          {
            "Action": "sts:AssumeRole",
            "Condition": {
              "StringLike": {
                "sts:ExternalId": "yourSpaceliftAccountName@*"
              }
            },
            "Effect": "Allow",
            "Principal": {
              "AWS": "324880187172"
            }
          }
  ]
}
```

!!! info
    Be sure to replace **yourSpaceliftAccountName** in the example above with your actual Spacelift account name.

![Configure a Custom Trust Policy on the IAM Role](<../../assets/screenshots/Screen Shot 2022-07-21 at 3.25.21 PM.png>)

#### Optionally Configure Further Constraints on the Trust Policy

!!! info
    By default, Spacelift passes the `ExternalId` value in this format: `<spacelift-account-name>@<integration-id>@<stack-slug>@<read|write>`

Knowing the format of the External ID passed by Spacelift, you can further secure your IAM Role trust policies if you desire a deeper level of granular security.

For example, you may wish to lock down an IAM Role so that it can only be used by a specific stack. The following example shows how to lock down an IAM Role so that it can only be assumed by the stack `stack-a` in a Spacelift account called `example`:

```json
{
  "Version": "2012-10-17",
  "Statement": [
          {
            "Action": "sts:AssumeRole",
            "Condition": {
              "StringLike": {
                "sts:ExternalId": "example@*@stack-a@*"
              }
            },
            "Effect": "Allow",
            "Principal": {
              "AWS": "324880187172"
            }
          }
  ]
}
```

#### Configure Role Permissions

Next, you need to attach at least one IAM Policy to your IAM Role to provide it with sufficient permissions to deploy any resources that your IaC code defines.

!!! info
    For Terraform users that are managing their own state file, don't forget to give your role sufficient permissions to access your state (Terraform documents the permissions required for S3-managed state [here](https://www.terraform.io/language/settings/backends/s3#s3-bucket-permissions){: rel="nofollow"}, and for DynamoDB state locking [here](https://www.terraform.io/language/settings/backends/s3#dynamodb-table-permissions){: rel="nofollow"}).

#### Create IAM Role

Once you have your IAM Role's trust policy and IAM Policies configured, you can finish creating the role. Take a note of the IAM Role ARN, as you'll need this when setting up the integration in Spacelift in the next section.

![](../../assets/screenshots/copy-role-arn.png)

### Navigate to Cloud Integrations

Now that you have an IAM Role created, navigate to the Cloud Integration page from the Spacelift navigation sidebar.

![Navigate to the Cloud integrations page](<../../assets/screenshots/aws-add-first-role.png>)

### Create an Integration

Click the **add your first integration** button to begin the creation of your first integration.

![](<../../assets/screenshots/Screen Shot 2022-07-20 at 10.42.05 AM.png>)

When creating an integration, you will immediately notice that you need to specify two required fields: **Name** and **Role ARN.** Give the integration a name of your choosing, and paste in the ARN of the IAM Role that you just created.

If you enable the **assume role on worker** option, the role assumption will be performed on your private worker rather than at Spacelift's end. When role assumption on the worker is enabled, you can also optionally specify a custom External ID to use during role assumption.

!!! info
    **When creating your role in AWS, you need to ensure the role has a trust policy that allows Spacelift to assume the role to generate temporary credentials for runs.** Assuming you are following this guide, you should have configured this in the [previous section](#configure-trust-policy).

### Using the Integration

Now that the integration has been created, you need to attach it to one or more stacks. To do this, navigate to a stack that you want to attach your integration to:

![](<../../assets/screenshots/Screen Shot 2022-07-25 at 9.27.13 AM.png>)

Next, go to the stack's settings:

![](<../../assets/screenshots/Screen Shot 2022-07-25 at 9.29.09 AM.png>)

Choose the integrations tab:

![](<../../assets/screenshots/Screen Shot 2022-07-25 at 9.31.14 AM.png>)

Select the **AWS** option from the drop down, choose your integration, and select whether it should be used for read, write or both read and write phases:

![](<../../assets/screenshots/Screen Shot 2022-07-25 at 9.35.09 AM.png>)

!!! info
    Once you have chosen your integration and specified whether it will be used for read or write phases, an example trust relationship statement will be displayed. This shows an example of how to configure your role for use by this exact stack, and based on whether the integration is being attached for read or write phases. This policy statement is provided for convenience only, and you can safely ignore it if you have already configured your trust relationship for your role.

#### Read vs Write

You can attach an AWS integration as read, write or read-write, and you can attach at most two integrations to any single stack. **Read** indicates that this integration will be used during read phases of runs (for example, plans), and **Write** indicates that this integration will be used during write phases of runs (for example, applies).

#### Role Assumption Verification

If the Cloud Integration has the "Assume Role on Worker" setting disabled, Spacelift will verify the role assumption as soon as you click the attach button. If role assumption succeeds, it will try to assume the role **without the unique external ID**, and this time it **expects to fail**. If Spacelift fails the latter check, we consider the integration is safely configured.

!!! success
    This somewhat counterintuitive extra check is to prevent against malicious takeover of your account by someone who happens to know your AWS account ID, which isn't all that secret, really. The security vulnerability we're addressing here is known as the [_confused deputy problem_](https://en.wikipedia.org/wiki/Confused_deputy_problem){: rel="nofollow"}.

## Programmatic Setup

You can also use the [Spacelift Terraform provider](../../vendors/terraform/terraform-provider.md) in order to create an AWS Cloud integration from an [administrative stack](../../concepts/stack/README.md#administrative), including the trust relationship. Note that in order to do that, your administrative stack will require AWS credentials itself, and ones powerful enough to be able to deal with IAM.

Here's a little example of what that might look like to create a Cloud Integration programmatically:

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
    Please always refer to the [provider documentation](https://github.com/spacelift-io/terraform-provider-spacelift) for the most up-to-date documentation.

### Attaching a Role to Multiple Stacks

The previous example explained how to use the `spacelift_aws_integration_attachment_external_id` data-source to generate the assume role policy for using the integration with a single stack, but what if you want to attach the integration to multiple stacks? The simplest option would be to create multiple instances of the data-source - one for each stack - but you can also use a Terraform `for_each` condition to reduce the amount of code required:

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
                "AWS": "arn:aws:iam::324880187172:root"
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

## Is it safe?

Assuming roles and generating credentials **on the private worker** is **perfectly safe**. Those credentials are never leaked to us in any shape or form. Hence, the rest of this section discusses the trust relationship established between the Spacelift account and your AWS account for the purpose of dynamically generating short-lived credentials. So, how safe is that?

Probably safer than storing static credentials in your stack environment. Unlike user keys that you'd normally have to use, role credentials are dynamically created and short-lived. We use the default expiration which is **1 hour**, and do not store them anywhere. Leaking them **accidentally** through the logs is not an option either because we mask AWS credentials.

The most tangible safety feature of the AWS integration is the breadcrumb trail it leaves in [CloudTrail](https://aws.amazon.com/cloudtrail/){: rel="nofollow"}. Every resource change can be mapped to an individual Terraform [run](../../concepts/run/README.md) or [task](../../concepts/run/task.md) whose ID automatically becomes the username as the [`sts:AssumeRole`](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html){: rel="nofollow"} API call with that ID as `RoleSessionName`. In conjunction with AWS tools like [Config](https://aws.amazon.com/config/){: rel="nofollow"}, it can be a very powerful compliance tool.

Let's have a look at a CloudTrail event showing an IAM role being created by what seems to be a Spacelift run:

![](../../assets/screenshots/CloudTrail_Management_Console.png)

`01DSJ63P40BAZY4VW8BXXG7M4K` is indeed a run ID we can then trace back even further:

![](../../assets/screenshots/01DSJ63P40BAZY4VW8BXXG7M4K_·_End-to-end_testing.png)

## Roles assuming other roles

OK, we get it. Using everyone's favorite Inception meme:

![](../../assets/screenshots/image.png)

Indeed, the AWS Terraform provider allows you to [assume an IAM role during setup](https://www.terraform.io/docs/providers/aws/index.html#assume-role){: rel="nofollow"}, effectively doing the same thing over again. This approach is especially useful if you want to control resources in multiple AWS accounts from a single Spacelift stack. This is totally fine - in IAM, roles can assume other roles, though what you need to do on your end is set up the trust relationship between the role you have Spacelift assume and the role for each provider instance to assume. But let's face it - at this level of sophistication, you sure know what you're doing.

One bit you might not want to miss though, is the guaranteed ability to map the change to a particular [run](../../concepts/run/README.md) or [task](../../concepts/run/task.md) that we described in the [previous section](#is-it-safe). One way of fixing that would be to use the `TF_VAR_spacelift_run_id` [computed environment variable](../../concepts/configuration/environment.md#computed-values) available to each Spacelift workflow. Conveniently, it's already a [Terraform variable](https://www.terraform.io/docs/configuration/variables.html#environment-variables){: rel="nofollow"}, so a setup like this should do the trick:

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

## Migrating from "Legacy" integrations

Originally, when our AWS integration was created it did not support account-level integrations. Instead, each integration was created separately on a per-stack basis. This section provides instructions on how to migrate to the new account-level integrations, with different sets of instructions provided depending on whether you manage your integrations via the UI, or via the [Spacelift Terraform Provider](https://registry.terraform.io/providers/spacelift-io/spacelift/latest/docs).

### Via the UI

Once the new Cloud Integrations UI is enabled for your account, you will still be able to view your legacy integrations in the “Integrations” section of your stacks, but it will look slightly different:

![Legacy integration attachment](../../assets/screenshots/aws-legacy-integration-attachment.png)

The first thing to do is to copy your Role ARN, then head over to the Cloud Integrations section. Once there, click on the “Add your first integration” button to get started:

![Add your first integration](<../../assets/screenshots/aws-add-first-role.png>)

Give your role a name, and paste in your existing ARN:

![Enter ARN](../../assets/screenshots/aws-migration-create-role.png)

The role name is completely up to you and is just used for managing the roles in your account. Maybe it’s a role that allows management of S3 accounts, like in the example above, or maybe you have a single role that can manage your entire pre-production environment, in which case you might name it “Preprod Writer”.

Now that you’ve created an AWS integration, head back to your stack integration settings and click on the “Delete” button next to your legacy integration:

![Delete Integration](../../assets/screenshots/aws-migration-delete-integration.png)

Now choose the “AWS” option from the “Select integration to set up” drop down, select the AWS integration you just created, and check the read and write checkboxes:

![Attach to Stack](../../assets/screenshots/aws-migration-attach-to-stack.png)

You’ll notice that we display an example trust relationship on this screen. You may or may not need to adjust the Trust Relationship of your role at this point. If you already use a `StringLike` condition with an `<account-name>@*` wildcard you shouldn’t need to change anything.

Click on the Attach button to attach your integration to your stack:

![Role attached successfully](../../assets/screenshots/aws-migration-role-attached.png)

Congrats - you’ve now successfully migrated!

### Via the Terraform Provider

Migrating via the Terraform Provider is also very simple. The Terraform Provider now contains two new resources, along with an additional data source that you can use:

- [spacelift_aws_integration](https://registry.terraform.io/providers/spacelift-io/spacelift/latest/docs/resources/aws_integration) - creates an account level integration.
- [spacelift_aws_integration_attachment](https://registry.terraform.io/providers/spacelift-io/spacelift/latest/docs/resources/aws_integration_attachment) - attaches an integration to a stack.
- [spacelift_aws_integration_attachment_external_id](https://registry.terraform.io/providers/spacelift-io/spacelift/latest/docs/data-sources/aws_integration_attachment_external_id) - a data source that can help you generate the correct trust relationship for attaching an integration to a stack.

#### Starting Configuration

To begin with, let’s assume you have the following Terraform configuration that creates an IAM role, a Stack, and connects the role to the stack:

```hcl
resource "spacelift_stack" "this" {
 name         = "AWS Integration Mig Test"
 repository   = "spacelift-local"
 branch       = "main"
 project_root = "stacks/aws-integration-testing"
}

resource "aws_iam_role" "this" {
 name = "adamc-v1-to-v2-migration-role"

 assume_role_policy = jsonencode({
   Version   = "2012-10-17"
   Statement = [jsondecode(spacelift_stack.this.aws_assume_role_policy_statement)]
 })
}

resource "aws_iam_role_policy" "this" {
 name = aws_iam_role.this.name
 role = aws_iam_role.this.id

 policy = jsonencode({
    # Excluded for brevity })
}

resource "spacelift_aws_role" "this" {
 stack_id = spacelift_stack.this.id
 role_arn = aws_iam_role.this.arn
}
```

#### Migration

To migrate to the new integration format, we need to take the following steps:

1. Add a new AWS integration.
2. (optional) Generate an AssumeRole policy for attaching it to our stack.
3. (optional) Update the `assume_role_policy` on our `aws_iam_role` resource.
4. Remove the `spacelift_aws_role` resource.
5. Attach your new integration to your stack via the `spacelift_aws_integration_attachment` resource.

Steps 2 and 3 are completely optional, and may not be required if you are using wildcard matching for the external ID, for example.

#### Result

The following shows the finished result of the migrated Terraform:

```hcl
data "aws_caller_identity" "current" {}

# In this example, we're using some locals to calculate the role ARN. This is to avoid a circular
# dependency between the aws_iam_role resource and the spacelift_aws_integration resource.
locals {
 role_name = "adamc-v1-to-v2-migration-role"
 role_arn  = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/${local.role_name}"
}

resource "spacelift_stack" "this" {
 name         = "AWS Integration Mig Test"
 repository   = "spacelift-local"
 branch       = "main"
 project_root = "stacks/aws-integration-testing"
}

# 1. Add the new integration.
resource "spacelift_aws_integration" "this" {
 name                           = local.role_name
 role_arn                       = local.role_arn
 generate_credentials_in_worker = false
}

# 2. Generate the AssumeRole policy for attaching it to our stack.
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
     # 3. Remove the old assume role policy statement, and add our new one.
     # jsondecode(spacelift_stack.this.aws_assume_role_policy_statement),
     jsondecode(data.spacelift_aws_integration_attachment_external_id.this.assume_role_policy_statement),
   ]
 })
}

resource "aws_iam_role_policy" "this" {
 name = aws_iam_role.this.name
 role = aws_iam_role.this.id

 policy = jsonencode({
   # Excluded for brevity
 })
}

# 4. Remove the old spacelift_aws_role resource
# resource "spacelift_aws_role" "this" {
#   stack_id = spacelift_stack.this.id
#   role_arn = aws_iam_role.this.arn
# }

# 5. Add the new integration attachment
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
