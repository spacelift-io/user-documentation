# Context

## Introduction

On a high level, context is a bundle of configuration elements ([environment variables](environment.md#environment-variables) and [mounted files](environment.md#mounted-files)) independent of any [stack](../stack/) that can be managed separately and [attached](context.md#attaching-a-context) to as many or as few stacks as necessary. Contexts are only directly accessible to administrators from the account view:

![](../../assets/screenshots/Contexts\_·\_marcinwyszynski.png)

The list of contexts merely shows the name and description of the context. Clicking on the name allows you to [edit it](context.md#editing-a-context).

## Management

Managing a context is quite straightforward - you can [create](context.md#creating), [edit](context.md#editing), [attach, detach](context.md#attaching-and-detaching) and [delete](context.md#deleting) it. The below paragraphs will focus on doing that through the web GUI but doing it programmatically using [our Terraform provider](../../vendors/terraform/terraform-provider.md) is an attractive alternative.

### Creating

As an account administrator you can create a new context from the Contexts screen as seen on the above screenshot by pressing the Add context button:

![](<../../assets/screenshots/Contexts\_·\_marcinwyszynski (1).png>)

This takes you to a simple form where the only inputs are name and description:

![](../../assets/screenshots/New\_context\_·\_marcinwyszynski.png)

The required _name_ is what you'll see in the context list and in the dropdown when attaching the context. Make sure that it's informative enough to be able to immediately communicate the purpose of the context, but short enough so that it fits nicely in the dropdown, and no important information is cut off.

The optional _description_ is completely free-form and it supports [Markdown](https://daringfireball.net/projects/markdown/). This is a good place perhaps for a thorough explanation of the purpose of the stack, perhaps a link or two, and/or a funny GIF. In the web GUI this description will only show on the Contexts screen so it's not a big deal anyway.

!!! warning
    Based on the original _name_, Spacelift generates an immutable slug that serves as a unique identifier of this context. If the name and the slug diverge significantly, things may become confusing.\
    \
    So even though you can change the context name at any point, we strongly discourage all non-trivial changes.

### Editing

Editing the context is only a little more exciting. You can edit the context from its dedicated view by pressing the Edit button:

![](../../assets/screenshots/Managed\_context\_·\_marcinwyszynski.png)

This switches the context into editing mode where you can change the name and description but also manage configuration elements the same way you'd do for the [stack environment](environment.md), only much simpler - without overrides and [computed values](environment.md#computed-values):

![](../../assets/screenshots/Editing\_Managed\_context\_·\_marcinwyszynski.png)

### Attaching and detaching

Attaching and detaching contexts actually happens from the [stack](../stack/) management view. To attach a context, select the Contexts tab. This should show you a dropdown with all the contexts available for attaching, and a slider to set the [priority of the attachment](context.md#a-note-on-priority):

![](<../../assets/screenshots/Edit\_stack\_·\_Managed\_stack (1).png>)

!!! info
    A context can only be attached once to a given stack, so if it's already attached, it will not be visible in the dropdown menu.

OK, let's attach the context with priority 0 and see what gives:

![](<../../assets/screenshots/Edit\_stack\_·\_End-to-end\_testing (1).png>)

Now this attached context will also contribute to the [stack environment](environment.md)...

![](<../../assets/screenshots/Environment\_·\_Managed\_stack (3).png>)

...and be visible on the list of attached stacks:

![](<../../assets/screenshots/Environment\_·\_Managed\_stack (4).png>)

In order to detach the context, you can just press the _Detach_ button and the context will stop contributing to the [stack's environment](environment.md):

![](<../../assets/screenshots/Edit\_stack\_·\_End-to-end\_testing (2).png>)

#### A note on priority

You may be wondering what the priority slider is for. A priority is a property of context-stack relationship - in fact, the only property. All the contexts attached to a stack are sorted by priority (lowest first), though values don't need to be unique. This ordering establishes [precedence rules](environment.md#a-note-on-precedence) between contexts should there be a conflict and multiple contexts define the same value.

### Deleting

Deleting a context is straightforward - by pressing the Delete button in the context view you can get rid of an unnecessary context:

![](../../assets/screenshots/Production\_Kubernetes\_cluster\_Ireland\_·\_marcinwyszynski.png)

!!! warning
    Deleting a context will also automatically detach it from all the stacks it was attached to. Make sure you only delete contexts that are no longer useful. For security purposes we do not store historical stuff and actually remove the deleted data from all of our data storage systems.

## Use cases

We can see two main use cases for contexts, depending on whether the context data is [supplied externally](context.md#shared-setup) or [produced by Spacelift](context.md#remote-state-alternative).

### Shared setup

If the data is external to Spacelift, it's likely that this is a form of shared setup - that is, configuration elements that are common to multiple stacks, and grouped as a context for convenience. One example of  this use case is cloud provider configuration, either for Terraform or Pulumi. Instead of attaching the same values - some of them probably secret and pretty sensitive - to individual stacks, contexts allow you to define those once and then have admins attach them to the stacks that need them.

A variation of this use case is collections of [Terraform input variables](https://www.terraform.io/docs/configuration/variables.html#assigning-values-to-root-module-variables) that may be shared by multiple stacks - for example things relating to a particular system environment (staging, production etc). In this case the collection of variables can specify things like environment name, DNS domain name or a reference to it (eg. zone ID), tags, references to provider accounts and similar settings. Again, instead of setting these on individual stacks, an admin can group them into a context, and attach to the eligible stacks.

### Remote state alternative (Terraform-specific)

If the data in the context is produced by one or more Spacelift stacks, contexts can be an attractive alternative to the Terraform [remote state](https://www.terraform.io/docs/providers/terraform/d/remote\_state.html). In this use case, contexts can serve as outputs for stacks that can be consumed by (attached to) other stacks. So, instead of exposing the entire state, a stack can use Spacelift Terraform provider to define values on a context - either managed by the same stack , or managed externally. Managing a context externally can be particularly useful when multiple stacks contribute to a particular context.

!!! info
    In order to use the Terraform provider to define contexts or its configuration elements the stack has to be marked as [administrative](../stack/#administrative).

As an example of one such use case, let's imagine an organization where shared infrastructure (VPC, DNS, compute cluster etc.) is centrally managed by a DevOps team, which exposes it as a service to be used by individual product development teams. In order to be able to use the shared infrastructure, each team needs to address multiple entities that are generated by the central infra repo. In vanilla Terraform one would likely use remote state provider, but that might expose secrets and settings the DevOps team would rather keep it to themselves. Using a context on the other hand allows the team to decide (and hopefully document) what constitutes their "external API".

The proposed setup for the above use case would involve two administrative stacks - one to manage all the stacks, and the other for the DevOps team. The management stack would programmatically define the DevOps one, and possibly also its context. The DevOps team would receive the context ID as an input variable, and use it to expose outputs as [`spacelift_environment_variable`](https://github.com/spacelift-io/terraform-provider-spacelift#spacelift\_environment\_variable-resource)  and/or [`spacelift_mounted_file`](https://github.com/spacelift-io/terraform-provider-spacelift#spacelift\_mounted\_file-resource) resources. The management stack could then simply attach the context populated by the DevOps stack to other stacks it defines and manages.



### Extending Terraform CLI Configuration (Terraform-specific)

For some of our Terraform users, a convenient way to configure the Terraform CLI behavior is through customizing the `~/.terraformrc` file.

Spacelift allows you to extend terraform CLI configuration through the use of [mounted files](../../vendors/terraform/cli-configuration.md#using-mounted-files).
