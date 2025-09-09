---
description: >-
   A quick start on creating a Spacelift account, linking it to a VCS, and
   creating your first Spacelift stack.
---

# Getting Started with Spacelift

Spacelift blends a regular CI's versatility with the methodological rigor of a specialized, security-conscious infrastructure tool.

In this guide we will briefly introduce some key concepts that you need to know to work with Spacelift. These concepts will be followed by detailed instructions to help you create and configure your first run with Spacelift.

## Main Concepts

- [Stacks](concepts/stack/README.md): Spacelift's central entity that connects to your source control repository and manages the state of infrastructure. Stacks also facilitate integration with cloud providers (AWS, Azure, Google Cloud) and other important Spacelift components.
- [State management](vendors/terraform/state-management.md): Infrastructure states can be managed by your backend, or (for OpenTofu/Terraform projects) imported into Spacelift. You are not required to manage your state with Spacelift.
- [Worker pools](concepts/worker-pools/README.md): The underlying compute used by Spacelift is called a worker, managed in groups known as worker pools. You need to provision at least one worker pool to use Spacelift.{% if is_saas() %} Spacelift provides public (managed by Spacelift) and private (hosted by you) worker pools.{% endif %}
- [Policies](concepts/policy/README.md): Policies provide a way to express rules as code to manage your IaC environment, and help make common decisions for login, access, and execution. Policies are based on the [Open Policy Agent](https://www.openpolicyagent.org/){: rel="nofollow"} project and can be defined using its rule language _Rego_.
- [Cloud integration](integrations/cloud-providers/README.md): Spacelift provides native integration with AWS{% if is_saas() %}, Azure, and Google Cloud (GCP){% endif %}. Integration with other cloud providers is also possible via OIDC Federation or programmatic connection with their identity services.
- [VCS change workflow](integrations/source-control/README.md): Spacelift evaluates your version control system's (VCS's) pull requests (PRs) to provide a preview of changes being made to your infrastructure. These changes are deployed automatically when PRs are merged.

{% if is_saas() %}

## Create your Spacelift account

![](<./assets/screenshots/StartforfreeGS.png>)

1. On the [Spacelift home page](https://spacelift.io/){: rel="nofollow"}, click **Start for Free**.
2. Create your Spacelift account by signing in with your GitHub, GitLab, Google, or Microsoft account.

    ![](<./assets/screenshots/Startoptions.png>)

If using GitHub, the selected GitHub organization or account name will be your Spacelift account name.

!!! note
    If using a Microsoft account, you may need to [provide admin approval](./faq/README.md#providing-admin-consent-for-microsoft-login) to log in.

{% else %}

### Step 1: Install Spacelift

Follow the [install guide](installing-spacelift/install-methods.md) to get Spacelift up and running.

{% endif %}

## Welcome to the LaunchPad

![](<./assets/screenshots/getting-started/LaunchPad.png>)

Once you log in to your Spacelift account, you will be brought to the LaunchPad tab to configure your environment. The checklist has four steps to help you get started:

1. [Integrate source code](getting-started/integrate-source-code/README.md)
2. [Integrate your cloud account](getting-started/integrate-cloud/README.md)
3. [Create first stack](getting-started/create-stack/README.md)
4. [Invite teammates](getting-started/invite-teammates/README.md)

Once your LaunchPad tasks are complete, you can start your first stack run.

## Trigger your first run

Assuming your repository contains your infrastructure (or you're using our provided [Terraform starter repository](https://github.com/spacelift-io/terraform-starter){: rel="nofollow"}), you can start using Spacelift to start runs.

!!! tip
    If you are using the Terraform starter repository, and you did not sign up for your Spacelift account with GitHub, you may need to add the environment variable `TF_VAR_github_app_namespace` with the value as your organization name or GitHub handle. You can do this under the `Environment` tab in the stack.

![](<./assets/screenshots/getting-started/trigger-stack-run.png>)

1. Navigate to the _Stacks_ tab.
2. Click the name of the stack you want to run.
3. Click **Trigger** to start a Spacelift run. This will check the source code and run any commands on it, and you will be taken to the run view.
4. Click **Confirm** to apply your changes.
5. Wait for the run to finish.

![](<./assets/screenshots/ConfirmRunGS.png>)

Your output will look different based on your code repository and the resources it creates. If you used the starter repository, you should have a new stack in your account called `Managed stack` that can demonstrate the effectiveness of our [plan policies](./concepts/policy/terraform-plan-policy.md). Play with it and see if you can fix the purposeful plan issue.
