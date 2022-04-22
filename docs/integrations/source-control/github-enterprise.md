# GitHub Enterprise

In addition to our out-of-the-box [integration with GitHub](github.md), Spacelift also supports using GitHub Enterprise as the source of code for your stacks and modules. Only one GitHub Enterprise server can be used by a single Spacelift account.

## Setting up the integration

In order to set up the integration from the Spacelift side, please navigate to the VCS Providers section of the admin Settings page and click the _Set up_ button next to the GitHub Enterprise integration:

![](/assets/images/image%20%2895%29.png)

This should open a form like this one:

![](/assets/images/image%20%2897%29.png)

### Create a GitHub App

Before you can complete this step you need to create a GitHub App in your GitHub Enterprise server. You will need the Webhook endpoint and Webhook secret while creating your App, so take a note of them.

You can either create the App in a user account or an organization account. Start by navigating to the _GitHub Apps_ page in the _Developer Settings_ for your account, and clicking on _New GitHub App:_

![](/assets/images/image%20%2852%29.png)

Give your app a name and homepage URL (these are only used for informational purposes within GitHub):

![](/assets/images/image%20%2853%29.png)

Enter your Webhook URL and secret:

![](/assets/images/image%20%2854%29.png)

Set the following Repository permissions:

| Permission      | Access       |
| --------------- | ------------ |
| Checks          | Read & write |
| Contents        | Read-only    |
| Deployments     | Read & write |
| Metadata        | Read-only    |
| Pull requests   | Read & write |
| Webhooks        | Read & write |
| Commit statuses | Read & write |

Set the following Organization permissions:

| Permission | Access    |
| ---------- | --------- |
| Members    | Read-only |

Subscribe to the following events:

* Organization
* Pull request
* Push
* Repository

Finally, choose whether you want to allow the App to be installed on any account or only on the account it is being created in and click on _Create GitHub App:_

![](/assets/images/image%20%2855%29.png)

Once your App has been created, make a note of the _App ID_ in the _About_ section:

![](/assets/images/image%20%2856%29.png)

Now scroll down to the _Private keys_ section __ of the page and click on _Generate a private key:_

![](/assets/images/image%20%2857%29.png)

This will download a file onto your machine containing the private key for your GitHub app. The file will be named `<app-name>.<date>.private-key.pem`, for example `spacelift.2021-05-11.private-key.pem`.

Now that your GitHub App has been created, go back to the integration configuration screen in Spacelift, and enter your _API host URL_ (the URL to your GitHub Enterprise server), the _App ID_, and paste the contents of your private key file into the Private key box:

![](/assets/images/image%20%2898%29.png)

Click on the Save button to save your integration settings.

### Installing your GitHub App

Now that you've created a GitHub App and configured it in Spacelift, the last step is to install your App in one or more accounts in your GitHub Enterprise server. To do this, go back to GitHub Enterprise, find your App in the GitHub Apps page in your account settings, and click on the _Edit_ button next to it:

![](/assets/images/image%20%2858%29.png)

Go to the _Install App_ section, and click on the _Install_ button next to the account your want Spacelift to access:

![](/assets/images/image%20%2859%29.png)

Choose whether you want to allow Spacelift access to all the repositories in the account, or only certain ones:

![](/assets/images/image%20%2860%29.png)

Congrats, you've just linked your GitHub Enterprise account to Spacelift!

## Using GitHub Enterprise with stacks and modules

If your Spacelift account is integrated with GitHub Enterprise, the stack or module creation and editing forms will show a dropdown from which you can choose the VCS provider to use. GitHub Enterprise will always come first, assuming that you've integrated it with Spacelift for a good reason:

![](/assets/images/image%20%2861%29.png)

The rest of the process is exactly the same as with [creating a GitHub-backed stack](../../concepts/stack/creating-a-stack.md#integrate-vcs) or module, so we won't go into further details.

## Unlinking the Integration

If you no-longer need the integration, you can remove it via the _Unlink_ button on the VCS Providers page:

![](/assets/images/image%20%2899%29.png)

Please note that unlinking the integration in Spacelift will not remove the GitHub App or its permissions from the Enterprise Server. You will need to do that yourself.
