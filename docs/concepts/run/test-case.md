# Module test case

Module test cases are special types of runs that are executed not on [Stacks](../stack/README.md) but on Spacelift-managed [Terraform modules](../../vendors/terraform/module-registry.md). Note that this article does not cover modules specifically - for that please refer directly to [their documentation](../../vendors/terraform/module-registry.md). The purpose of this article is to explain how modules test cases are executed and how they're different from other types of runs.

In a nutshell, module test cases are almost identical to [autodeployed](../stack/stack-settings.md#autodeploy) [tracked runs](tracked.md). But unlike stacks, modules are stateless and do not manage any resources directly, so just after the changes are applied and resources are created, they are immediately destroyed during the _destroying_ phase. Here is what a fully successful module test case looks like:

![](../../assets/screenshots/run/finished-module-run.png)

Note that the destroying phase will run regardless of whether the applying phase succeeds or fails. This is because the failure could have been partial, and some resources may still have been created.

The destroying phase can be skipped without execution by setting the `SPACELIFT_SKIP_DESTROYING` environment variable to _true_ in the stack's [environment variables](../stack/stack-settings.md#environment-variables).

## Success criteria

A module test case will only transition to the successful [finished](./README.md#finished) state if all the previous phases succeed. If any of the phases fails, the run will be marked as [failed](./README.md#failed).
