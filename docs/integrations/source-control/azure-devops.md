# Azure DevOps

Spacelift supports Azure DevOps as the code source for your [stacks](../../concepts/stack/README.md) and [modules](../../vendors/terraform/module-registry.md).

You can set up multiple Space-level and one default Azure DevOps integration per account.

## Create the Azure DevOps integration

### Initial setup

1. On the _Integrate Services > Discover all integrations_ screen, click **View** on the _Azure DevOps_ card, then **Set up Azure DevOps**.
    ![Create an Azure DevOps integration](<../../assets/screenshots/azure_devops_fresh_form.png>)
2. **Integration name**: Enter a name for your integration. It cannot be changed later because the Spacelift webhook endpoint is generated based on this name.
3. **Integration type**: Default (all spaces) or [Space-specific](../../concepts/spaces/README.md). Each Spacelift account can only support one default integration per VCS provider, which is available to all stacks and modules in the same Space as the integration.

### Find your organization URL

You will need your [Azure DevOps organization URL](https://docs.microsoft.com/en-us/azure/devops/release-notes/2018/sep-10-azure-devops-launch#administration){: rel="nofollow"}, which usually follows this format: `https://dev.azure.com/{my-organization-name}`.

!!! tip
    Depending on when your Azure DevOps organization was created, it may use a different format, for example: `https://{my-organization-name}.visualstudio.com`.

![Azure DevOps main organization page](../../assets/screenshots/azureDevOps1.png)

1. Navigate to your main organization page in Azure DevOps.
2. Copy the Azure DevOps organization URL.

### Create a personal access token

You need to create a [personal access token](https://docs.microsoft.com/en-us/azure/devops/organizations/accounts/use-personal-access-tokens-to-authenticate){: rel="nofollow"} in Azure DevOps to create the integration with Spacelift.

1. Navigate to _User settings_ > _Personal access tokens_ in the top-right section of the Azure DevOps page.

    ![Personal access tokens menu in Azure DevOps](<../../assets/screenshots/azureDevOpsPersonalAccessToken1.png>)

2. Click **New Token**.
3. Fill in the details to create a new personal access token:
    ![Creating a new personal access token in Azure DevOps](<../../assets/screenshots/azureDevOpsPersonalAccessToken3.png>)
    1. **Name**: Enter a descriptive name for the token.
    2. **Organization**: Select the organization to connect to Spacelift.
    3. **Expiration**: Select an expiration date for the token.
    4. **Scopes**: Select **Custom defined**, then check **Read & write** in the _Code_ section.
4. Click **Create**.
5. Copy the token details to finish the integration in Spacelift.
    ![Successfully created Personal Access Token in Azure DevOps](<../../assets/screenshots/azureDevOpsPeronalAccessToken5.png>)

### Copy details into Spacelift

Now that your personal access token has been created, return to the integration configuration screen in Spacelift.

1. **Organization URL**: Paste your [Azure DevOps organization URL](#find-your-organization-url).
2. **User facing host URL**: Enter the URL that will be shown to the user and displayed in the Spacelift UI. This will be the same as the API host URL unless you are using [VCS Agents](../../concepts/vcs-agent-pools.md), in which case it should be `private://<vcs-agent-pool-name>/<azure-organization-name>`.
3. **Personal access token**: Paste the [personal access token](#create-a-personal-access-token) that Spacelift will use to access your Azure DevOps organization.
4. **Labels**: Organize integrations by assigning labels to them.
5. **Description**: A markdown-formatted free-form text field to describe the integration.
6. **Use Git checkout**: Toggle that defines if integration should use git checkout to download source code, otherwise source code will be downloaded as archive through API. This is required for [sparse checkout](../../concepts/stack/stack-settings.md#git-sparse-checkout-paths) to work.
7. Click **Set up** to save your integration details.

### Set up webhooks

For every Azure DevOps repository being used in Spacelift stacks or modules, you will need to set up a webhook to notify Spacelift about project changes.

!!! note
    Default integrations are visible to all users of the account, but only **root** Space admins can see their details.

    Space-level integrations will be listed to users with **read** access to the integration Space. Integration details, however, contain sensitive information (such as the webhook secret) and are only visible to those with **admin** access.

1. On the _Integrate Services > Discover all integrations_ page, click **View** on the _Azure DevOps_ card, then click the **three dots** next to the integration name.
2. Click **See details** to find the _webhook endpoint_ and _webhook secret_.
    ![Find webhook endpoint and secret](<../../assets/screenshots/azure_devops_details.png>)

#### Configure webhooks in Azure DevOps

1. In Azure DevOps, select the project you are connecting to Spacelift.
2. Navigate to _Project settings_ > _Service hooks_.
3. Click **Create subscription**, then select **Web Hooks** and click **Next**.
    ![Create webhooks in Azure DevOps](<../../assets/screenshots/azureWebhooks1.gif>)
4. On the _Trigger_ page of the _New Service Hooks Subscription_ window:
      1. **Trigger on this type of event**: Select **Code pushed**, then click **Next**.
    ![Creating Code pushed webhook integration in Azure DevOps](<../../assets/screenshots/azureWebhooks2.png>)
5. In the _Settings_ section of the _Action_ page:
    ![Configuring webhook integration in Azure DevOps](<../../assets/screenshots/azureWebhooks3.png>)
      1. **URL**: Enter the _webhook endpoint_ from Spacelift.
      2. **Basic authentication username**: Leave blank.
      3. **Basic authentication password**: Enter the _webhook secret_ from Spacelift.
6. Click **Finish**.
7. **Repeat steps 3 through 6** for the following event triggers:
      - Pull request created.
      - Pull request merge attempted.
      - Pull request updated.
      - Pull request commented on.

Once all hooks are created, you should see them on the _Service Hooks_ page.

![Service Hooks page with four configured webhook integrations in Azure DevOps](<../../assets/screenshots/image (108) (1).png>)

## Use the integration

When creating a stack, you will now be able to choose the Azure DevOps provider and a repository inside of it:

![Use Azure DevOps when creating a stack](<../../assets/screenshots/azure_devops_stack_creation.png>)

### Using Spacelift checks to protect branches

Use commit statuses to protect your branches tracked by Spacelift stacks by ensuring that _proposed_ runs succeed before merging their Pull Requests.

#### Aggregated checks

{% if is_saas() %}
!!! info
    This feature is only available to Business plan and above. Please check out our [pricing page](https://spacelift.io/pricing){: rel="nofollow"} for more information.
{% endif %}

If you have multiple stacks tracking the same repository, you can enable the _Aggregate VCS checks_ feature in the integration's settings. This will group all the checks from the same commit into a predefined set of checks, making it easier to see the overall status of the commit.

![Enable aggregated VCS checks](<../../assets/screenshots/aggregated-checks-azuredevops-settings.png>)

When the aggregated option is enabled, Spacelift will post the following checks:

- **spacelift/tracked**: Groups all checks from tracked runs
- **spacelift/proposed**: Groups all checks from proposed runs
- **spacelift/modules**: Groups all checks from module runs

The summary will look like this:

![Aggregated checks summary](<../../assets/screenshots/aggregated-checks-azuredevops-summary.png>)

#### Receiving checks in pull requests

For Spacelift to be able to send checks to pull requests, it has to include an iteration ID as part of the check. This information is only available on pull request events. To make this work, please make sure the push policy triggers proposed runs from pull request events, like in the example below. The default push policy does not guarantee that.

```rego
propose if {
    affected_pr
}

affected_pr if {
    filepath := input.pull_request.diff[_]
    startswith(normalize_path(filepath), normalize_path(input.stack.project_root))
}

normalize_path(path) := trim(path, "/")
```

## Delete the integration

If you no longer need the integration, delete it by clicking the 3 dots next to the integration name on the _Integrations > Azure DevOps_ page, and then clicking **Delete**. You need **admin** access to the integration Space to be able to delete it.

![](<../../assets/screenshots/azure_devops_deletion_button.png>)

!!! warning
    You can delete integrations **while stacks are still using them**, which will have consequences.

### Consequences

When a stack has a detached integration, it will no longer be able to receive webhooks from Azure DevOps and you won't be able to trigger runs manually either.

To fix the issue, click the stack name on the _Stacks_ tab, navigate to the **Settings** tab, and choose a new integration.

!!! tip
    You can save a little time if you create the new integration with the exact same name as the old one. This way, the webhook URL will remain the same and you won't have to update it in Azure DevOps. You will still need to update the webhook secret though.
