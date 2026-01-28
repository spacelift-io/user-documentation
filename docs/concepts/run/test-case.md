# Module test case

Module test cases are special types of runs that are executed on Spacelift-managed [OpenTofu/Terraform modules](../../vendors/terraform/module-registry.md) instead of [stacks](../stack/README.md). The purpose of this article is to explain how modules test cases are executed and how they're different from other types of runs.

Module test cases are almost identical to [autodeployed](../stack/stack-settings.md#autodeploy) [tracked runs](tracked.md). But unlike stacks, modules are stateless and do not manage any resources directly, so just after the changes are applied and resources are created, they are immediately destroyed during the _destroying_ phase. Here is what a fully successful module test case looks like:

![Finished module run](<../../assets/screenshots/run/finished-module-run.png>)

The destroying phase will run regardless of whether the applying phase succeeds or fails. This is because the failure could have been partial, and some resources may still have been created.

The destroying phase can be skipped without execution by setting the `SPACELIFT_SKIP_DESTROYING` environment variable to _true_ in the stack's [environment variables](../stack/stack-settings.md).

## Success criteria

!!! note
    Make sure to attach the integration for the cloud provider if your module is for a cloud provider.

A module test case will only transition to the successful [finished](./README.md#finished) state if all the previous phases succeed. If any of the phases fails, the run will be marked as [failed](./README.md#failed).
