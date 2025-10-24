# Create, delete, and lock stacks

## Create a stack in Spacelift

[Creating a stack](../../concepts/stack/creating-a-stack.md) involves 9 steps, most of which are optional. Required tasks are marked with an asterisk here:

1. *[Name, describe, and label](#1-stack-details) the stack.
2. *[Create a link](#2-connect-to-source-code) between your new stack and an existing source code repository.
3. *[Choose the backend vendor](#3-choose-vendor).
4. [Define common behavior](#4-define-behavior) of the stack.
5. [Assign roles](#5-assign-roles).
6. [Create stack hooks](#6-add-hooks).
7. [Attach a cloud integration](#7-attach-cloud).
8. [Attach policies](#8-attach-policies).
9. [Attach contexts](#9-attach-context).
10. *[Review the summary and create your stack](#10-summary).

!!! info
    You need to be an admin to create a stack. By default, GitHub account owners and admins are automatically given Spacelift admin privileges, but this can be customized using [login policies](../policy/login-policy.md) and/or [SSO integration](../../integrations/single-sign-on/README.md).

To get started, click **Create stack** on the _Stacks_ page or **Create first stack** from the _LaunchPad_ if you haven't set up a stack before.

![Create a new stack](<../../assets/screenshots/CreateStackGS.png>)

### 1. Stack details

Fill in required _stack details_.

![Fill in stack details](<../../assets/screenshots/getting-started/create-stack/Stack-details.png>)

1. **Name**: Enter a unique, descriptive name for your stack.
2. **Space**: Select the [space](../../concepts/stack/README.md) to create the stack in.
3. [**Labels**](../../concepts/stack/stack-settings.md#labels) (optional): Add labels to help sort and filter your stacks.
4. **Description** (optional): Enter a (markdown-supported) description of the stack and the resources it manages.
5. Click **Continue**.

### 2. Connect to source code

Connect your [VCS provider](../../getting-started/integrate-source-code/README.md) and fill in the details.

![](<../../assets/screenshots/getting-started/create-stack/connect-source-code.png>)

1. **Integration**: Verify the VCS integration name is correct.
2. **Repository**: Select the repository to manage in Spacelift. If you have multiple repositories linked to one VCS, leave blank.
3. **Branch**: Select the branch of the repository to manage with this stack.
4. [**Project root**](../../concepts/stack/stack-settings.md#project-root) (optional): If the entrypoint of the stack is different than the root of the repo, enter its path here.
5. [**Project globs**](../../concepts/stack/stack-settings.md#project-globs) (optional): Enter additional files and directories that should be managed by the stack.
6. Click **Continue**.

### 3. Choose vendor

Select your IaC vendor and fill in the required details, then click **Create & continue**.

![](<../../assets/screenshots/getting-started/create-stack/choose-vendor.png>)

#### OpenTofu/Terraform

We support Terraform 0.12.0 and above, and all OpenTofu versions. Spacelift also supports full [Terraform version management](../../vendors/terraform/version-management.md) allowing you to preview the impact of upgrading to a newer version.

!!! warning

    This is the only time you can ask Spacelift to be the state backend for a given [OpenTofu/Terraform stack](../../vendors/terraform/state-management.md).

1. **Workflow tool**: Set to OpenTofu, Terraform (FOSS), or [Custom](../../vendors/terraform/workflow-tool.md).
      - With OpenTofu or Terraform (FOSS), select a specific **version** or enter a **version range**.
2. **Smart Sanitization** (recommended): Choose whether Spacelift attempts to sanitize sensitive resources created by OpenTofu/Terraform.
3. **Manage State** (recommended): Choose whether Spacelift should handle the OpenTofu/Terraform state.
      1. If **disabled**: Optionally enter a **workspace**.
      2. If **enabled**: Configure these options:
         - [**External state access**](../../vendors/terraform/external-state-access.md): Allow external read-only access for stacks with [Space writer role](../authorization/assigning-roles-stacks.md) or users with write permissions to the Stack's space.
         - **Import existing state file**: Enable to import a state file from your previous backend.
4. Click **Create & continue**.

#### Pulumi

1. **Login URL**: Enter the URL to your Pulumi state backend.
2. **Stack name**: Enter a name for your Pulumi stack. This is separate from the name of the Spacelift stack, but you can give both the same name.
3. Click **Create & continue**.

#### AWS CloudFormation

1. **Region**: Enter the AWS region your stack will be located in (e.g. `us-east-2`).
2. **Stack name**: Enter the name of the corresponding CloudFormation stack.
3. **Entry template file**: Enter the path to the template file in your repo describing the root CloudFormation stack.
4. **Template bucket**: Enter the location of the S3 bucket to store processed CloudFormation templates, so Spacelift can manage the state properly.
5. Click **Create & continue**.

#### Kubernetes

1. **Namespace** (optional): Enter the namespace of the Kubernetes cluster you want to run commands on. Leave blank for multi-namespace stacks.
2. **Workflow tool**: Select the tool used to execute workflow commands.
      - **Kubernetes**: Provide the **kubectl version** the worker will download.
      - **Custom**: No configuration needed.
3. Click **Create & continue**.

#### Terragrunt

1. **Terragrunt version**: Select a specific OpenTofu/Terraform **version** or enter a **version range**.
2. **Tool**: Select the tool used to make infrastructure changes:
      - **OpenTofu/Terraform (FOSS)**: Select a specific OpenTofu/Terraform version or enter a version range.
      - **Manually provisioned**: Outside of Spacelift, ensure the tool is available to the worker via a custom image or hook and set the `TERRAGRUNT_TFPATH` environment variable to tell Terragrunt where to find it.
3. **Smart Sanitization** (recommended): Choose whether Spacelift attempts to sanitize sensitive resources created by OpenTofu/Terraform.
4. **Use All Run**: Enable to use Terragrunt's run-all feature.
5. Click **Create & continue**.

#### Ansible

1. **Playbook**: Enter the playbook file to run in the stack.
2. Click **Create & continue**.

Once you've configured your vendor information, click **Continue** to **Define stack behavior**.

![Define stack behavior](<../../assets/screenshots/DefineStackBehaviorGS.png>)

### 4. Define behavior

Determine and set additional behaviors for your stack.

1. **Worker pool**: Choose which [worker pool](../../concepts/worker-pools/README.md) to use (default is public workers).
2. **Runner image**: Use a custom runner for your runtime environment.
3. **Allow** [**run promotion**](../../concepts/run/run-promotion.md): Allows you to promote a proposed run to a tracked run (i.e. deploy from a feature branch).
4. **Autodeploy**: Automatically deploy changes to your code.
5. [**Autoretry**](../../concepts/stack/stack-settings.md#autoretry): Automatically retry deployment of invalidated proposed runs. For stacks using private workers only.
6. **Enable local preview**: Preview how code changes will execute with the [spacectl](https://github.com/spacelift-io/spacectl){: rel="nofollow"} CLI feature.
7. **Enable** [**secret masking**](../../concepts/stack/stack-settings.md#enable-well-known-secret-masking): Automatically redact secret patterns from logs.
8. **Protect from deletion** (recommended): Protect your stacks from accidental deletion.
9. **Transfer sensitive outputs across dependencices**: Pass sensitive outputs from this stack to dependent stacks.

Once you've configured your settings, click **Save & continue**.

### 5. Assign roles

You can assign roles to your stack to control access and permissions to other Spacelift resources. This is done through [role attachments](../authorization/assigning-roles-stacks.md). This is useful if you want to manage Spacelift resources using IaC. See more details in the [Terraform provider documentation](../../vendors/terraform/terraform-provider.md).

### 6. Add hooks

You also have the ability to control what happens before and after each runner phase using [stack hooks](../../concepts/stack/stack-settings.md#customizing-workflow). Define commands that run during the following phases:

- Initialization
- Planning
- Applying
- Destroying
- Performing
- Finally

Once you've added all hooks, click **Save & continue**.

### 7. Attach cloud

If desired, attach your [cloud provider integration](../../getting-started/integrate-cloud/README.md).

1. Select the cloud provider the stack will use.
2. **Attach integration**: Choose the name of the integration the stack will use.
3. **Read**: Use the integration during read phases.
4. **Write**: Use the integration during write phases.
5. Click **Attach**.
6. Click **Continue**.

### 8. Attach policies

If you're just following the LaunchPad steps, you won't have any [policies](../../concepts/policy/README.md) yet. If you did configure policies, you will be able to attach them here:

- [Approval](../../concepts/policy/approval-policy.md): Who can approve or reject a run and how a run can be approved.
- [Plan](../../concepts/policy/terraform-plan-policy.md): Which changes can be applied.
- [Push](../../concepts/policy/push-policy/README.md): How Git push events are interpreted.
- [Trigger](../../concepts/policy/trigger-policy.md): What happens when blocking runs terminate.

Click **Continue**.

### 9. Attach context

Contexts are sets of environment variables and related configuration, including hooks, that can be shared across multiple stacks. By attaching a context, you ensure your stack has all the necessary configuration elements it needs to operate, without repeating the setup for each stack.

If you're just following the LaunchPad steps, you won't have any [contexts](../../concepts/configuration/context.md) yet. If you did configure contexts, you will be able to attach them here.

Click **Continue**.

### 10. Summary

Review your settings before finalizing your stack, then click **Confirm**.

## Delete a stack in Spacelift

If you want to save the state file before deleting a stack, you can retrieve it with a task.

1. On the _Stacks_ tab, click the three dots next to the stack you want to delete.
2. Click **Settings**, then click **Stack deletion**.
3. Choose whether to delete or keep the stack's resources.
4. Type "**delete**" in the box, then click **Delete**.

![Delete a stack](<../../assets/screenshots/stack/delete-stack.png>)

!!! info
    Resource deletion is not currently supported while using the native Terragrunt support.

### Deleting resources managed by a stack

Depending on the backend of your stack, there are different commands you can run as a [task](../run/task.md) before deleting the stack.

| Backend            | Command                                                                                                                                        |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| **Terraform**      | `terraform destroy -auto-approve`                                                                                                              |
| **OpenTofu**       | `tofu destroy -auto-approve`                                                                                                                   |
| **CloudFormation** | `aws cloudformation delete-stack --stack-name <cloudformation-stack-name>`                                                                     |
| **Pulumi**         | `pulumi destroy --non-interactive --yes`                                                                                                       |
| **Kubernetes**     | `kubectl delete --ignore-not-found -l spacelift-stack=<stack-slug> $(kubectl api-resources --verbs=list,create -o name &#124; paste -s -d, -)` |

!!! tip
    For Terraform, you can also run a task through our CLI tool [spacectl](../../vendors/terraform/provider-registry.md#use-our-cli-tool-called-spacectl).

### Scheduled delete

You can use [scheduling to delete a stack](./scheduling.md) at a specified time and date.

### Using the API

You can also use Spacelift's [GraphQL API to delete a stack](../../integrations/api.md).

## Lock a stack in Spacelift

Spacelift supports locking a stack for one person's exclusive use. This is useful to prevent someone else's changes to the strack from impacting delicate operations. Every stack [writer](../policy/stack-access-policy.md#readers-and-writers) can lock a stack unless it's already locked.

The owner of the lock is the only one who can trigger [runs](../run/README.md) and [tasks](../run/task.md) for the entire duration of the lock. Locks never expire, and only its creator and Spacelift admins can release it.

![Lock a stack](<../../assets/screenshots/lockstackss.png>)

!!! info
    Note that while a stack is locked, [auto deploy](stack-settings.md#autodeploy) is disabled to prevent accidental deployments.
