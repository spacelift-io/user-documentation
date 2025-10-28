# Bitbucket Cloud

Spacelift supports Bitbucket Cloud as the code source for your [stacks](../../concepts/stack/README.md) and [modules](../../vendors/terraform/module-registry.md).

You can set up multiple Space-level and one default Bitbucket Cloud integration per account.

## Create the Bitbucket Cloud integration

### Initial setup

1. On the _Integrate Services > Discover all integrations_ screen, click **View** on the _Bitbucket Cloud_ card, then **Set up Bitbucket Cloud**.
    ![Create a Bitbucket integration](<../../assets/screenshots/Bitbucket-cloud-form.png>)
2. **Integration name**: Enter a name for your integration. It cannot be changed later because the Spacelift webhook endpoint is generated based on this name.
3. **Integration type**: Default (all spaces) or [Space-specific](../../concepts/spaces/README.md). Each Spacelift account can only support one default integration per VCS provider, which is available to all stacks and modules in the same Space as the integration.

!!! warning "Migration from App Passwords to API Tokens"
    Previously, this integration used Bitbucket App Passwords for authentication. Atlassian has deprecated App Passwords and [replaced them with API tokens](https://www.atlassian.com/blog/bitbucket/bitbucket-cloud-transitions-to-api-tokens-enhancing-security-with-app-password-deprecation){: rel="nofollow"}.

### Create your API token

You will need to create an [API token](https://support.atlassian.com/bitbucket-cloud/docs/using-api-tokens){: rel="nofollow"} for this integration on the Bitbucket Cloud site.

1. Navigate to **Atlassian account settings** > **Security** > **Create API token with scopes**.
2. Fill in the details to create a new API token:
    1. Choose a name for your API token.
    2. Set an expiration date.
    3. Select **Bitbucket** as the app.

        ![Api token app](<../../assets/screenshots/api-token-app.png>)

    4. Select read permissions for:
        - Repository
        - Pull requests

        ![Api token permissions](<../../assets/screenshots/api-token-permissions.png>)

3. Click **Create**.
4. Copy the API token details to finish the integration in Spacelift.

### Copy details into Spacelift

Now that your API token has been created, return to the integration configuration screen in Spacelift.

1. **Email**: Enter your Bitbucket Cloud email address.
2. **API token**: Paste the [API token](#create-your-api-token) that Spacelift will use to access your Bitbucket Cloud repository.
3. **Labels**: Organize integrations by assigning labels to them.
4. **Description**: A markdown-formatted free-form text field to describe the integration.
5. Click **Set up** to save your integration details.
    ![Filled integration details](<../../assets/screenshots/Bitbucket-cloud-form-filled.png>)

### Set up webhooks

For every Bitbucket Cloud repository being used in Spacelift stacks or modules, you will need to set up a webhook to notify Spacelift about project changes.

!!! note
    Default integrations are visible to all users of the account, but only **root** Space admins can see their details.

    Space-level integrations will be listed to users with **read** access to the integration Space. Integration details, however, contain sensitive information (such as the webhook secret) and are only visible to those with **admin** access.

1. On the _Integrate Services > Discover all integrations_ page, click **View** on the _Bitbucket Cloud_ card, then click the **three dots** next to the integration name.
2. Click **See details** to find the _webhook endpoint_ and _webhook secret_.
    ![Find webhook endpoint and secret](<../../assets/screenshots/Bitbucket-cloud-integration-details.png>)

#### Configure webhooks in Bitbucket Cloud

For each repository you want to use with Spacelift, you now need to add webhooks in Bitbucket Cloud.

1. In Bitbucket Cloud, select the repository you are connecting to Spacelift.
2. Navigate to _Repository settings_ > _Webhooks_.
3. Click **Add webhook**.
    ![Webhooks configuration](<../../assets/screenshots/bitbucket-cloud-webhook-settings.png>)
4. **Title**: Enter a name for the webhook.
5. **URL**: Paste the _webhook endpoint_ from Spacelift.
6. **Secret**: Paste the _webhook secret_ from Spacelift.
7. **Status**: Check **Active**.
8. **Triggers**:
      1. Under _Repository_, check **Push**.
      2. Under _Pull Request_, check:
         - **Created**
         - **Updated**
         - **Approved**
         - **Approval removed**
         - **Merged**
         - **Comment created**
9. Click **Save**.

#### Install Pull Request Commit Links app

Finally, you should install the **Pull Request Commit Links** app to be able to use [this API](https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/commit/%7Bcommit%7D/pullrequests){: rel="nofollow"}. The app is installed automatically when you go to the commit's details and click **Pull requests**.

![Commit's details](<../../assets/screenshots/Screenshot from 2021-06-15 11-19-56.png>)

## Use the Bitbucket Cloud integration

When creating a stack, you will now be able to choose the Bitbucket Cloud provider and a repository inside of it:

![Stack creation form](<../../assets/screenshots/Screenshot from 2021-06-11 15-03-21.png>)

### Troubleshooting

If you're receiving a [401 error](https://confluence.atlassian.com/bitbucketserverkb/bitbucket-server-backup-client-401-unauthorized-779171351.html), use this command to check the username and password:

```bash
curl -v -u your_username:some_app_password "https://api.bitbucket.org/2.0/workspaces/workspace_id"
```

And this to check if some repositories may not be showing up:

```bash
curl -s -u your_username:some_app_password "https://api.bitbucket.org/2.0/repositories" | jq
```

## Use Spacelift checks to protect branches

You can use commit statuses to protect your branches tracked by Spacelift stacks by ensuring that _proposed_ runs succeed before merging their Pull Requests.

### Aggregated checks

{% if is_saas() %}
!!! info
    This feature is only available to Business plan and above. Please check out our [pricing page](https://spacelift.io/pricing){: rel="nofollow"} for more information.
{% endif %}

If you have multiple stacks tracking the same repository, you can enable the _Aggregate VCS checks_ feature in the integration's settings. This will group all the checks from the same commit into a predefined set of checks, making it easier to see the overall status of the commit.

![Enable aggregated checks](<../../assets/screenshots/aggregated-checks-bitbucketcloud-settings.png>)

When the aggregated option is enabled, Spacelift will post the following checks:

- **spacelift/tracked**: Groups all checks from tracked runs
- **spacelift/proposed**: Groups all checks from proposed runs
- **spacelift/modules**: Groups all checks from module runs

The summary will look like this:

![Aggregated checks summary](<../../assets/screenshots/aggregated-checks-bitbucketcloud-summary.png>)

## Delete the Integration

If you no longer need the integration, you can delete it by clicking the 3 dots next to the integration name on the _Integrations > Bitbucket Cloud_ page, and then clicking **Delete**. You need **admin** access to the integration Space to be able to delete it.

![Delete the Azure DevOps integration](<../../assets/screenshots/azure_devops_deletion_button.png>)

!!! warning
    You can delete source code integrations **while stacks are still using them**, which will have consequences.

### Consequences

When a stack has a detached integration, it will no longer be able to receive webhooks from Bitbucket and you won't be able to trigger runs manually either.

To fix the issue, click the stack name on the _Stacks_ tab, navigate to the **Settings** tab, and choose a new integration.

!!! tip
    You can save a little time if you create the new integration with the exact same name as the old one. This way, the webhook URL will remain the same and you won't have to update it in Bitbucket.
