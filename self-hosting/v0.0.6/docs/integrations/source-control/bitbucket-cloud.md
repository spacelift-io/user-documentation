# Bitbucket Cloud

 Spacelift supports using Bitbucket Cloud as the source of code for your [stacks](../../concepts/stack/README.md) and [modules](../../vendors/terraform/module-registry.md).

## Setting up the integration

In order to set up the integration from the Spacelift side, please navigate to the VCS providers section of the admin Settings page, find the Bitbucket Cloud integration and click the _Set up_ button:

![VCS providers page](<../../assets/screenshots/Screenshot from 2021-06-10 16-05-39.png>)

This should open a form like this one:

![Bitbucket Cloud setup form](<../../assets/screenshots/Screenshot from 2021-06-10 16-09-36.png>)

Now you'll have to fill in the Username, which is a username of your Bitbucket Cloud account.

In order to get the [App password](https://support.atlassian.com/bitbucket-cloud/docs/app-passwords/){: rel="nofollow"} you'll need to go to the Bitbucket Cloud site and navigate to **Personal settings** -> **App passwords** (it's under Access management) -> **Create app password**. There, you will need to give your new app password a label and give it read access to repositories and pull requests:

![App password creation](<../../assets/screenshots/Screenshot from 2021-06-10 16-16-53.png>)

This will give you an app password token which you can put into the **App Password** field in the integration configuration.

![Created new app password](<../../assets/screenshots/Screenshot from 2021-06-10 16-39-03.png>)

After doing all this you should have all fields filled in.

![Filled in Bitbucket Cloud integration form](<../../assets/screenshots/Screenshot from 2021-06-11 10-50-38.png>)

After saving, you'll receive your webhook endpoint:

![Configured integration](<../../assets/screenshots/Screenshot from 2021-06-11 14-52-40.png>)

For each repository you want to use with Spacelift, you now have to go into its **Repository settings -> Webhooks -> Add webhook**, and configure the webhook accordingly, by activating the following events:

- Repository > Push
- Pull Request > Created
- Pull Request > Updated
- Pull Request > Approved
- Pull Request > Approval removed
- Pull Request > Merged
- Pull Request > Comment created

It should look something like the following:

![Webhooks configuration](<../../assets/screenshots/bitbucket-cloud-webhook-settings.png>)

The last step is to install the **Pull Request Commit Links** app to be able to use [this](https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/commit/%7Bcommit%7D/pullrequests){: rel="nofollow"} API. This is done automatically when you go to the commit's details and then click "Pull requests" link.

![Commit's details](<../../assets/screenshots/Screenshot from 2021-06-15 11-19-56.png>)

When creating a Stack, you will now be able to choose the Bitbucket Cloud provider and a repository inside of it:

![Stack creation form](<../../assets/screenshots/Screenshot from 2021-06-11 15-03-21.png>)

## Unlinking the Integration

If you no-longer need the integration, you can remove it via the _Unlink_ button on the VCS settings page.

![VCS providers page](<../../assets/screenshots/Screenshot from 2021-06-14 08-53-09.png>)

Please also remember to remove any Spacelift webhooks from your repositories.
