# GitLab

Spacelift supports GitLab as the code source for your [stacks](../../concepts/stack/README.md) and [modules](../../vendors/terraform/module-registry.md).

You can set up multiple Space-level and one default GitLab integration per account.

!!! info "Using multiple GitLab accounts"
    If you want to use multiple GitLab accounts, teams, or groups, or connect Spacelift to your GitLab Enterprise instance, you will need to set up separate GitLab integrations (with different access tokens) for each different team or group in GitLab.

## Create the GitLab integration

### Initial setup

1. On the _Source control_ tab, click **Set up integration**, then choose **GitLab** on the dropdown.
    ![Create a GitLab integration](<../../assets/screenshots/Gitlab_create_form.png>)
2. **Integration name**: Enter a name for your integration. It cannot be changed later because the Spacelift webhook endpoint is generated based on this name.
3. **Integration type**: Default (all spaces) or [Space-specific](../../concepts/spaces/README.md). Each Spacelift account can only support one default integration per VCS provider, which is available to all stacks and modules in the same Space as the integration.

### Create an access token

Assuming you don't already have an access token at the ready, navigate to your GitLab server (we'll just use `gitlab.com`) to create one from the _Access Tokens_ section of your _User Settings_ page:

![Create a GitLab access token](<../../assets/screenshots/Personal_Access_Tokens_·_User_Settings_·_GitLab_and_Slack___Zuzia___office-space.png>)

1. **Name**: Enter a descriptive name for the token.
2. **Expires at**: We recommend leaving this blank. If set and the token expires before being replaced, Spacelift won't be able to access your GitLab environment.
3. **Scopes**: Check the `api` box. While Spacelift will only write commit statuses, merge request comments, and environment deployments, GitLab's permissions require us to take _write_ access on everything.
4. Create the token and copy its details to finish the integration in Spacelift.

!!! tip "Required user access level"
    When creating tokens bound to a GitLab user, the user is required to have "Maintainer" level access to any projects you require Spacelift to access.

### Copy details into Spacelift

Now that your GitLab access token has been created, return to the integration configuration screen in Spacelift.

1. **API host URL**: Enter the URL of your GitLab server. For SaaS GitLab, this is `https://gitlab.com`.
2. **User facing host URL**: Enter the URL that will be shown to the user and displayed in the Spacelift UI. This will be the same as the API host URL unless you are using [VCS Agents](../../concepts/vcs-agent-pools.md), in which case it should be `private://<vcs-agent-pool-name>`.
3. **API token**: Enter the access token that Spacelift will use to access your GitLab.
4. **Labels**: Organize integrations by assigning labels to them.
5. **Description**: A markdown-formatted free-form text field to describe the integration.
6. Click **Set up** to save your integration settings.

!!! warning
    Unlike GitHub credentials (which are organization-specific), the GitLab integration uses personal credentials, which makes it more fragile in situations where an individual leaves the organization and deletes the access token. This is a general concern across your environment, not one specific to Spacelift.

    We recommend you create "virtual" (machine) users in GitLab as a source of more stable credentials.

### Set up webhooks

For every GitLab project being used in Spacelift stacks or modules, you will need to set up a webhook to notify Spacelift about the project changes.

!!! note
    Default integrations are visible to all users of the account, but only **root** Space admins can see their details.

    Space-level integrations will be listed to users with **read** access to the integration Space. Integration details, however, contain sensitive information (such as the webhook secret) and are only visible to those with **admin** access.

1. On the _Source code_ page, click the **three dots** next to the integration name.
2. Click **See details** to find the _webhook endpoint_ and _webhook secret_.
    ![Find webhook endpoint and secret](<../../assets/screenshots/Gitlab_details_highlight.png>)
3. In GitLab, navigate to _Settings_ > _Webhooks_ to create a new webhook.
    ![Set webhooks in GitLab](<../../assets/screenshots/Webhooks_·_Settings_·_spacelift-test___demo_·_GitLab.png>)
      1. **URL**: Enter the _webhook endpoint_ from Spacelift.
      2. **Secret Token**: Enter the _webhook secret_ from Spacelift.
      3. **Trigger**: Check the **Push events**, **Tag push events**, and **Merge request events** boxes.
4. Complete the webhook setup in GitLab.

!!! warning
    You only need to set up one hook for each repository used by Spacelift, regardless of how many stacks use it. Setting up multiple hooks for a single repo may lead to unintended behavior.

