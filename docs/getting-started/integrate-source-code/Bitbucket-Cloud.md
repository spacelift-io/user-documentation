# Use Bitbucket Cloud as your source code provider

Spacelift supports Bitbucket Cloud as the code source for your [stacks](../../concepts/stack/README.md) and [modules](../../vendors/terraform/module-registry.md).

You can set up multiple Space-level and one default Bitbucket Cloud integration per account.

## Create the Bitbucket Cloud integration

!!! tip "Bitbucket Cloud integration details"
    Learn more about setting up and using the Bitbucket integration on the [Bitbucket Cloud source control](../../integrations/source-control/bitbucket-cloud.md) page.

### Initial setup

1. On the _Source control_ tab, click **Set up integration**, then choose **Bitbucket Cloud** on the dropdown.
    ![Create a Bitbucket integration](<../../assets/screenshots/Screenshot from 2021-06-10 16-05-39.png>)
2. **Integration name**: Enter a name for your integration. It cannot be changed later because the Spacelift webhook endpoint is generated based on this name.
3. **Integration type**: Default (all spaces) or [Space-specific](../../concepts/spaces/README.md). Each Spacelift account can only support one default integration per VCS provider, which is available to all stacks and modules in the same Space as the integration.

### Create your app password

You will need to create an [app password](https://support.atlassian.com/bitbucket-cloud/docs/app-passwords/){: rel="nofollow"} for this integration on the Bitbucket Cloud site.

1. Navigate to _Personal settings_ > _App passwords_.
2. Click **Create app password**.
3. Fill in the details to create a new app password:
    ![App password creation](<../../assets/screenshots/Screenshot from 2021-06-10 16-16-53.png>)
      1. Label: Enter a descriptive name (label) for the password.
      2. Permissions: Check the **Read** box for _Repositories_ and _Pull requests_ to grant read access.
4. Click **Create**.
5. Copy the app password details to finish the integration in Spacelift.
    ![Created new app password](<../../assets/screenshots/Screenshot from 2021-06-10 16-39-03.png>)

### Copy details into Spacelift

Now that your personal access token has been created, return to the integration configuration screen in Spacelift.

1. **Username**: Enter your Bitbucket Cloud username.
2. **App password**: Paste the [app password](#create-your-app-password) that Spacelift will use to access your Bitbucket Cloud repository.
3. **Labels**: Organize integrations by assigning labels to them.
4. **Description**: A markdown-formatted free-form text field to describe the integration.
5. Click **Set up** to save your integration details.
    ![Filled integration details](<../../assets/screenshots/Screenshot from 2021-06-11 10-50-38.png>)

### Set up webhooks

For every Bitbucket Cloud repository being used in Spacelift stacks or modules, you will need to set up a webhook to notify Spacelift about project changes.

!!! note
    Default integrations are visible to all users of the account, but only **root** Space admins can see their details.

    Space-level integrations will be listed to users with **read** access to the integration Space. Integration details, however, contain sensitive information (such as the webhook secret) and are only visible to those with **admin** access.

1. On the _Source code_ page, click the **three dots** next to the integration name.
2. Click **See details** to find the _webhook endpoint_ and _webhook secret_.
    ![Find webhook endpoint and secret](<../../assets/screenshots/Screenshot from 2021-06-11 14-52-40.png>)

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

✅ Step 1 of the LaunchPad is complete! Now you can [connect your cloud account](../integrate-cloud/README.md).

![](<../../assets/screenshots/getting-started/source-code/Launchpad-step-1-complete.png>)
