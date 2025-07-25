---
description: Details about using run-all based Terragrunt stacks in spacelift.
---

# Using Run-All

## Introduction

Terragrunt's [run-all](https://terragrunt-v1.gruntwork.io/docs/reference/hcl/functions/#run_cmd){: rel="nofollow"} feature allows you to deploy multiple modules at the same time. This very powerful feature allows you to develop large amounts of infrastructure as code with dependencies, mocked values, and while keeping things [DRY](https://terragrunt.gruntwork.io/docs/features/keep-your-terraform-code-dry/){: rel="nofollow"}.

## How to use run-all

When creating a stack in Spacelift, you can enable the **Use Run All** property to start using this functionality natively in your own stacks:

![Terragrunt stack creation screen](../../assets/screenshots/terragrunt/run-all/run-all-toggle.png)

When this option is enabled, Spacelift will run all Terragrunt commands with the `run-all` option, taking into account any dependencies between your projects!

!!! Tip
    When using Terragrunt run-all, we recommend setting the [TERRAGRUNT_PARALLELISM](https://terragrunt.gruntwork.io/docs/reference/cli-options/#terragrunt-parallelism){: rel="nofollow"} variable to optimize CPU usage by adjusting the number of tasks processed concurrently, aligning with the capacity of our public workers and preventing worker crashes from overloaded resources.

    If additional parallelism is needed to meet your specific requirements, consider using our [private workers](../../concepts/worker-pools/README.md).

## Why are my resources named strangely?

![Screenshot of run changes across a run-all Terragrunt stack](../../assets/screenshots/terragrunt/run-all/run-all-changes.png)
Due to the way Terragrunt works, you may find that modules and projects create outputs or resources with the same names, and we want to make sure that you can determine the origin of all of your resources without getting confused about "Which project created `output.password`"?

For this reason, we prepend the addresses of your outputs and resources in the Spacelift user interface with the project they originated from. This allows you to keep on top of your resources, understand at a glance how things were created, and identify issues faster, Giving you more control and visibility over the resources you create!
