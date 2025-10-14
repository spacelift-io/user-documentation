# Use GitHub as your source code provider

Spacelift is deeply integrated with GitHub, providing organizations a simple way to manage IaC versioned in GitHub.

You can set up multiple Space-level and one default GitHub integration per account.

!!! info "Using multiple GitHub accounts"
    If you want to use multiple GitHub accounts or organizations, or connect Spacelift to your GitHub Enterprise instance, you will need to set up a custom GitHub integration via a [GitHub App](GitHub.md#create-the-github-application).

{% if is_saas() %}
 If you used GitHub to create your Spacelift account, the flow for also connecting GitHub as your [VCS provider](./README.md) is slightly different. Select the option that applies to your account:

1. Created Spacelift account with [GitHub](GitHub.md#signed-in-with-github).
2. Created Spacelift account with [GitLab, Google, or Microsoft](GitHub.md#signed-in-with-another-option).

!!! tip "GitHub integration details"
    Learn more about setting up and using the GitHub integration on the [GitHub source control page](../../integrations/source-control/github.md).

## Signed in with GitHub

1. [Install the Spacelift GitHub App](https://github.com/apps/spacelift-io/installations/new){: rel="nofollow"} from the GitHub Marketplace.
2. Select the GitHub repository or repositories to manage in Spacelift.
      - If you do not have a GitHub repository of this kind, you can fork our [terraform-starter repository](https://github.com/spacelift-io/terraform-starter){: rel="nofollow"}. Allow the installed GitHub app access to the forked repository.

![](<../../assets/screenshots/InstallAppGS.png>)

## Signed in with another option

If you used GitLab, Google, or Microsoft to create your account, you will need to create a custom GitHub application to link it to Spacelift.

{% else %}

## Create and link a custom application

You will need a GitHub Enterprise account to create a custom GitHub application to link it to Spacelift.
{% endif %}

### Create the GitHub application

1. On the _Source control_ tab, click **Set up integration**, then choose **GitHub** on the dropdown.
2. Click [**Set up via wizard**](GitHub.md#set-up-via-wizard) (_recommended_) or [**Set up manually**](GitHub.md#set-up-manually).

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

     | Permission | Access    |
     | ---------- | --------- |
     | Members    | Read-only |

7. Subscribe to the following events:
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

✅ Step 1 of the LaunchPad is complete! Now you can [connect your cloud account](../integrate-cloud/README.md).

![LaunchPad step 1 complete](<../../assets/screenshots/getting-started/source-code/Launchpad-step-1-complete.png>)
