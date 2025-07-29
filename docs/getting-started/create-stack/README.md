# Create a stack in Spacelift

[Creating a stack](../../concepts/stack/creating-a-stack.md) involves 9 steps, most of which are optional. Required tasks are marked with an asterisk here:

1. *[Name, describe, and label](#1-stack-details) the stack.
2. *[Create a link](#2-connect-to-source-code) between your new stack and an existing source code repository.
3. *[Choose the backend vendor](#3-choose-vendor).
4. [Define common behavior](#4-define-behavior) of the stack.
5. [Create stack hooks](#5-add-hooks).
6. [Attach a cloud integration](#6-attach-cloud).
7. [Attach policies](#7-attach-policies).
8. [Attach contexts](#8-attach-context).
9. *[Review the summary and create your stack](#9-summary).

To get started, click **Create stack** on the _Stacks_ page or **Create first stack** from the _LaunchPad_.

![](<../../assets/screenshots/CreateStackGS.png>)

## 1. Stack details

Fill in required _stack details_.

![](<../../assets/screenshots/getting-started/create-stack/Stack-details.png>)

1. **Name**: Enter a unique, descriptive name for your stack.
2. **Space**: Select the [space](../../concepts/stack/README.md) to create the stack in.
3. [**Labels**](../../concepts/stack/stack-settings.md#labels) (optional): Add labels to help sort and filter your stacks.
4. **Description** (optional): Enter a (markdown-supported) description of the stack and the resources it manages.
5. Click **Continue**.

## 2. Connect to source code

Connect your VCS provider as configured during [LaunchPad step 1](../integrate-source-code/README.md) and fill in the details.

![](<../../assets/screenshots/getting-started/create-stack/connect-source-code.png>)

1. **Integration**: Verify the VCS integration name is correct.
2. **Repository**: Select the repository to manage in Spacelift. If you have multiple repositories linked to one VCS, leave blank.
3. **Branch**: Select the branch of the repository to manage with this stack.
4. [**Project root**](../../concepts/stack/stack-settings.md#project-root) (optional): If the entrypoint of the stack is different than the root of the repo, enter its path here.
5. [**Project globs**](../../concepts/stack/stack-settings.md#project-globs) (optional): Enter additional files and directories that should be managed by the stack.
6. Click **Continue**.

## 3. Choose vendor

Select your IaC vendor and fill in the required details, then click **Create & continue**. You can find more details on each vendor and how they interact with Spacelift stacks in our [stack documentation](../../concepts/stack/creating-a-stack.md#configure-backend).

![](<../../assets/screenshots/getting-started/create-stack/choose-vendor.png>)

### OpenTofu/Terraform

1. **Workflow tool**: Set to OpenTofu, Terraform (FOSS), or Custom.
      - With OpenTofu or Terraform (FOSS), select a specific **version** or enter a **version range**.
2. **Smart Sanitization** (recommended): Choose whether Spacelift attempts to sanitize sensitive resources created by OpenTofu/Terraform.
3. **Manage State** (recommended): Choose whether Spacelift should handle the OpenTofu/Terraform state.
      1. If **disabled**: Optionally enter a **workspace**.
      2. If **enabled**: Configure these options:
         - [**External state access**](../../vendors/terraform/external-state-access.md): Allow external read-only access for administrative stacks or users with write permissions to the Stack's space.
         - **Import existing state file**: Enable to import a state file from your previous backend.
4. Click **Create & continue**.

### Pulumi

1. **Login URL**: Enter the URL to your Pulumi state backend.
2. **Stack name**: Enter a name for your Pulumi stack. This is separate from the name of the Spacelift stack, but you can give both the same name.
3. Click **Create & continue**.

### AWS CloudFormation

1. **Region**: Enter the AWS region your stack will be located in (e.g. `us-east-2`).
2. **Stack name**: Enter the name of the corresponding CloudFormation stack.
3. **Entry template file**: Enter the path to the template file in your repo describing the root CloudFormation stack.
4. **Template bucket**: Enter the location of the S3 bucket to store processed CloudFormation templates, so Spacelift can manage the state properly.
5. Click **Create & continue**.

### Kubernetes

1. **Namespace** (optional): Enter the namespace of the Kubernetes cluster you want to run commands on. Leave blank for multi-namespace stacks.
2. **Workflow tool**: Select the tool used to execute workflow commands.
      - **Kubernetes**: Provide the **kubectl version** the worker will download.
      - **Custom**: No configuration needed.
3. Click **Create & continue**.

### Terragrunt

1. **Terragrunt version**: Select a specific Terraform **version** or enter a **version range**.
2. **Tool**: Select the tool used to make infrastructure changes:
      - **OpenTofu/Terraform (FOSS)**: Select a specific Terraform version or enter a version range.
      - **Manually provisioned**: Outside of Spacelift, ensure the tool is available to the worker via a custom image or hook and set the `TERRAGRUNT_TFPATH` environment variable to tell Terragrunt where to find it.
3. **Smart Sanitization** (recommended): Choose whether Spacelift attempts to sanitize sensitive resources created by OpenTofu/Terraform.
4. **Use All Run**: Enable to use Terragrunt's run-all feature.
5. Click **Create & continue**.

### Ansible

1. **Playbook**: Enter the playbook file to run in the stack.
2. Click **Create & continue**.

Once youv'e configured your vendor information, click **Continue** to **Define stack behavior**.

![Define stack behavior](<../../assets/screenshots/DefineStackBehaviorGS.png>)

## 4. Define behavior

Determine and set additional behaviors for your stack.

1. **Worker pool**: Choose whether the stack uses public or private [worker pools](../../concepts/worker-pools/README.md) (default is public).
2. **Runner image**: Use a custom runner for your runtime environment.
3. [**Administrative**](../../concepts/stack/stack-settings.md#administrative): Choose whether a stack receives administrator access to other stacks in the same environment.
4. **Allow** [**run promotion**](../../concepts/run/run-promotion.md): Deploy runs via the [Spacelift API](../../integrations/api.md) or GitHub Actions.
5. **Autodeploy**: Automatically deploy changes to your code.
6. [**Autoretry**](../../concepts/stack/stack-settings.md#autoretry): Automatically retry deployment of invalidated proposed runs. For stacks using private workers only.
7. **Enable local preview**: Preview how code changes will execute with the [spacectl](https://github.com/spacelift-io/spacectl){: rel="nofollow"} CLI feature.
8. **Enable** [**secret masking**](../../concepts/stack/stack-settings.md#enable-well-known-secret-masking): Automatically redact secret patterns from logs.
9. **Protect from deletion** (recommended): Protect your stacks from accidental deletion.
10. **Transfer sensitive outputs across dependencices**: Pass sensitive outputs from this stack to dependent stacks.

Once you've configured your settings, click **Save & continue**.

## 5. Add hooks

You also have the ability to control what happens before and after each runner phase using [stack hooks](../../concepts/stack/stack-settings.md#customizing-workflow). Define commands that run during the following phases:

- Initialization
- Planning
- Applying
- Destroying
- Performing
- Finally

Once you've added all hooks, click **Save & continue**.

## 6. Attach cloud

If desired, attach the cloud provider integration configured in [LaunchPad step 2](../integrate-cloud/README.md).

1. Select the cloud provider the stack will use.
2. **Attach integration**: Choose the name of the integration the stack will use.
3. **Read**: Use the integration during read phases.
4. **Write**: Use the integration during write phases.
5. Click **Attach**.
6. Click **Continue**.

## 7. Attach policies

If you're just following the LaunchPad steps, you won't have any [policies](../../concepts/policy/README.md) yet. If you did configure policies, you will be able to attach them here:

- [Approval](../../concepts/policy/approval-policy.md): Who can approve or reject a run and how a run can be approved.
- [Plan](../../concepts/policy/terraform-plan-policy.md): Which changes can be applied.
- [Push](../../concepts/policy/push-policy/README.md): How Git push events are interpreted.
- [Trigger](../../concepts/policy/trigger-policy.md): What happens when blocking runs terminate.

Click **Continue**.

## 8. Attach context

Contexts are sets of environment variables and related configuration, including hooks, that can be shared across multiple stacks. By attaching a context, you ensure your stack has all the necessary configuration elements it needs to operate, without repeating the setup for each stack.

If you're just following the LaunchPad steps, you won't have any [contexts](../../concepts/configuration/context.md) yet. If you did configure contexts, you will be able to attach them here.

Click **Continue**.

## 9. Summary

Review your settings before finalizing your stack, then click **Confirm**.

✅ Step 3 of the LaunchPad is complete! Now you can [invite teammates](../invite-teammates/README.md).

![](<../../assets/screenshots/getting-started/create-stack/Launchpad-step3-complete.png>)
