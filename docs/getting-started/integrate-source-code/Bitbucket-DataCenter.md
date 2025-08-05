# Use Bitbucket Data Center as your source code provider

Spacelift supports Bitbucket Data Center (on-premise) as the code source for your [stacks](../../concepts/stack/README.md) and [modules](../../vendors/terraform/module-registry.md).

You can set up multiple Space-level and one default Bitbucket Data Center integration per account.

## Create the Bitbucket Data Center integration

!!! tip "Bitbucket Data Center integration details"
    Learn more about setting up and using the Bitbucket integration on the [Bitbucket Data Center source control](../../integrations/source-control/bitbucket-datacenter-server.md) page.

### Initial setup

1. On the _Source control_ tab, click **Set up integration**, then choose **Bitbucket Data Center** on the dropdown.
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
7. Click **Set up** to save your integration settings.

![Completed integration](<../../assets/screenshots/BitbucketDatacenter_save_form.png>)

### Set up webhooks

For every Bitbucket Data Center repository being used in Spacelift stacks or modules, you will need to set up a webhook to notify Spacelift about project changes.

!!! note
    Default integrations are visible to all users of the account, but only **root** Space admins can see their details.

    Space-level integrations will be listed to users with **read** access to the integration Space. Integration details, however, contain sensitive information (such as the webhook secret) and are only visible to those with **admin** access.

1. On the _Source code_ page, click the **three dots** next to the integration name.
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

✅ Step 1 of the LaunchPad is complete! Now you can [connect your cloud account](../integrate-cloud/README.md).

![](<../../assets/screenshots/getting-started/source-code/Launchpad-step-1-complete.png>)
