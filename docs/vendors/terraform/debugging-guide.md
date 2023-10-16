---
 description: Describes methods of debugging Terraform and Terragrunt on Spacelift.
---

# Debugging Guide

## Setting Environment Variables

Environment variables are commonly used for enabling advanced logging levels for Terraform and Terragrunt. There are two ways environment variables can be set for runs.

1. Set Environment Variable(s) directly on a Stack's [Environment](../../concepts/configuration/environment.md) (easiest method).

2. Set Environment Variable(s) in a [Context](../../concepts/configuration/context.md), and then attach that Context to your Spacelift Stack(s).

## Terraform Debugging

Terraform providing an advanced logging mode that can be enabled using the `TF_LOG` environment variable. As of the writing of this documentation, `TF_LOG` has 5 different logging levels: `TRACE` `DEBUG` `INFO` `WARN` and `ERROR`

Please refer to the [Setting Environment Variables](./debugging-guide.md#setting-environment-variables-for-debugging) section for more information on how to set these variables on your Spacelift Stack(s).

For more information on Terraform logging, please refer directly to the Terraform [documentation](https://www.terraform.io/internals/debugging){: rel="nofollow"}.

## Terragrunt Debugging

Please refer to the [Debugging Terragrunt](./terragrunt.md#debugging-terragrunt) section of our Terragrunt documentation.
