# Policy Flag Reset

Policies can now reset flags they have previously set using the `reset_flag` rule.

## Basic usage

=== "Rego v1"
    ```opa
    package spacelift

    # Set a flag when creating S3 buckets
    flag contains "s3-review" if {
        some resource in input.terraform.resource_changes
        resource.type == "aws_s3_bucket"
    }

    # Reset the flag when no S3 buckets are being created
    reset_flag contains "s3-review" if {
        not has_s3_bucket
    }

    has_s3_bucket if {
        some resource in input.terraform.resource_changes
        resource.type == "aws_s3_bucket"
    }
    ```

=== "Rego v0"
    ```opa
    package spacelift

    # Set a flag when creating S3 buckets
    flag["s3-review"] {
        input.terraform.resource_changes[_].type == "aws_s3_bucket"
    }

    # Reset the flag when no S3 buckets are being created
    reset_flag["s3-review"] {
        not input.terraform.resource_changes[_].type == "aws_s3_bucket"
    }
    ```

## Multi-owner security

- Multiple policies can own the same flag when they all set it
- **ALL owners must agree** to reset a flag for it to be removed
- Prevents malicious policies from hijacking flags set by other policies

## Processing order

Within each policy evaluation:

1. Reset flags are processed first
2. Add flags are processed second

## Legacy policies

Policies without PolicyULID can set flags but cannot reset any flags.

## Use with targeted replans

Flag reset is particularly useful during [targeted replans](../run/tracked.md#targeted-replan), where plan and approval policies can be evaluated multiple times within the same run as the plan changes. Policies can dynamically set and reset flags based on the current plan content, allowing for adaptive approval workflows that respond to the actual changes being deployed.

## Supported policy types

Available in [push](push-policy/README.md), [approval](approval-policy.md), [plan](terraform-plan-policy.md), and [trigger](trigger-policy.md) policies.
