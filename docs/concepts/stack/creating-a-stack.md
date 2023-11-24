# Creating a stack

Unless you're defining a stack programmatically using our [Terraform provider](../../vendors/terraform/terraform-provider.md), you will be creating one from the root of your Spacelift account:

![](<../../assets/screenshots/Create_Stack_Overview.png>)

!!! info
    You need to be an admin to create a stack. By default, GitHub account owners and admins are automatically given Spacelift admin privileges, but this can be customized using [login policies](../policy/login-policy.md) and/or [SSO integration](../../integrations/single-sign-on/README.md).

The stack creation process involves five simple steps:

1. [Naming, describing and labeling](creating-a-stack.md#name-your-stack);
2. [Creating a link between your new stack and an existing Git repository](#integrate-vcs);
3. [Defining backend-specific behavior](creating-a-stack.md#configure-backend) (different for each supported backend, eg. [Terraform](creating-a-stack.md#terraform), [AWS CloudFormation](../../vendors/cloudformation/README.md), [Pulumi](creating-a-stack.md#pulumi), or [Kubernetes](../../vendors/kubernetes/README.md)
4. [Defining common behavior of the stack](#define-behavior);
5. [Creating stack hooks](#create-stack-hooks);

## Name your stack

![](<../../assets/screenshots/Create_Stack_Stack_Details.png>)

Staring with the most difficult step - naming things. Here's where you give your new stack a nice informative [name and an optional description](stack-settings.md#name-and-description) - this one even supports Markdown:

![](<../../assets/screenshots/Create_Stack_Labels.png>)

You'll be able to change the name and description later, too - with one caveat. Based on the original _name_, Spacelift generates an immutable slug that serves as a unique identifier of this stack. If the name and the slug diverge significantly, things may become confusing.

Here you will be able to choose which [space](../spaces/) your stack belongs to. Initially, you start with a root and a legacy space. The root space is the top-level space of your account, while the legacy space exists for backward compatibility with pre-spaces RBAC.

Also, this is the opportunity to set a few [labels](stack-settings.md#labels). Labels are useful for searching and grouping things, but also work extremely well with policies.

## Integrate VCS

![](<../../assets/screenshots/Create_Stack_VCS.png>)

In this step, you will need to tell Spacelift where to look for the Terraform code for the stack - a combination of Git repository and one of its existing branches. The branch that you specify set here is what we called a _tracked_ branch. By default, anything that you push to this branch will be considered for deployment. Anything you push to a different branch will be tested for changes against the current state.

 The project root configuration is where inside the repository Spacelift should look for the infra project source code (e.g. create a stack for a specific folder in the repository).

A few things worth noting:

- you can point multiple Spacelift stacks to the same repository, even the same branch;
- the default behavior can be tweaked extensively to work with all sorts of Git and deployment workflows (yes, we like monorepos, too) using [push](../policy/push-policy/README.md) and [trigger](../policy/trigger-policy.md) policies, which are more advanced topics;
- in order to learn what exactly our Git hosting provider integration means, please refer to [GitHub](../../integrations/source-control/github.md) and [GitLab](../../integrations/source-control/gitlab.md) integration documentation;

!!! info
    If you're using our default GitHub App integration, we only list the repositories you've given us access to. If some repositories appear to be missing in the selection dropdown, it's likely that you've installed the app on a few selected repositories. That's fine, too, just [whitelist the desired repositories](../../integrations/source-control/github.md) and retry.

## Configure backend

At this point you'll probably know whether you want to create a [Terraform](creating-a-stack.md#terraform), [OpenTofu](creating-a-stack.md#opentofu), [Terragrunt](creating-a-stack.md#terragrunt), [AWS CloudFormation](../../vendors/cloudformation/README.md), [Pulumi](creating-a-stack.md#pulumi), [Ansible](creating-a-stack.md#ansible) or [Kubernetes](../../vendors/kubernetes/README.md) stack. Each of the supported vendors has some settings that are specific to it, and the backend configuration step is where you can define them.

### Terraform

![](<../../assets/screenshots/Create_Stack_Terraform.png>)

When selecting **Terraform**, you can choose which **version of Terraform** to start with - we support Terraform 0.12.0 and above, up to the latest version of MPL Terraform. You don't need to dwell on this decision since you can change the version later - Spacelift supports full [Terraform version management](../../vendors/terraform/version-management.md) allowing you to even preview the impact of upgrading to a newer version.

The next decisions involves your Terraform state. First, whether you want us to provide a Terraform state backend for your state. We do offer that as a convenience feature, though Spacelift works just fine with any remote backend, like Amazon S3.

!!! info
    If you want to bring your own backend, there's no point in doing additional [state locking](https://www.terraform.io/docs/state/locking.html){: rel="nofollow"} - Spacelift itself provides a more sophisticated state access control mechanism than Terraform.

If you choose not to use our state backend, feel free to proceed. If you do want us to manage your state, you have an option to import an existing state file from your previous backend. This is only relevant if you're migrating an existing Terraform project to Spacelift. If you have no state yet and Spacelift will be creating resources from scratch, this step is unnecessary.

!!! warning
    Remember - this is the only time you can ask Spacelift to be the state backend for a given stack, so choose wisely. You can read more about state management [here](../../vendors/terraform/state-management.md).

In addition to these options, we also offer [external state access](../../vendors/terraform/external-state-access.md) for read-only purposes, this is available for administrative stacks or users with write permission to this Stack's space.

### OpenTofu

![](<../../assets/screenshots/Create_Stack_OpenTofu.png>)

Right now, creating an OpenTofu has only one slight difference from creating a Terraform stack and that difference refers to setting the workflow tool to OpenTofu.

### Pulumi

![](<../../assets/screenshots/Create_Stack_Pulumi.png>)

When creating a Pulumi stack, you will need to provide two things. First, the login URL to your Pulumi state backend, as currently we don't provide one like we do for Terraform, so you will need to bring your own.

Second, you need to specify the name of the Pulumi stack. This is separate from the name of the Spacelift stack, which you will specify in the [next step](creating-a-stack.md#define-behaviour). That said, nothing prevents you from keeping them in sync.

### CloudFormation

![](<../../assets/screenshots/Create_Stack_CF.png>)

If you're using CloudFormation with Spacelift, there are a few pieces of information you'll need to provide. First, you'll need to specify the region where your CloudFormation stack will be located.

Additionally, you'll need to provide the name of the corresponding CloudFormation stack for this Spacelift stack. This will help us keep track of the different resources in your infrastructure.

You'll also need to provide the path to the template file in your repository that describes the root CloudFormation stack and finally you'll need to specify the S3 bucket where your processed CloudFormation templates will be stored. This will enable us to manage your CloudFormation state and ensure that all changes are properly applied.

### Kubernetes

![](<../../assets/screenshots/Create_Stack_K8s.png>)

When you create a Kubernetes stack in Spacelift, you have the option to specify the namespace of the Kubernetes cluster that you want to run commands on. You can leave this empty for multi-namespace Stacks.

You can also provide the version of kubectl that you want the worker to download. This is useful if you need to work with a specific version of kubectl for compatibility or testing purposes. The worker will download the specified version of kubectl at runtime, ensuring that the correct version is available for executing commands on the cluster.

### Terragrunt

![](<../../assets/screenshots/Create_Stack_Terragrunt.png>)
Creating a Terragrunt stack in Spacelift, gives you the option to specify the Terraform and Terragrunt versions you want to use.

You also have the possibility of enabling the run-all feature of Terragrunt, which is useful in scenarios where organizations rely on this in their current process and are unable to do a full migration yet.

Support is currently in Beta.

### Ansible

![](<../../assets/screenshots/Create_Stack_Ansible.png>)

When you create an Ansible stack in Spacelift, you have the option to select the playbook file you want to use. You can define policies for your stack as you would do for any other stack.

Support is currently in Beta.

## Define behavior

Regardless of which of the supported backends (Terraform, Pulumi etc.) you're setting up your stack to use, there are a few common settings that apply to all of them. You'll have a chance to define them in the next step:

![](<../../assets//screenshots/Create_Stack_Define_Behavior.png>)

The behavior settings are:

- whether the stack is [administrative](./stack-settings.md#administrative);
- [worker pool](../worker-pools.md) to use, if applicable (default uses the Spacelift public worker pool);
- whether the changes should [automatically deploy](./stack-settings.md#autodeploy);
- whether obsolete tests should be [automatically retried](./stack-settings.md#autoretry);
- whether or not to protect the stack from deletion;
- whether or not to enable the local preview [spacectl](https://github.com/spacelift-io/spacectl){: rel="nofollow"} CLI feature;
- whether or not [run promotion](../run/run-promotion.md) is enabled;
- optionally specify a custom Docker image to use to for your job container;

## Create Stack Hooks

![](<../../assets/screenshots/Create_Stack_Hooks.png>)

You also have the ability to control what happens before and after each runner phase using Stack Hooks. In this phase, you can define commands that run in between the following phases:

- Initialization
- Planning
- Applying
- Destroying
- Performing
- Finally
