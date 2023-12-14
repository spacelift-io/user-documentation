# Provider

What would you say if you could manage Spacelift resources - that is [stacks](../../concepts/stack/README.md), [contexts](../../concepts/configuration/context.md), [integrations](../../integrations/cloud-providers/aws.md), and [configuration](../../concepts/configuration/environment.md) - using Spacelift? We hate ClickOps as much as anyone, so we designed everything from the ground up to be easily managed using a Terraform provider. We hope that advanced users will define most of their resources programmatically.

{% if is_self_hosted() %}

## Self-Hosted Version Compatibility

The Terraform provider uses our [GraphQL API](../../integrations/api.md) to manage Spacelift, and relies on certain features being available in the API in order to work. What this can sometimes mean is that a new feature is added to the Terraform provider which hasn't yet been made available in the GraphQL API for Self-Hosted versions of Spacelift.

Because of this, it's not always possible to use the latest version of the Terraform provider with Self-Hosted, and we recommend that you pin to a known-compatible version. You can do this using a `required_providers` block like in the following example:

```terraform
terraform {
    required_providers {
        spacelift = {
            source = "spacelift-io/spacelift"
            version = "1.8.0"
        }
    }
}
```

The following table shows the latest version of the Terraform provider known to work with our Self-Hosted versions:

| Self-Hosted Version | Max Provider Version |
| ------------------- | -------------------- |
| 0.0.11              | 1.8.0                |
| 0.0.10              | 1.4.0                |
| 0.0.9               | 1.3.1                |
| 0.0.8-hotfix.1      | 1.3.1                |
| 0.0.8               | 1.3.1                |

{% endif %}

## Taking it for a spin

