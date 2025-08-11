# Use GitLab as your source code provider

Spacelift supports GitLab as the code source for your [stacks](../../concepts/stack/README.md) and [modules](../../vendors/terraform/module-registry.md).

You can set up multiple Space-level and one default GitLab integration per account.

!!! info "Using multiple GitLab accounts"
    If you want to use multiple GitLab accounts, teams, or groups, or connect Spacelift to your GitLab Enterprise instance, you will need to set up separate GitLab integrations (with different access tokens) for each different team or group in GitLab.

## Create the GitLab integration

!!! tip "GitLab integration details"
    Learn more about setting up and using the GitLab integration on the [GitLab source control page](../../integrations/source-control/gitlab.md).

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

✅ Step 1 of the LaunchPad is complete! Now you can [connect your cloud account](../integrate-cloud/README.md).

![](<../../assets/screenshots/getting-started/source-code/Launchpad-step-1-complete.png>)
