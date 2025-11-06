# Bitbucket Datacenter/Server

Spacelift supports Bitbucket Data Center (on-premise) as the code source for your [stacks](../../concepts/stack/README.md) and [modules](../../vendors/terraform/module-registry.md).

You can set up multiple Space-level and one default Bitbucket Data Center integration per account.

## Create the Bitbucket Data Center integration

### Initial setup

1. On the _Integrate Services > Discover all integrations_ screen, click **View** on the _Bitbucket Data Center_ card, then **Set up Bitbucket Data Center**.
    ![Create a Bitbucket integration](<../../assets/screenshots/BitbucketDatacenter_create_form.png>)
2. **Integration name**: Enter a name for your integration. It cannot be changed later because the Spacelift webhook endpoint is generated based on this name.
3. **Integration type**: Default (all spaces) or [Space-specific](../../concepts/spaces/README.md). Each Spacelift account can only support one default integration per VCS provider, which is available to all stacks and modules in the same Space as the integration.

### Create an access token

You will need to create an access token in Bitbucket to use with Spacelift. The token requires the following access:

- _Read_ access to any projects Spacelift needs to be able to access.
- _Read_ access to the repositories within those projects.

![Personal token creation](<../../assets/screenshots/image (65).png>)

1. Navigate to _Manage account_ > _Personal access tokens_.
2. Click **Create**.
3. **Name**: Enter a descriptive name for the token.
4. **Permissions > Projects**: Select **Read**.
5. **Permissions > Repositories**: Select **Read**.
6. **Automated expiry**: Select **No**.
7. Click **Create**.
    ![Created personal token](<../../assets/screenshots/image (66).png>)
8. Copy the token details to finish the integration in Spacelift.

### Copy details into Spacelift

Now that your Bitbucket Data Center access token has been created, return to the integration configuration screen in Spacelift.

1. **API host URL**: Enter the URL of your Bitbucket server. This will likely use a format like: `https://bitbucket.<myorganization>.com`
2. **User facing host URL**: Enter the URL that will be shown to the user and displayed in the Spacelift UI. This will be the same as the API host URL unless you are using [VCS Agents](../../concepts/vcs-agent-pools.md), in which case it should be `private://<vcs-agent-pool-name>`.
3. **Username**: Enter the username for the Bitbucket account where you created the access token.
4. **Access token**: Enter the access token that Spacelift will use to access your Bitbucket.
5. **Labels**: Organize integrations by assigning labels to them.
6. **Description**: A markdown-formatted free-form text field to describe the integration.
7. **Use Git checkout**: Toggle that defines if integration should use git checkout to download source code, otherwise source code will be downloaded as archive through API. This is required for [sparse checkout](../../concepts/stack/stack-settings.md#git-sparse-checkout-paths) to work.
8. Click **Set up** to save your integration settings.

![Completed integration](<../../assets/screenshots/BitbucketDatacenter_save_form.png>)

### Set up webhooks

For every Bitbucket Data Center repository being used in Spacelift stacks or modules, you will need to set up a webhook to notify Spacelift about project changes.

!!! note
    Default integrations are visible to all users of the account, but only **root** Space admins can see their details.

    Space-level integrations will be listed to users with **read** access to the integration Space. Integration details, however, contain sensitive information (such as the webhook secret) and are only visible to those with **admin** access.

1. On the _Integrate Services > Discover all integrations_ page, click **View** on the _Bitbucket Data Center_ card, then click the **three dots** next to the integration name.
2. Click **See details** to find the _webhook endpoint_ and _webhook secret_.
    ![Find webhook endpoint and secret](<../../assets/screenshots/BitbucketDatacenter_details.png>)

#### Configure webhooks in Bitbucket Data Center

For each repository you want to use with Spacelift, you now need to add webhooks in Bitbucket Data Center.

1. In Bitbucket Data Center, select the repository you are connecting to Spacelift.
2. Navigate to _Repository settings_ > _Webhooks_.
3. Click **Add webhook**.
    ![Configuring Webhooks](<../../assets/screenshots/bitbucket-datacenter-webhook-settings.png>)
4. **Title**: Enter a name for the webhook.
5. **URL**: Paste the _webhook endpoint_ from Spacelift.
6. **Secret**: Paste the _webhook secret_ from Spacelift.
7. **Status**: Check **Active**.
8. **Triggers**:
      1. Under _Repository_, check **Push**.
      2. Under _Pull Request_, check:
         - **Opened**
         - **Source branch updated**
         - **Modified**
         - **Approved**
         - **Unapproved**
         - **Merged**
         - **Comment added**
9. Click **Save**.

!!! warning
    Don't forget to enter a secret when configuring your webhook. Bitbucket will allow you to create your webhook with no secret specified, but any webhook requests to Spacelift will fail without one configured.

#### Install Pull Request Commit Links app

Finally, you should install the **Pull Request Commit Links** app to be able to use [this API](https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/commit/%7Bcommit%7D/pullrequests){: rel="nofollow"}. The app is installed automatically when you go to the commit's details and click **Pull requests**.

![Commit's details](<../../assets/screenshots/Screenshot from 2021-06-15 11-19-56.png>)

## Use the integration

When creating a stack, you will now be able to choose the Bitbucket Data Center provider and a repository inside of it:

![Creating a Stack with the Bitbucket Data Center integration](<../../assets/screenshots/BitbucketDatacenter_create_stack.png>)

### Using Spacelift checks to protect branches

You can use commit statuses to protect your branches tracked by Spacelift stacks by ensuring that _proposed_ runs succeed before merging their Pull Requests.

#### Aggregated checks

{% if is_saas() %}
!!! info
    This feature is only available to Business plan and above. Please check out our [pricing page](https://spacelift.io/pricing){: rel="nofollow"} for more information.
{% endif %}

If you have multiple stacks tracking the same repository, you can enable the _Aggregate VCS checks_ feature in the integration's settings. This will group all the checks from the same commit into a predefined set of checks, making it easier to see the overall status of the commit.

![Enable aggregated checks](<../../assets/screenshots/aggregated-checks-bitbucketserver-settings.png>)

When the aggregated option is enabled, Spacelift will post the following checks:

- **spacelift/tracked**: Groups all checks from tracked runs
- **spacelift/proposed**: Groups all checks from proposed runs
- **spacelift/modules**: Groups all checks from module runs

The summary should look like this:

![Summary with aggregated checks](<../../assets/screenshots/aggregated-checks-bitbucketserver-summary.png>)

## Delete the integration

If you no longer need the integration, you can delete it by clicking the 3 dots next to the integration name on the _Integrations > Bitbucket Data Center_ page, and then clicking **Delete**. You need **admin** access to the integration Space to be able to delete it.

![Delete the integration](<../../assets/screenshots/BitbucketDatacenter_deletion_button.png>)

!!! warning
    You can delete integrations **while stacks are still using them**, which will have consequences.

### Consequences

When a stack has a detached integration, it will no longer be able to receive webhooks from Bitbucket Data Center and you won't be able to trigger runs manually either.

![Detached stack](<../../assets/screenshots/BitbucketDatacenter_detached_stack.png>)

To fix the issue, click the stack name on the _Stacks_ tab, navigate to the **Settings** tab, and choose a new integration.

!!! tip
    You can save a little time if you create the new integration with the exact same name as the old one. This way, the webhook URL will remain the same and you won't have to update it in Bitbucket Data Center. You will still need to update the webhook secret though.