You can also set up GitLab webhooks automatically using [GitLab's Terraform provider](https://registry.terraform.io/providers/gitlabhq/gitlab/latest/docs/resources/project_hook){: rel="nofollow"}.

Regardless of whether you've created it manually or programmatically, once your project webhook is set up, your GitLab-powered stack or module is ready to use.

### Use GitLab with stacks and modules

If your Spacelift account is integrated with GitLab, the creation and editing forms for stacks and modules will display GitLab as a source code option:

![Create a stack with GitLab](<../../assets/screenshots/Gitlab_create_stack.png>)

The rest of the process is exactly the same as with [creating a GitHub-backed stack](../../concepts/stack/creating-a-stack.md#2-connect-to-source-code) or module, so we won't be going into further details.

### Namespaces

When using the Terraform provider to provision Spacelift stacks for GitLab, you are required to specify a `namespace`.

The `namespace` value should be set to the group that your project (repository) is within. For example, if you are simply referencing a project (repository) within your GitLab account that is not within any group, then the namespace value should be set to your GitLab account username.

If your project lives within a group, then the namespace should be set to the project group's slug. For example, if you have `project-a` within `group-1` the namespace would be `group-1`. When using subgroups, you will also need to include these within your namespace references.

GitLab provides a [Namespaces API](https://docs.gitlab.com/ee/api/namespaces.html){: rel="nofollow"} which you can use to find information about your project's namespace. Reference the `full_url` attribute value as this namespace for a given project.

## Spacelift in GitLab

Spacelift provides feedback to GitLab in a number of ways.

### Commits and merge requests

When a webhook containing a push or tag event is received by Spacelift, it may trigger a [test run](../../concepts/run/README.md). Test runs provide feedback though GitLab's [pipeline](https://docs.gitlab.com/ee/ci/pipelines/){: rel="nofollow"} functionality. When viewed from a merge request, the pipeline looks like this:

![GitLab PR View](<../../assets/screenshots/Gitlab_pr_1.png>)

Click through to a pipeline's dedicated view to see all the Spacelift jobs executed as part of it:

![GitLab pipeline dedicated view](<../../assets/screenshots/Gitlab_pr_2.png>)

As you can see, the test job passed and gave some brief information about the proposed change that, if applied, would add a single resource.

Also, for every merge request affected by the commit there will be a comment showing the exact change:

![GitLab merge comment](<../../assets/screenshots/Gitlab_pr_3.png>)

### Use Spacelift checks to protect branches

You can use commit statuses to protect your branches tracked by Spacelift stacks by ensuring that _proposed_ runs succeed before merging their Merge Requests.

#### Aggregated checks

{% if is_saas() %}
!!! info
    This feature is only available to Business plan and above. Please check out our [pricing page](https://spacelift.io/pricing){: rel="nofollow"} for more information.
{% endif %}

If you have multiple stacks tracking the same repository, you can enable the _Aggregate VCS checks_ feature in the integration's settings. This will group all the checks from the same commit into a predefined set of checks, making it easier to see the overall status of the commit.

![Enable aggregated VCS checks](<../../assets/screenshots/aggregated-checks-gitlab-settings.png>)

When the aggregated option is enabled, Spacelift will post the following checks:

- **spacelift/tracked**: Groups all checks from tracked runs
- **spacelift/proposed**: Groups all checks from proposed runs
- **spacelift/modules**: Groups all checks from module runs

The summary will look like this:

![Summary view](<../../assets/screenshots/aggregated-checks-gitlab-summary.png>)

### Environments

Each Spacelift stack creates an [Environment](https://docs.gitlab.com/ee/ci/environments/){: rel="nofollow"} in GitLab where we report the status of each [tracked run](../../concepts/run/README.md).

For example, this successful run is reflected in its respective GitLab environment:

![Successful run in Spacelift](<../../assets/screenshots/Gitlab_successful_run.png>)
![Successful run in GitLab](<../../assets/screenshots/Gitlab_environment_after.png>)

This functionality allows you to track Spacelift history directly from GitLab.

## Delete the GitHub integration

If you no longer need the integration, you can delete it by clicking the 3 dots next to the integration name on the **Source code** page, and then clicking **Delete**. You need **admin** access to the integration Space to be able to delete it.

![Delete GitLab integration](<../../assets/screenshots/Gitlab_delete.png>)

!!! warning
    You can delete integrations **while stacks are still using them**, which will have consequences.

### Consequences

When a stack has a detached integration, it will no longer be able to receive webhooks from GitLab and you won't be able to trigger runs manually either.

![Detached GitLab stack](<../../assets/screenshots/Gitlab_detached_stack.png>)

To fix the issue, click the stack name on the _Stacks_ tab, navigate to the **Settings** tab, and choose a new integration.

!!! tip
    You can save a little time if you create the new integration with the exact same name as the old one. This way, the webhook URL will remain the same and you won't have to update it in GitLab. You will still need to update the webhook secret though.