Our Terraform provider is open source and its [README](https://github.com/spacelift-io/terraform-provider-spacelift){: rel="nofollow"} always contains the latest available documentation. It's also distributed as part of our [Docker runner image](../../integrations/docker.md#standard-runner-image) and available through our [own provider registry](terraform-provider.md#how-it-works). The purpose of this article isn't as much to document the provider itself but to show how it can be used to incorporate Spacelift resources into your infra-as-code.

So, without further ado, let's define a stack:

```terraform title="stack.tf"
resource "spacelift_stack" "managed-stack" {
  name = "Stack managed by Spacelift"

  # Source code.
  repository = "testing-spacelift"
  branch     = "master"
}
```

That's awesome. But can we put Terraform to good use and integrate it with resources from a completely different provider? Sure we can, and we have a good excuse, too. Stacks accessibility can be managed [by GitHub teams](../../concepts/stack/README.md#access-readers-and-writers-teams), so why don't we define some?

```terraform title="stack-and-teams.tf"
resource "github_team" "stack-readers" {
  name = "managed-stack-readers"
}

resource "github_team" "stack-writers" {
  name = "managed-stack-writers"
}

resource "spacelift_stack" "managed-stack" {
  name = "Stack managed by Spacelift"

  # Source code.
  repository = "testing-spacelift"
  branch     = "master"

}
```

Now that we programmatically combine Spacelift and GitHub resources, let's add AWS to the mix and give our new stack a dedicated [IAM role](../../integrations/cloud-providers/aws.md):

```terraform title="stack-teams-and-iam.tf"
resource "github_team" "stack-readers" {
  name = "managed-stack-readers"
}

resource "github_team" "stack-writers" {
  name = "managed-stack-writers"
}

resource "spacelift_stack" "managed-stack" {
  name = "Stack managed by Spacelift"

  # Source code.
  repository = "testing-spacelift"
  branch     = "master"

}

# IAM role.
resource "aws_iam_role" "managed-stack" {
  name = "spacelift-managed-stack"

  assume_role_policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [
      jsondecode(
        spacelift_stack.managed-stack.aws_assume_role_policy_statement
      )
    ]
  })
}

# Attaching a nice, powerful policy to it.
resource "aws_iam_role_policy_attachment" "managed-stack" {
  role       = aws_iam_role.managed-stack.name
  policy_arn = "arn:aws:iam::aws:policy/PowerUserAccess"
}

# Telling Spacelift stack to assume it.
resource "spacelift_stack_aws_role" "managed-stack" {
  stack_id = spacelift_stack.managed-stack.id
  role_arn = aws_iam_role.managed-stack.arn
}
```

!!! success
    OK, so who wants to go back to clicking on things in the web GUI? Because you will likely need to do some clicking, too, [at least with your first stack](terraform-provider.md#proposed-workflow).

## How it works

Depending on whether you're using Terraform _0.12.x_ or higher, the Spacelift provider is distributed slightly differently. For _0.12.x_ users, the provider is distributed as a binary available in the [runner Docker image](../../integrations/docker.md#standard-runner-image) in the same folder we put the Terraform binary. If you're using Terraform _0.13_ and above, you can benefit from pulling our provider directly from our own provider registry. In order to do that, just point Terraform to the right location:

```terraform
provider "spacelift" {}

terraform {
  required_providers {
    spacelift = {
      source = "spacelift-io/spacelift"
    }
  }
}
```

### Using inside Spacelift

Within Spacelift, the provider is configured by an environment variable `SPACELIFT_API_TOKEN` injected into each run and task belonging to [stacks](../../concepts/stack/README.md) **marked as** [**administrative**](../../concepts/stack/README.md#administrative). This value is a bearer token that contains all the details necessary for the provider to work, including the full address of the [API endpoint](../../integrations/api.md) to talk to. It's technically valid for 3 hours but only when the [run](../../concepts/run/README.md) responsible for generating it is in [_Planning_](../../concepts/run/README.md#planning), [_Applying_](../../concepts/run/README.md#applying) or [Performing](../../concepts/run/task.md#performing) (for [tasks](../../concepts/run/task.md)) state and throughout that time it provides full administrative access to Spacelift entities [that can be managed by Terraform](terraform-provider.md#boundaries-of-programmatic-management) within the same Spacelift account.

### Using outside of Spacelift

If you want to run the Spacelift provider outside of Spacelift, or you need to manage resources across multiple Spacelift accounts from the same Terraform project, the preferred method is to generate and use dedicated [API keys](../../integrations/api.md#api-key-management). Note that unless you're just accessing whitelisted data resources, the Terraform use case will normally require marking the API key as administrative.

In order to set up the provider to use an API key, you will need the key ID, secret, and the API key endpoint:

```terraform
variable "spacelift_key_id" {}
variable "spacelift_key_secret" {}

provider "spacelift" {
  api_key_endpoint = "https://your-account.app.spacelift.io"
  api_key_id       = var.spacelift_key_id
  api_key_secret   = var.spacelift_key_secret
}
```

These values can also be passed using environment variables, though this will only work to set up the provider for a single Spacelift account:

- `SPACELIFT_API_KEY_ENDPOINT` for `api_key_endpoint`;
- `SPACELIFT_API_KEY_ID` for `api_key_id`;
- `SPACELIFT_API_KEY_SECRET` for `api_key_secret`;

If you want to talk to multiple Spacelift accounts, you just need to set up [provider aliases](https://www.terraform.io/docs/configuration/providers.html#alias-multiple-provider-configurations){: rel="nofollow"} like this:

```terraform
variable "spacelift_first_key_id" {}
variable "spacelift_first_key_secret" {}

variable "spacelift_second_key_id" {}
variable "spacelift_second_key_secret" {}

provider "spacelift" {
  alias = "first"

  api_key_endpoint = "https://first.app.spacelift.io"
  api_key_id       = var.spacelift_first_key_id
  api_key_secret   = var.spacelift_first_key_secret
}

provider "spacelift" {
  alias = "second"

  api_key_endpoint = "https://second.app.spacelift.io"
  api_key_id       = var.spacelift_second_key_id
  api_key_secret   = var.spacelift_second_key_secret
}
```

If you're running from inside Spacelift, you can still use the default, zero-setup provider for the current account with providers for accounts set up through API keys:

```terraform
variable "spacelift_that_key_id" {}
variable "spacelift_that_key_secret" {}

provider "spacelift" {
  alias = "this"
}

provider "spacelift" {
  alias = "that"

  api_key_endpoint = "https://that.app.spacelift.io"
  api_key_id       = var.spacelift_that_key_id
  api_key_secret   = var.spacelift_that_key_secret
}
```

## Proposed workflow

We suggest to first manually create a single administrative stack, and then use it to programmatically define other stacks as necessary. If you're using an integration like AWS, you should probably give the role associated with this stack **full IAM access** too, allowing it to create separate roles and policies for individual stacks.

If you want to share data or outputs between stacks, please consider programmatically creating [Stack Dependencies](../../concepts/stack/stack-dependencies.md).

!!! info
    Programmatically generated stacks can still be manually augmented, for example by setting extra elements of the environment. Thanks to the magic of Terraform, these will simply be invisible to (and thus not disturbed by) your resource definitions.

## Boundaries of programmatic management

Spacelift administrative tokens are not like user tokens. Specifically, they allow access to a much smaller subset of the [API](../../integrations/api.md#graphql-schema-s). They allow managing the lifecycles of [stacks](../../concepts/stack/README.md), [contexts](../../concepts/configuration/context.md), [integrations](../../integrations/cloud-providers/aws.md), and [configuration](../../concepts/configuration/environment.md), but they won't allow you to create or even access [Terraform state](state-management.md), [runs](../../concepts/run/README.md) or [tasks](../../concepts/run/task.md), or their associated logs.

Administrative tokens have no superpowers either. They can't read write-only configuration elements any more than you can as a user. Unlike human users with user tokens, administrative tokens won't allow you to run `env` in a [task](../../concepts/run/task.md) and read back the logs.

In general, we believe that things like runs or tasks do not fit the (relatively static) Terraform resource lifecycle model and that hiding those parts of the API from Terraform helps us ensure the integrity of potentially sensitive data - just see the example above.
