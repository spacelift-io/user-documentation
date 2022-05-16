---
description: >-
  Describes various approaches you can use to configure external identity
  providers to log in to your Spacelift account.
---

# Single sign-on

By default, Spacelift supports logging in using GitHub, GitLab, or Google. Some organizations however prefer a single sign-on approach, where access to resources is centralized. To accommodate this use-case, Spacelift supports single sign-on using [SAML 2.0](single-sign-on.md#setting-up-saml) or [OIDC](single-sign-on.md#setting-up-oidc).

## Managing integrations

In order to manage single sign-on integrations on your Spacelift account, please go to the _Settings_ section of your account view. Next, navigate to the _Single sign-on_ tab_._ If SSO is not enabled for your account, all you're going to see is instructions on how to get started. The first steps are always taken in your identity provider (GSuite, Okta, Auth0, ActiveDirectory, etc.). Navigate to your identity provider and create a dedicated SSO application filled with appropriate URLs taken from the Spacelift settings page presented below.

![These URLs will be different for your account](../.gitbook/assets/sso\_settings.png)



## Setting up SAML

When setting up Spacelift on your identity provider, you may want to add three attribute mappings:

* `FirstName` is used to build human-friendly user name;
* `LastName` is used to build human-friendly user name;
* `Teams` can be used by [login](../concepts/policy/login-policy.md) and [stack access](../concepts/policy/stack-access-policy.md) policies to determine the level access to the Spacelift account and/or individual Stacks;

Depending on your identity provider and your use case, your mapping may be different. Especially with regards to `Teams`, some identity providers (eg. [Okta](https://www.okta.com/)) will support an arbitrary list of memberships similar to GitHub teams out of the box, some will need extra customizations like (eg. [GSuite](https://support.google.com/a/answer/6327792?hl=en) and as a courtesy, we will flush your login history.

Some identity providers (eg. [Okta](https://www.okta.com/)) will allow you to provide a custom per-user SAML 2.0 _Subject_ for SAML assertions. You could use this feature to map GitHub usernames to your identity provider users and thus get the exact same experience as when using GitHub as your identity provider.

{% hint style="warning" %}
When setting up SSO without this GitHub mapping, your future logins will appear as new users since Spacelift has no way of mapping those without your assistance. New users will count against your seat quota and you may run out of seats. If you run into this problem, you can [contact us](https://spacelift.io/contact).&#x20;
{% endhint %}

### NameID format

The NameID format specifies the format that Spacelift requests user identifiers from your identity provider. The user identifier is used as the Spacelift login, and each unique identifier will count against your seat quota. Some identity providers allow you to configure this format, but certain providers (eg. Azure AD) do not.

If your identity provider does not allow the NameID format to be configured at their end, you can choose from one of the following options:

* Transient - an opaque identifier that is not guaranteed to remain the same between logins.
* Email Address - an email address.
* Persistent - an opaque identifier that remains the same between logins.

## Setting up OIDC

When setting up Spacelift on your identity provider, you must make sure it supports the `email` scope and returns the corresponding `email`

### Additional claims

Spacelift dynamically checks integrated Identity Provider's Well-Known OpenID configuration for a list of supported scopes and, optionally, asks for `profile` and `groups` scopes if those are available.&#x20;

{% hint style="warning" %}
In order to populate the `input.session.teams` value in the Login Policies Spacelift tries to fetch the `groups` claim. For many Identity Providers, this claim has to be manually set and configured. Bear in mind that some providers such as GSuite do not support retrieving groups of given users.
{% endhint %}

### OIDC Setup Guide Examples:

The following are links to example implementations you can use as a reference/guide for setting up your own OIDC integration.

* [GitLab](single-sign-on/gitlab-oidc-setup-guide.md)
* [Okta](single-sign-on/okta-oidc-setup-guide.md)
* [OneLogin](single-sign-on/onelogin-oidc-setup-guide.md)
* [Azure AD](single-sign-on/azure-ad-oidc-setup-guide.md)
* If you can't find your OIDC provider in the list above, don't worry - we do support all OIDC providers as long as they support the email scope and return the user's email. Fortunately, most OIDC providers do :sunglasses:

## IdP-initiated SSO

While certainly more convenient, IdP-initiated SSO lacks some of the protections awarded by SP-initiated SSO and is thus inherently less safe. Since Spacelift manages some of your most valuable resources, we decided against supporting this feature.

If our server detects an IdP-initiated SSO session, it simply redirects the browser using [_303 See other_](https://en.wikipedia.org/wiki/HTTP\_303) HTTP status code to the endpoint that triggers a regular SP-initiated SSO flow. As a result, you can still access Spacelift by clicking on the link in your IdP catalog, but are not exposed to the vulnerabilities of the IdP-initiated SSO.

## Disabling SSO

In order to disable SSO integration for your Spacelift account, or change the IdP provider, please click the _Disable_ button to delete the integration. This change takes effect immediately for new logins, and will invalidate existing sessions. New sessions will be created using the new SSO identity provider or - if none is set up - Spacelift will utilize the default identity provider that was used to create the account originally.

{% hint style="warning" %}
Again, please note that new usernames will occupy new seats, even if they're the same users registered with a different identity provider.
{% endhint %}

![](../.gitbook/assets/disable-oidc.png)
