# Stack

_Stack_ is one of the core concepts in Spacelift. A stack is an isolated, independent entity and the choice of the word mirrors products like [AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacks.html){: rel="nofollow"}, or [Pulumi](https://www.pulumi.com/docs/intro/concepts/stack/){: rel="nofollow"} (of which we support both). You can think about a stack as a combination of source code, current state of the managed infrastructure (eg. Terraform state file) and configuration in the form of [environment](../configuration/environment.md) variables and mounted files.

Unless you're using Spacelift only to host and test private [Terraform modules](../../vendors/terraform/module-registry.md), your account should probably contain one or more stacks to be of any use. For example:

![](<../../assets/screenshots/Screen Shot 2022-06-29 at 2.47.11 PM.png>)

Here's a few helpful articles about stacks:

- In [this article](creating-a-stack.md), you can learn how to create a new stack;
- [Here](stack-settings.md) you can see all the settings that are available for the stack;
- [Here](stack-locking.md#stack-locking) you can learn about stack locking;

## Stack state

Similar to [runs](../run/README.md) and [tasks](../run/task.md), stacks also have states.
A stack's state is the last state of its most recently processed [tracked run](../run/README.md#where-do-runs-come-from) that has progressed beyond the [queued](../run/README.md#queued) state and which was not [canceled](../run/README.md#canceled).
Only if the stack has no runs yet a special state "None" is applied:

![](<../../assets/screenshots/Stacks_·_spacelift-io (1).png>)

Stack states allow users to see at a glance the overall health of their infrastructure, and the level of development activity associated with it.
