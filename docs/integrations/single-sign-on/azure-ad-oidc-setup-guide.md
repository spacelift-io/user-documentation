---
description: >-
  Example instructions for setting up Azure AD as a Single Sign-On source via
  OIDC.
---

# Azure AD OIDC Setup Guide

If you'd like to set up the ability to sign in to your Spacelift account using an OIDC integration with Azure AD, you've come to the right place. This example will walk you through the steps to get this setup, and you'll have Single Sign-On running in no time!

!!! warning
    Before setting up SSO, it's recommended to create backup credentials for your Spacelift account for use in case of SSO misconfiguration, or for other break-glass procedures. You can find more about this in the [Backup Credentials](./backup-credentials.md) section.

!!! warning
    Due to a limitation in Azure AD, when you map the teams to spacelift it will only map the IDs of the teams. A workaround would be to rewrite the teams in the [login policy](../../concepts/policy/login-policy.md#rewriting-teams).

!!! warning
    Due to an Azure AD limitation, if a user is attached to more than 150 groups, this causes Microsoft Entra ID to not send any of the user's group claims.

## Pre-requisites

- Spacelift account, with access to admin permissions
- Azure account, with an existing Azure Active Directory
- You'll need permissions to create an **App Registration** within your Azure AD

!!! info
    Please note you'll need to be an admin on the Spacelift account to access the account settings to configure Single Sign-On.

## Configure Account Settings

You'll need to visit the Spacelift account settings page to set up this integration, from the navigation side bar menu, select "Settings."

![](../../assets/screenshots/Screen Shot 2022-07-01 at 4.12.30 PM (1).png)

## Setup OIDC

Next, you'll want to click the Set Up box underneath the "OIDC Settings" section. This will expand some configuration we will need to fill out in a few minutes, which we will be obtaining from Azure. For now, **copy the authorized redirect URL** as we will need to provide Azure this URL when configuring our Azure App Registration within your Azure AD.

![](../../assets/screenshots/Screen Shot 2022-07-01 at 4.16.00 PM.png)

## Azure Portal: Navigate to Azure Active Directory

Within your Azure Account, navigate to your Azure Active Directory where you'd like to setup the OIDC integration for. In this guide, we are using a Default Directory for example purposes.

![Navigate to your Azure Active Directory.](../../assets/screenshots/1-azure-navigate-to-azure-ad.png)

## Azure AD: Create an App Registration

While you are within your Active Directory's settings, click on **App registrations** from the navigation, and then select **New registration**.

![Click on App Registrations, then click New Registration.](../../assets/screenshots/2-azure-ad-new-registration.png)

## Azure AD: App Registration Configuration

Give your application a name - Spacelift sounds like a good one.

Configure your supported account types as per your login requirements. In this example, we are allowing Accounts in this organizational directory access to Spacelift.

Remember the **authorized redirect URL** we copied earlier from Spacelift? We'll need that in this step. You'll want to paste that URL into the **Redirect URI** input as shown. Make sure you select **Web** for the type.

Click **Register**.

![Give your App Registration a name. Configure the redirect URI.](../../assets/screenshots/3-azure-create-app-integration-step-1.png)

## Azure AD: Add UPN Claim

Start by navigating to the **Token configuration** section of your application.

![](<../../assets/screenshots/image (116).png>)

Click the **Add optional claim** button, choose the **ID** token type, and select the **upn** claim:

![](<../../assets/screenshots/image (118) (1).png>)

Click the **Add** button, making sure to enable the **Turn on the Microsoft Graph profile permission** checkbox on the popup that appears:

![](<../../assets/screenshots/image (113).png>)

## Azure AD: Configure App Credentials

Navigate to the **Certificates & secrets** section of your application.

![Navigate to Credentials & secrets.](../../assets/screenshots/3-azure-navigate-to-credentials.png)

Click the **New client secret** button.

![Click New client secret.](../../assets/screenshots/4-azure-new-client-secret.png)

Give your secret a description and an expiration:

![Define client secret Description and Expires duration.](../../assets/screenshots/5-azure-new-secret.png)

!!! info
    In this example, we are using 6 months for **Expires.** This means you will need to generate a new client secret in 6 months for your OIDC integration.

Click **Add.**

Now that your secret has been created, copy its **Value**:

![Copy the Value to your Spacelift OIDC settings as the "Secret".](<../../assets/screenshots/Screen Shot 2022-04-14 at 11.03.31 AM.png>)

Take this secret value that you have just copied and paste this into our Spacelift OIDC settings within the **Secret** input:

![Enter secret into Spacelift OIDC settings](../../assets/screenshots/azure-ad-oidc-enter-secret.png)

!!! info
    Don't click Save in Spacelift just yet, we still need to get the Client ID and Provider URL for your application.

## Azure AD: Client ID and Provider URL

To complete your configuration, you need two more pieces of information:

- The Client ID.
- The Provider URL.

You can get both of these pieces of information from the **Overview** section of your Azure AD application. The **Application (client) ID** field should be used as the Client ID, and the Provider URL can be found in the **OpenID Connect metadata document** field after clicking on the **Endpoints** button:

![Azure AD App overview](../../assets/screenshots/azure-ad-oidc-app-overview.png)

In summary, here are the values that should be copied over to Spacelift:

- Application (client) ID within Azure AD => Client ID on Spacelift
- Secret Value you generated => Secret input on Spacelift
- OpenID Connect metadata document URL => Provider URL on Spacelift

Click **Save.**

## Azure AD OIDC Setup Completed

That's it! Your OIDC integration with Azure AD should now be configured (as per this example). Feel free to make any changes to your liking within your Azure AD App Registration configuration for the app that you just created.
