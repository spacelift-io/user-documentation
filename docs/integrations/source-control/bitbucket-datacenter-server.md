# Bitbucket Datacenter/Server

In addition to our out-of-the-box [integration with GitHub](github.md), Spacelift supports using an on-premises Bitbucket installation as the source of code for your [stacks](../../concepts/stack/) and [modules](../../vendors/terraform/module-registry.md).

## Setting up the integration

In order to set up the integration from the Spacelift side, please navigate to the _VCS Providers_ section of the admin Settings page and click the _Set up_ button next to the Bitbucket Data Center integration:

![](/assets/images/image%20%28100%29.png)

This should open a form like this one:

![](/assets/images/image%20%28101%29.png)

Now you'll have to fill in the API host URL, which is the URL on which Spacelift will access the Bitbucket server. This may be a URL which uses [VCS Agent Pools](../../concepts/vcs-agent-pools.md), or a normal URL, if your Bitbucket instance is publicly available.

The user facing host URL is the address on which users of you Bitbucket instance access it. This could be an internal address inside of your company network, but could also by a public address if your Bitbucket instance is publicly available.

In order to get the access token you'll need to go on your Bitbucket instance into **Manage account -> Personal access tokens -> create**. There, you will need to give your new access token a name and give it write access to repositories:

![Personal token creation](/assets/images/image%20%2865%29.png)

This will give you an access token which you can put into the **Access token** field in the integration configuration.\


![Created personal token](/assets/images/image%20%2866%29.png)

After doing all this you should have all fields filled in.

![](/assets/images/image%20%28102%29.png)

After saving, you'll receive your webhook secret and endpoint:

![](/assets/images/image%20%28103%29.png)

For each repository you want to use with Spacelift, you need to go into its **Repository settings -> Webhooks -> Create webhook**, and configure the webhooks accordingly, by activating Push and Pull Request Opened events.

![Configuring Webhooks](/assets/images/Screenshot%202022-02-04%20at%2012.02.27.png)

When creating a Stack, you will now be able to choose the Bitbucket Datacenter provider and a repository inside of it:

![Creating a Stack with the Bitbucket Datacenter integration](/assets/images/image%20%2872%29.png)
