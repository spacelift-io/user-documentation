---
description: Details about all limitations when using Terragrunt stacks in spacelift.
---

# Limitations

## State management

Terragrunt is a great tool for organizing your state management configuration and allows you to easily define how you manage your state across multiple projects. However, It is not currently possible when using Terragrunt's run-all functionality to relate state files to projects in a consistent manner. For this reason Spacelift does not support storing state for Terragrunt based stacks, and you will need to maintain your own remote state backend configuration.

## Terragrunt mocked outputs

Mocked outputs in Terragrunt are placeholder values used during the development or planning phases of Terragrunt deployments.

For example, you may have a module that provides the output of a connection string to a database, but during the planning phase that database does not yet exist. In this case you would use a mocked output in Terragrunt to ensure that any dependencies that rely on this output in their planning phase have access to at least some data.

This mocked data is only used if the output does not already exist in the state. Therefore in situations such as the initial run of your stack, or the introduction of new outputs with mocked values, these mocked values will be used.

### Mocked outputs and Plan policies

Due to the nature of the mocked outputs and the way that Spacelift uses the plan data to provide the input to [plan policies](../../concepts/policy/terraform-plan-policy.md), it is possible that these mocked output values could be used as input values for your [plan policies](../../concepts/policy/terraform-plan-policy.md) and you should take precaution when writing policies that check against values that could be mocked.

### Mocked outputs and the Apply phase

Terragrunt consumes the mocked outputs and places those values within the plan file that is stored on disk as part of the planning phase. Because the plan file has the possibility of containing mocked outputs Spacelift does not use the plan files in the apply phase. This does mean there is a possibility of changes happening between the planning and applying phase, but Spacelift has taken the stance that it is more important from a security standpoint to not allow any mocked outputs to be deployed here. Nobody wants to deploy something with a mocked, hardcoded password!

## Usage of the run_cmd function

The [run_cmd](https://terragrunt.gruntwork.io/docs/reference/built-in-functions/#run_cmd) function is currently limited to only work with the `--terragrunt-quiet` flag.
Ensure this flag is included in your command to avoid run failures.

## Resource Deletion

Our Terragrunt support currently does not support resource deletion, either through the Spacelift stack destructor or the "Delete Stack" option in the UI.
