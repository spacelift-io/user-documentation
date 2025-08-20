---
description: >-
  Describes how to setup the GitHub VCS integration on Spacelift, as well as the
  features supported by the integration.
---

# GitHub

Spacelift is deeply integrated with GitHub, providing organizations a simple way to manage IaC versioned in GitHub.

You can set up multiple Space-level and one default GitHub integration per account.

!!! info "Using multiple GitHub accounts"
    If you want to use multiple GitHub accounts or organizations, or connect Spacelift to your GitHub Enterprise instance, you will need to set up a custom GitHub integration via a [GitHub App](github.md#create-the-github-application).

{% if is_saas() %}
 If you used GitHub to create your Spacelift account, the flow for also connecting GitHub as your [VCS provider](./README.md) is slightly different. Select the option that applies to your account:

1. Created Spacelift account with [GitHub](github.md#signed-in-with-github).
2. Created Spacelift account with [GitLab, Google, or Microsoft](github.md#signed-in-with-another-option).

## Signed in with GitHub

1. [Install the Spacelift GitHub App](https://github.com/apps/spacelift-io/installations/new){: rel="nofollow"} from the GitHub Marketplace.
2. Select the GitHub repository or repositories to manage in Spacelift.
      - If you do not have a GitHub repository of this kind, you can fork our [terraform-starter repository](https://github.com/spacelift-io/terraform-starter){: rel="nofollow"}. Allow the installed GitHub app access to the forked repository.

![](<../../assets/screenshots/InstallAppGS.png>)

## Signed in with another option

If you used GitLab, Google, or Microsoft to create your account, you will need to create a GitHub custom applicationto link it to Spacelift.

{% else %}

## Create and link a custom application

You will need to create a GitHub application to link it to Spacelift.
{% endif %}

### Create the GitHub application

1. On the _Source control_ tab, click **Set up integration**, then choose **GitHub** on the dropdown.
2. Click [**Set up via wizard**](github.md#set-up-via-wizard) (_recommended_) or [**Set up manually**](github.md#set-up-manually).

![](<../../assets/screenshots/CleanShot 2022-09-16 at 09.38.30.png>)

!!! warning
    Manual application setup is more prone to errors and should only be used if other methods will not work.

### Set up via wizard

1. Select whether you're integrating with GitHub.com or a self-hosted installation, then click **Continue**.
2. Select whether the GitHub integration should be owned by a personal or organization account, then click **Continue**.
3. Click **Continue** to create the application on GitHub.com.
    1. Enter a name for your integration. This can be changed later.
    2. Click **Create GitHub app**. You will be redirected back to Spacelift.
4. Fill in the additional information:
    ![](<../../assets/screenshots/GitHub_wizard_final_step.png>)
    1. **Integration name**: Must be unique, and cannot be changed after app creation because the Spacelift webhook endpoint is generated based on this name.
    2. **Integration type**: Default (all spaces) or [Space-specific](../../concepts/spaces/README.md). Each Spacelift account can only support one default integration per VCS provider, which is available to all stacks and modules in the same Space as the integration.
    3. **VCS checks**: Individual checks (one per stack) or aggregated checks (summarized checks across all affected stacks).
    4. **Labels**: Organize integrations by assigning labels to them.
    5. **Description**: A markdown-formatted free-form text field to describe the integration.
5. Click **Set up**. Once the application is created, you will automatically be redirected to install it in GitHub.

### Set up manually

After selecting the option to enter your details manually, you should see the following form:

![](<../../assets/screenshots/CleanShot 2022-09-16 at 10.14.05.png>)

1. **Integration name:** Enter a name for your integration. It cannot be changed later because the Spacelift webhook endpoint is generated based on this name.
2. **Integration type:** Default (all spaces) or [Space-specific](../../concepts/spaces/README.md). Each Spacelift account can only support one default integration per VCS provider, which is available to all stacks and modules in the same Space as the integration.

Once the integration name and the type are chosen, a **webhook endpoint** and a **webhook secret** will be generated for the GitHub app in the middle of the form.

#### Create app in GitHub

##### Initial setup

1. Open GitHub, navigate to the _GitHub Apps_ page in the _Developer Settings_ for your account/organization, and click **New GitHub App**.
2. You can either create the App in an individual user account or within an organization account:
   ![](<../../assets/screenshots/image (52).png>)
3. Give your app a name and homepage URL (these are only used for informational purposes within GitHub):
   ![](<../../assets/screenshots/image (53).png>)
4. Paste your Webhook URL and secret from Spacelift:
   ![](<../../assets/screenshots/image (54).png>)
5. Set the following Repository permissions:

     | Permission      | Access       |
     | --------------- | ------------ |
     | Checks          | Read & write |
     | Commit statuses | Read & write |
     | Contents        | Read-only    |
     | Deployments     | Read & write |
     | Metadata        | Read-only    |
     | Pull requests   | Read & write |
     | Webhooks        | Read & write |

6. Set the following Organization permissions:

      - Check run
      - Issue comment
      - Organization
      - Pull request
      - Pull request review
      - Push
      - Repository
8. Choose whether you want to allow the App to be installed on any account or only the current account, then click **Create GitHub App**:
    ![](<../../assets/screenshots/image (55).png>)

##### Generate key

1. Copy the _App ID_ in the _About_ section:
    ![](<../../assets/screenshots/image (56).png>)
2. Scroll down to the _Private keys_ section of the page and click **Generate a private key**:
    ![](<../../assets/screenshots/image (57).png>)
    This will download the private key file for your GitHub app named `<app-name>.<date>.private-key.pem` (for example: `spacelift.2025-05-11.private-key.pem`).

##### Copy API details into Spacelift

Now that your GitHub App has been created, return to the integration configuration screen in Spacelift.

1. **API host URL**: Enter the URL to your GitHub server, which should be [https://api.github.com](https://api.github.com){: rel="nofollow"}.
2. **User facing host URL**: Enter the URL that will be shown to the user and displayed in the Spacelift UI. This will be the same as the API host URL unless you are using [VCS Agents](../../concepts/vcs-agent-pools.md), in which case it should be `private://<vcs-agent-pool-name>`.
3. **App ID**: Enter the App ID you copied before generating the private key.
4. **Private key**: Paste the contents of your private key file.
    ![](<../../assets/screenshots/Screen Shot 2022-04-20 at 4.30.53 PM.png>)
5. **Labels**: Organize integrations by assigning labels to them.
6. **Description**: A markdown-formatted free-form text field to describe the integration.
7. Click **Set up** to save your integration settings.

### Install the GitHub application

Once your GitHub app has been created and configured in Spacelift, you can install it on one or more accounts or organizations you have access to.

=== "Via Spacelift UI"

    1. On the _Source code_ page, click **Install the app**:

        ![](<../../assets/screenshots/github_install_app.png>)
    2. On GitHub, click **Install**.
    3. Choose whether you want to allow Spacelift access to all repositories or only specific ones in the account:
        
        ![](<../../assets/screenshots/image (60).png>)
    4. Click **Install** to link your GitHub account to Spacelift.

=== "Via GitHub UI"

    1. Find your Spacelift app on the _GitHub Apps_ page in your account settings, and click **Edit**:
        ![](<../../assets/screenshots/image (58).png>)
    2. In the _Install App_ section, click **Install** next to the account you want Spacelift to access:
        ![](<../../assets/screenshots/image (59).png>)
    3. Choose whether you want to allow Spacelift access to all repositories or only specific ones in the account:
        
        ![](<../../assets/screenshots/image (60).png>)
    4. Click **Install** to link your GitHub account to Spacelift.

## Access controls

### Space-level integrations

{% if is_saas() %}
!!! hint
    This feature is only available on the Enterprise plan. Please check out our [pricing page](https://spacelift.io/pricing){: rel="nofollow"} for more information.
{% endif %}

You can use the [Spaces](../../concepts/spaces/README.md) to control what can access your integrations. For example, if you have a Space called `Rideshare`, you can create a GitHub integration in that Space, and that can only be attached to those stacks and modules that are in the same Space (or [inherit](../../concepts/spaces/access-control.md#inheritance) permissions through a parent Space).

#### Integration details visibility

Only Space **admins** will be able to see the webhook URLs and secrets of Space-level integrations. Space **readers** will only be able to see the name, description, and labels of the integration.

The details of default integrations are only visible to **root** Space admins.

### Legacy method

You can also use GitHub's native teams. If you're using GitHub as your identity provider (which is the default), upon login, Spacelift uses the                   GitHub API to determine organization membership level and team membership within an organization and persists it in the session token which is valid for one hour. Based on that token, you can set up [login policies](../../concepts/policy/login-policy.md) to determine who can log in to your Spacelift account, and [stack access policies](../../concepts/policy/stack-access-policy.md) that can grant an appropriate level of access to individual [Stacks](../../concepts/stack/README.md).

!!! info
    The list of teams is empty for individual/private GitHub accounts.

## Notifications

### Commit status notifications

Commit status notifications are triggered for [_proposed_ runs](../../concepts/run/proposed.md) to provide feedback on the proposed changes to your stack. You can trigger a proposed run using a preview command (e.g. `terraform plan` for Terraform) with the source code of a short-lived feature branch with the state and config of the stack that's pointing to another, long-lived branch. Here's what commit status notifications looks like:

1\. When the run is in progress ([initializing](../../concepts/run/README.md#initializing)):

![](../../assets/screenshots/Test_a_change_by_marcinwyszynski_·_Pull_Request__6_·_spacelift-io_marcinw-end-to-end.png)

2\. When it succeeds _without changes_:

![](<../../assets/screenshots/Test_a_change_by_marcinwyszynski_·_Pull_Request__6_·_spacelift-io_marcinw-end-to-end (2).png>)

3\. When it succeeds _with changes_:

![](<../../assets/screenshots/Test_a_change_by_marcinwyszynski_·_Pull_Request__6_·_spacelift-io_marcinw-end-to-end (1).png>)

4\. And when it fails:

![](<../../assets/screenshots/Test_a_change_by_marcinwyszynski_·_Pull_Request__6_·_spacelift-io_marcinw-end-to-end (3).png>)

In each case, clicking on the _Details_ link will take you to the GitHub check view showing more details about the run:

![](<../../assets/screenshots/Add_Azure_integration_variables_by_adamconnelly_·_Pull_Request__561_·_spacelift-io_infra (1).png>)

The check view provides high-level information about the changes introduced by the push, including the list of changing resources and cost data if [Infracost](../../vendors/terraform/infracost.md) is set up.

From this view you can also perform two types of Spacelift actions:

- **Preview**: Execute a [proposed run](../../concepts/run/proposed.md) against the tested commit.
- **Deploy**: Execute a tracked run against the tested commit.

#### PR (Pre-merge) Deployments

The _Deploy_ functionality has been introduced in response to customers used to the Atlantis approach, where the deployment happens from within a Pull Request itself rather than on merge, which we see as the default and most typical workflow.

If you want to prevent users from deploying directly from GitHub, you can add a simple [plan policy](../../concepts/policy/terraform-plan-policy.md) to that effect, based on the fact that the run trigger always indicates GitHub as the source (the exact format is `github/$username`).

```opa
package spacelift

deny["Do not deploy from GitHub"] {
  input.spacelift.run.type == "TRACKED"
  startswith(input.spacelift.run.triggered_by, "github/")
}
```

The effect is this:

![](<../../assets/screenshots/Update_README_md_·_Private_worker_pool.png>)

#### Using Spacelift checks to protect branches

You can use commit statuses to protect your branches tracked by Spacelift stacks by ensuring that _proposed_ runs succeed before merging their Pull Requests:

![Protect branches with Spacelift](<../../assets/screenshots/New_branch_protection_rule (1).png>)

This is an important part of our [proposed workflow](github.md#proposed-workflow).

##### Aggregated checks

{% if is_saas() %}
!!! info
    This feature is only available to Business plan and above. Please check out our [pricing page](https://spacelift.io/pricing){: rel="nofollow"} for more information.
{% endif %}

If you have multiple stacks tracking the same repository, you can enable the _Aggregate VCS checks_ feature in the integration's settings.

This will group all the checks from the same commit into a predefined set of checks, making it easier to see the overall status of the commit.

![](<../../assets/screenshots/aggregated-checks-github-settings.png>)

When the aggregated option is enabled, Spacelift will post the following checks:

- **spacelift/tracked**: Groups all checks from tracked runs.
- **spacelift/proposed**: Groups all checks from proposed runs.
- **spacelift/modules**: Groups all checks from module runs.

Here's how the summary looks:

![](<../../assets/screenshots/aggregated-checks-github-summary.png>)

In each case, clicking on the _Details_ link will take you to the GitHub check view showing more details about stacks or modules included in the aggregated check:

![](<../../assets/screenshots/aggregated-checks-github-details.png>)

### Deployment status notifications

[Deployments](https://developer.github.com/v3/guides/delivering-deployments/){: rel="nofollow"} and their associated statuses are created by tracked runs to indicate that changes are being made to the Terraform state. A GitHub deployment is created and marked as _Pending_ when the [planning](../../concepts/run/proposed.md#planning) phase detects changes and a [tracked run](../../concepts/run/tracked.md) either transitions to the [_Unconfirmed_](../../concepts/run/tracked.md#unconfirmed) state or automatically starts [applying](../../concepts/run/tracked.md#applying) the diff:

![](<../../assets/screenshots/Deployments_·_spacelift-io_marcinw-end-to-end (1).png>)

If the user does not like the proposed changes and [discards](../../concepts/run/tracked.md#discarded) the [tracked run](../../concepts/run/tracked.md) during the manual review, its associated GitHub deployment is immediately marked as a _Failure_. The same thing happens when the user [confirms](../../concepts/run/tracked.md#confirmed) the [tracked run](../../concepts/run/tracked.md) but the [_Applying_](../../concepts/run/tracked.md#applying) phase fails:

![](<../../assets/screenshots/Deployments_·_spacelift-io_marcinw-end-to-end (2).png>)

If the [_Applying_](../../concepts/run/tracked.md#applying) phase succeeds, the deployment is marked as _Active_:

![](<../../assets/screenshots/Deployments_·_spacelift-io_marcinw-end-to-end.png>)

Your repository's _Environments_ section displays the entire deployment history broken down by stack:

![](../../assets/screenshots/spacelift-io_infra__Infrastructure_definitions_for_Spacelift.png)

That's what it looks like for our test repo, with a single stack pointing at it:

![](<../../assets/screenshots/Deployments_·_spacelift-io_marcinw-end-to-end (4).png>)

GitHub deployment environment names are derived from their respective stack names. This can be customized by setting the `ghenv:` label on the stack. For example, if you have a stack named `Production` and you want to name the deployment environment `I love bacon`, you can set the `ghenv:I love bacon` label on the stack. You can also disable the creation of a GitHub deployments by setting the `ghenv:-` label on the stack.

!!! info
    The _Deployed_ links lead to their corresponding Spacelift [tracked runs](../../concepts/run/tracked.md).

## Pull Requests

In order to help you keep track of all the pending changes to your infrastructure, Spacelift also has a PRs tab that lists all the active Pull Requests against your tracked branch. Each of the entries shows the current status of the change as determined by Spacelift, and a link to the most recent Run responsible for determining that status:

![](<../../assets/screenshots/Pull_Requests_·_Spacelift_development.png>)

Note that this view is read-only. You can't change a Pull Request through the Spacelift UI, but clicking on the PR name will take you to GitHub where you can make changes.

Once a Pull Request is closed, either with or without merging, it disappears from this list.

## Proposed workflow

This proposed workflow has been effective for us and many other DevOps professionals working with infrastructure-as-code. Its simplest version is based on a single stack tracking a long-lived branch like _main_, and short-lived feature branches temporarily captured in Pull Requests. A more sophisticated version can involve multiple stacks and a process like [GitFlow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow){: rel="nofollow"}.

!!! tip
    These are simply suggestions and Spacelift will fit almost any Git workflow. Feel free to experiment and find what works best for you.

### Single stack version

You have a single stack named _Infra_ tracking the default `master` branch in your repository, also called `infra`. If you want to introduce some changes, for example define an Amazon S3 bucket, we suggest this workflow:

1. Open a short-lived feature branch.
2. Make your changes on the branch.
3. Open a Pull Request from that branch to `master`.

At this point, a proposed run is triggered by the push notification, and the result of running `terraform plan` with the new code (but existing state and configuration) is reported to the Pull Request.

1. Ensure that the Pull Request does not get merged to `master` without a successful run by **requiring a successful status check** from your stack.
2. Decide whether you should **require a manual review** before merging the Pull Request on top of Spacelift's automated checks.
3. If coworkers are also modifying the branch, **require branches be up-to-date before merging**.

If the current feature branch is behind the PR target branch, it needs to be rebased, which triggers a fresh Spacelift run that will ultimately produce the newest and most relevant commit status.

### Multi-stack version

A common setup involves two similar (or even identical) environments, for example, _staging_ and _production_. One approach would be to have them in a single repository but different directories, setting the [`project_root`](../../concepts/configuration/runtime-configuration/README.md#project_root-setting) runtime configuration accordingly. This approach means changing the _staging_ directory often and using as much or little duplication as necessary to keep things moving. Many commits will be no-ops for the _production_ stack. This is a very flexible approach, but it leaves Git history messy.

If you prefer a cleaner Git history:

1. Create two long-lived Git branches, each linked to a different stack: the default `staging` branch linked to the _staging_ stack, and a `production` branch linked to the _production_ stack.
2. Develop and perfect the code on the `staging` branch.
3. Open a Pull Request from the `staging` to `production` branch, incorporating all the changes.

We've seen many teams use this workflow to implement [GitFlow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow){: rel="nofollow"}. This approach keeps the history of the `production` branch clean and allows plenty of experimentation in the `staging` branch.

With this GitFlow-like setup, we propose protecting both `staging` and `production` branches in GitHub. To maximize flexibility, the `staging` branch may require a green commit status from its associated stack but not necessarily a manual review. In the meantime, the `production` branch should require **both** a manual approval and a green commit status from its associated stack.

## Webhook integrations

We subscribe to many GitHub webhooks:

| **Webhook** | **How Spacelift uses it** |
| ------- | --------------------- |
| Push events | Any time we receive a repository code push notification, we match it against Spacelift repositories and, if necessary, [create runs](../../concepts/run/README.md). We'll also **stop** _proposed_ runs that have been superseded by a newer commit on their branch. |
| App installation creation | When the Spacelift GitHub app is installed on an account, we create a corresponding Spacelift account. |
| Organization renamed | If a GitHub organization name is changed, we change the name of the corresponding account in Spacelift. (Only applicable for accounts that were created using GitHub originally.) |
| Pull request events | Whenever a Pull Request is opened or reopened, we generate a record in our database to show it on the Stack's _PRs_ page. When it's closed, we delete that record. When it's synchronized (eg. new push) or renamed, we update the record accordingly. This way, what you see in Spacelift should be consistent with what you see in GitHub. |
| Pull request review events | Whenever a review is added or dismissed from a Pull Request, we check whether a new run should be triggered based on any push policies attached to your stacks. This allows you to make decisions about whether or not to trigger runs based on the approval status of your Pull Request. |
| Repository renamed | If a GitHub repository is renamed, we update its name in all the [stacks](../../concepts/stack/stack-settings.md#vcs-integration-and-repository) pointing to it. |
| **GitHub Action** | You can use the [Setup Spacectl](https://github.com/marketplace/actions/setup-spacectl){: rel="nofollow"} GitHub Action to install our [spacectl](https://github.com/spacelift-io/spacectl){: rel="nofollow"} CLI tool to easily interact with Spacelift. |
| **Git checkout support** | By default Spacelift uses the GitHub API to download a tarball containing the source code for your stack or module. We are introducing experimental support for downloading the code using a standard Git checkout. To enable this feature for your stacks/modules, either add a label called `feature:enable_git_checkout` to each stack or module that you want to use Git checkout on (which allows you to test without switching all stacks over), or contact our support team and ask us to enable the feature for all stacks/modules in your account. |

## Unlinking GitHub and Spacelift

=== "Uninstalling the Marketplace application"

    To uninstall the Spacelift application you installed on the GitHub Marketplace:

    1. Go to your GitHub account settings and select **Applications**.
        ![](<../../assets/screenshots/CleanShot 2022-09-15 at 17.54.57.png>)
    2. Click **Configure** for the _spacelift.io_ application.
        ![](<../../assets/screenshots/CleanShot 2022-09-15 at 17.57.41.png>)
    3. Click **Uninstall**.
        ![](<../../assets/screenshots/CleanShot 2022-09-15 at 17.58.05.png>)

=== "Uninstalling the custom application"

    1. Go to the _Developer settings_ of your GitHub account.
    2. In the _GitHub Apps_ section, click **Edit** for the Spacelift application.
        ![](<../../assets/screenshots/CleanShot 2022-09-16 at 10.28.11.png>)
    3. On the page for the Spacelift application, go to the _Advanced_ section and click **Delete GitHub App**. Confirm by typing the name of the application.
        ![](<../../assets/screenshots/CleanShot 2022-09-16 at 10.24.08.png>)
    4. You can now remove the integration via **Delete** on the *Source code* page in Spacelift:
        ![](<../../assets/screenshots/Gitlab_delete.png>)

    !!! warning
        Please note that you can delete integrations **while stacks are still using them**. As a consequence, when a stack has a detached integration, it will no longer be able to receive webhooks from Github and you won't be able to trigger runs manually either.

        To fix it, you'll need to open the stack, go to the **Settings** tab and choose a new integration.
