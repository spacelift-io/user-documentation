# Context

!!! note
    For simplicity, we'll use the term **projects** to refer to both [stacks](../stack/README.md) and [modules](../../vendors/terraform/external-modules.md).

{% if is_self_hosted() %}
Context is a bundle of configuration elements ([environment variables](./environment.md#environment-variables) and [mounted files](./environment.md#mounted-files)) independent of any [stack](../stack/README.md) that can be managed separately and [attached](#attaching-and-detaching-contexts) to as many or as few stacks as necessary. Contexts are only directly accessible to administrators from the _Share code & config_ > _Contexts_ tab:

![Contexts page](<../../assets/screenshots/context.png>)

The list of contexts merely shows the name and description of the context. Clicking on the name allows you to [edit it](context.md#editing-a-context).
{% else %}
Context is a bundle of configuration elements ([environment variables](environment.md#environment-variables), [mounted files](environment.md#mounted-files) and [hooks](../stack/stack-settings.md#customizing-workflow)) independent of any [stack](../stack/README.md) that can be managed separately and [attached](#attaching-and-detaching-contexts) to as many or as few projects as necessary. Contexts are only directly accessible to administrators from the _Share code & config_ > _Contexts_ tab:

![Contexts page](<../../assets/screenshots/context/contexts_list.png>)

The list of contexts displays names, descriptions, and labels of the contexts. You can [edit a context](context.md#editing-a-context) from the list by clicking the three dots in a context's row, clicking **Edit**, entering the new name, then clicking **Save**. You can also [delete a context](#deleting-a-context) from the same menu.
{% endif %}

## Context management

You can [create](#creating-a-context), [edit](#editing-a-context), [attach, detach](#attaching-and-detaching-contexts) and [delete](#deleting-a-context) contexts. We will show you how to do so through the Spacelift UI, but you can also manage contexts programmatically using [our Terraform provider](../../vendors/terraform/terraform-provider.md).

## Creating a context

{% if is_self_hosted() %}
As an account administrator you can create a new context by navigating to _Share code & config_ > _Contexts_ and clicking **Add context**.

This takes you to a simple form where the only inputs are name and description:

![Create a new context](<../../assets/screenshots/create_new_context.png>)

- **Name**: What will display on the _Contexts_ tab and on dropdown menus to attach the context. This should be concise but informative.
- **Description** (optional): A Markdown-supported free-form place to describe the context in more depth. This will only display on the _Contexts_ tab.

!!! warning
    Based on the original context name, Spacelift generates an immutable slug that serves as a unique identifier of the context. If the name and the slug diverge significantly, things may become confusing.

    Although you can change the context name at any point, we strongly discourage all non-trivial changes.
{% else %}
As an account administrator you can create a new context by navigating to _Share code & config_ > _Contexts_ and clicking **Create context**.

1. Fill in [context details](#step-1-context-details), then click **Continue**.
2. [Attach the context](#step-2-attach-context-optional) to project(s) using the dropdown, then click **Continue**.
3. [Add variables and mounted files](#step-3-setup-environment-optional), then click **Continue**:
      - **Variables**: Enter a name for the [variable](./environment.md#adding-environment-variables), its value, choose whether it's secret or not, and optionally enter a description, then click **Add variable**.
      - **Mounted files**: Enter the path to the [mounted file](./environment.md#mounted-files), choose whether it's secret or not, optionally enter a description, attach the file, then click **Add file**.
4. [Add hooks](#step-4-add-hooks-optional) to the various project phases, then click **Continue**.
5. Review the summary, then click **Create context**.

### Step 1. Context details

This is the only mandatory step in the context creation process; the remaining steps are optional.

![Fill in context details](<../../assets/screenshots/context/creation_form_step_1.png>)

- **Name**: Enter a unique, descriptive name for your context.
- **Space**: Select the space to create the context in.
- **Description** (optional): Enter a (markdown-supported) description of the context. This will display on the _Contexts_ tab and in the list of attached contexts in a stack's details.
- **Label** (optional): Add labels to help sort and filter your contexts. You can also use the `autoattach` label to [automatically attach the context](#auto-attachments) to a specified stack or stacks.

!!! warning
    Based on the original context name, Spacelift generates an immutable slug that serves as a unique identifier of the context. If the name and the slug diverge significantly, things may become confusing.

    Although you can change the context name at any point, we strongly discourage all non-trivial changes.

### Step 2. Attach context (optional)

Attach the context to projects by selecting the project from the dropdown and clicking **Attach**. You can attach it to multiple contexts. When you're done, click **Continue**.

![Attach context to projects](<../../assets/screenshots/context/creation_form_step_2.png>)

### Step 3. Setup environment (optional)

Configure [environment variables](./environment.md#adding-environment-variables) and [mounted files](./environment.md#mounted-files) if you already have them ready during the creation of the context.

| Environment variables                                                                         | Mounted files                                                                         |
| --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| ![Set up environment variables](<../../assets/screenshots/context/creation_form_step_2a.png>) | ![Set up mounted files](<../../assets/screenshots/context/creation_form_step_2b.png>) |

### Step 4. Add hooks (optional)

Hooks are optional scripts that can be set up to run before and/or after different project phases, automating tasks at specific points in the project lifecycle.

![Add optional hooks](<../../assets/screenshots/context/creation_form_step_4.png>)

To add a hook, select the phase in which it should be run, enter the command in the text box (either _Before_ or _After_), then click **Add**. You can add as many hooks as you like, and they will run in the order they appear.

After adding a hook, you can rearrange it within a section or move it to the other section by dragging and dropping:

![Reordering hooks](<../../assets/screenshots/context/context_hooks_reordering.gif>)

When you're done, click **Continue**.

### Step 5. Review summary

Review the full summary of the new context and the information you filled out in each of the steps. If it's all correct, click **Create context**.
{% endif %}

## Editing a context

{% if is_self_hosted() %}
You can edit the context from its dedicated view by clicking **Edit**:

![Edit context](<../../assets/screenshots/context_edit_button.png>)

This switches the context into editing mode where you can change the name and description. You can also manage configuration elements the same way you'd do for the [stack environment](environment.md), without overrides and [computed values](environment.md#computed-values):

![Edit context details](<../../assets/screenshots/context_edit_mode.png>)
{% else %}
You can edit everything about a context (details, attached projects, environment variables, mounted files, and hooks) except for its slug.

!!! note
    Any context details (such as environment variables or mounted files) that have been set as _secret_ will not be visible in the Spacelift UI or via the API.

### Editing context details

To edit the details of a context, navigate to the _Share code & config_ > _Contexts_ tab. Click the three dots in a context's row, then click **Edit**.

![Edit context details](<../../assets/screenshots/context/edit-context-details.png>)

### Editing environment variables

Click on a context in the list on the _Share code & config_ > _Contexts_ tab to view its details. On the _Variables_ tab, you'll find a list of all the environment variables associated with the context.

Click the three dots in a variable's row, then click **Edit**. This will open a drawer where you can edit the variable's properties such as value, description, and sensitivity. Make your changes, then click **Save**.

![Edit environment variable drawer](<../../assets/screenshots/context/edit_env_var.png>)

Changes to environment variables will **affect all projects using the context**. Be cautious when making changes to avoid unintended side effects.

### Editing mounted files

Navigate to the _Share code & config_ > _Contexts_ tab. On the _Mounted files_ tab, you'll find a list of all the mounted files associated with the context.

You can preview the contents of a non-secret mounted file by clicking **Expand** by the file name. To edit it, click the three dots in the file's row, then click **Edit file**. Make your changes, then click **Save**.

![Edit mounted file](<../../assets/screenshots/context/edit_mounted_file.png>)

### Editing hooks

Navigate to the _Share code & config_ > _Contexts_ tab. On the _Hooks_ tab, you'll find a list of all the hooks associated with the context grouped by the different project phases.

To modify hooks, click **Expand** by the phase name. Click **Edit** (pencil) to edit a hook, or **Delete** (trash can) to delete it.

![Edit hooks](<../../assets/screenshots/context/hooks_list.png>)

You can add a new command, adjust its position within the same section, or even move it to the other section using a simple drag-and-drop mechanism. Once you've made the necessary adjustments, click **Save**

Hooks run in the sequence they appear in the list, so the order matters.
{% endif %}

## Attaching and detaching contexts

{% if is_self_hosted() %}
Attaching and detaching contexts actually happens from the [stack](../stack/README.md) management view. To attach a context, select the Contexts tab. This should show you a dropdown with all the contexts available for attaching, and a slider to set the [priority of the attachment](context.md#on-priority):

![Attach context](<../../assets/screenshots/context_attach.png>)

!!! info
    A context can only be attached once to a given stack, so if it's already attached, it will not be visible in the dropdown menu.

For example, if you attach a context with priority 0:

![](../../assets/screenshots/context_attach_priority.png)

Now this attached context will also contribute to the [stack environment](environment.md)...

![](../../assets/screenshots/context_environment.png)

...and be visible on the list of attached contexts:

![](../../assets/screenshots/contexts_attached.png)

You can remove a context from the stack by clicking **Detach**.
{% else %}
Navigate to _Ship Infra_ > _Stacks_ and click the name of the stack where you want to add or remove a context. Then navigate to the _Contexts_ tab and click **Attach context**.

You'll see a dropdown with all the contexts available for attaching. Select the context, then enter its [priority](#on-priority) (lowest values go first).

![Attach context](<../../assets/screenshots/context/attach-context.png>)

!!! info
    A context can only be attached once to a given stack, so if it's already attached, it will not be visible in the dropdown menu.

Attached contexts contribute to the [stack environment](environment.md).

You can edit a context's priority by clicking the three dots in the context's row, then click **Edit priority**. To detach a context, click **Detach**.

![Edit priority or detach context](<../../assets/screenshots/context/edit-or-detach-context.png>)
{% endif %}

{% if is_saas() %}

### Auto-attachments

The `autoattach` label automatically attaches contexts and policies to projects based on shared labels. This comes in handy, especially when multiple projects require the same context.

Instead of manually attaching a context to every stack or module, simply define an `autoattach` label on the context. For example, adding the label `autoattach:XYZ` to a context will automatically attach that context to all projects with the matching `XYZ` label.

!!! Note
    You only need the `autoattach:` prefix for the context label; the projects only need the specific label (`XYZ`) to activate the automatic attachment.

1. Navigate to the context view and open the context [details drawer](#editing-context-details).
2. Define an `autoattach` label to the context. For instance, `autoattach:XYZ`.
   ![Context autoattach label](<../../assets/screenshots/context/add_autoattachment_label.png>)
3. Ensure that your projects have the matching label. In this case, it should be `XYZ`.
   ![Stack labels](<../../assets/screenshots/stack/settings/stack-details-labels.png>)

Once complete, Spacelift will automatically link the context to all projects sharing the `XYZ` label.

!!! tip
    If you want to attach a context to all projects, you can use the `autoattach:*` label on the context. This will attach the context to all projects, regardless of their labels.

    If the context is in a specific space, the `autoattach:*` label will only attach the context to stacks in that space and its child spaces.    
{% endif %}

#### On priority

Priority is a property of the context-stack relationship. All the contexts attached to a stack are sorted by priority (lowest first), though values don't need to be unique. This ordering establishes [precedence rules](./environment.md#attached-contexts) between contexts should there be a conflict and multiple contexts define the same value.

You might notice that there is no priority picker for auto-attached contexts. The highest priority for all configuration elements (environment variables, mounted files, and hooks) are:

1. At the stack level.
2. Explicitly attached contexts (based on set priorities).
3. Auto-attached alphabetically for environment variables, mounted files, and after phase hooks ([before phase hooks are attached reverse alphabetically](../stack/stack-settings.md#note-on-hook-order)).

### Deleting a context

{% if is_self_hosted() %}
Click **Delete** in the context view to remove an unneeded context:

![Delete a context](<../../assets/screenshots/context_delete.png>)
{% else %}
To delete a context, navigate to the _Share code & config_ > _Contexts_ tab. Click the three dots in a context's row, then click **Delete**.

![Delete a context](<../../assets/screenshots/context/delete-context.png>)

As a safety measure, you'll be asked to confirm the deletion:

![Confirm context deletion](<../../assets/screenshots/context/confirm-delete-context.png>)
{% endif %}

!!! warning
    Deleting a context will also automatically detach it from all the projects it was attached to. Make sure you only delete contexts that are no longer useful. For security purposes we do not store historical data and remove the deleted data from all of our data storage systems.

## Use cases

We can see two main use cases for contexts, depending on whether the context data is [supplied externally](context.md#shared-configuration-elements) or [produced by Spacelift](#remote-state-alternative-terraform-specific).

### Shared configuration elements

You can use contexts to group configuration elements (external to Spacelift) that are meant to be shared between multiple stacks. For example, you could use contexts for cloud provider configuration, either for OpenTofu/Terraform or Pulumi. Instead of attaching the same values (some of which could be secret) to individual stacks, contexts allow you to define those once and then attach them to the stacks that need them.

A variation of this use case is collections of [OpenTofu/Terraform input variables](https://www.terraform.io/docs/configuration/variables.html#assigning-values-to-root-module-variables){: rel="nofollow"} (for example, variables related to a particular system environment such as staging or production) that may be shared by multiple stacks. The collection of variables can specify:

- Environment name.
- DNS domain name or a reference to it (e.g. zone ID).
- Tags.
- References to provider accounts.

Instead of setting these on individual stacks, you can group them into a context and attach the context to eligible stacks.

### Remote state alternative (Terraform-specific)

You can use contexts to group data that are produced by one or more Spacelift stacks, as an alternative to the Terraform [remote state](https://www.terraform.io/docs/providers/terraform/d/remote_state.html){: rel="nofollow"}. In this use case, contexts can serve as outputs for stacks that can be consumed by (attached to) other stacks. So, instead of exposing the entire state, a stack can use the Spacelift Terraform provider to define values on a context, either managed by the same stack or externally. Managing a context externally can be particularly useful when multiple stacks contribute to a particular context.

!!! info
    To use the Terraform provider to define contexts or its configuration elements, the stack needs the right [role attachments](../authorization/assigning-roles-stacks.md).

As an example of this use case, imagine an organization where shared infrastructure (VPC, DNS, compute cluster, etc.) is centrally managed by a DevOps team, which exposes it as a service to be used by individual product development teams. To be able to use the shared infrastructure, each team needs to address multiple entities generated by the central infra repo. In vanilla Terraform you would likely use the remote state provider, but that could expose secrets and settings the DevOps team would rather keep it to themselves. Using a context, however, allows the team to decide (and  document) what constitutes their "external API".

The proposed setup for this use case would involve two [stacks with roles](../authorization/assigning-roles-stacks.md): one to manage all the stacks, and the other for the DevOps team.

1. The management stack would programmatically define the DevOps one, and possibly also its context.
2. The DevOps team would receive the context ID as an input variable, and use it to expose outputs as [`spacelift_environment_variable`](https://github.com/spacelift-io/terraform-provider-spacelift#spacelift_environment_variable-resource){: rel="nofollow"} and/or [`spacelift_mounted_file`](https://github.com/spacelift-io/terraform-provider-spacelift#spacelift_mounted_file-resource){: rel="nofollow"} resources.
3. The management stack could then attach the context populated by the DevOps stack to other stacks it defines and manages.

### Extending Terraform CLI Configuration (Terraform-specific)

For some of our Terraform users, a convenient way to configure the Terraform CLI behavior is through customizing the `~/.terraformrc` file.

Spacelift allows you to extend terraform CLI configuration through the use of [mounted files](../../vendors/terraform/cli-configuration.md#using-mounted-files).
