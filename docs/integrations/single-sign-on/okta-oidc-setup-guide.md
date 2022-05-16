---
description: Example instructions for setting up Okta as a single sign-on source via OIDC.
---

# Okta OIDC Setup Guide

If you'd like to set up the ability to sign in to your Spacelift account using an OIDC integration with Okta, you've come to the right place. This example will walk you through the steps to get this setup, and you'll have single sign-on running in no time!

### Pre-requisites

* Spacelift account, with access to admin permissions
* Okta account, with permission to create Okta App Integrations

### Configure Account Settings

You'll need to visit the Spacelift account settings page to set up this integration, from the account menu, select "Settings."

![Click on Settings](../../assets/screenshots/account-settings.png)

### Setup OIDC

Next, you'll want to click the Set Up box underneath the "OIDC Settings" section. This will expand some configuration we will need to fill out in a few minutes, which we will be obtaining from Okta. For now **copy the authorized redirect URL** as we will need to provide Okta this URL when configuring our Okta App Integration.

![Click on Set Up](../../assets/screenshots/1-setup-oidc.png)

### Okta: Select Applications

In a new browser tab, open your Okta account. Select the Applications link from the navigation.

![Select Applications](../../assets/screenshots/2-select-okta-applications.png)

### Okta: Create App Integration

Click the "Create App Integration" button. For the sign in type, ensure you select **OIDC** - for the application type, select **Web Application.**

![Click Create App Integration](../../assets/screenshots/3-create-app-integration.png)

![Select OIDC and Web Application, Click Next](../../assets/screenshots/4-create-app-integration-modal.png)

### Okta: Configure App Integration

Give your app integration a name - Spacelift sounds like a good one :clap:

Remember the **authorized redirect URL** we copied earlier from Spacelift? We'll need that in this step. You'll want to paste that URL into the **Sign-in redirect URIs** input as shown.

As far as the assignments for this app integration, that's up to you at the end of the day. This determines what users from your Okta account will be able to access Spacelift. Click **Save**.

![Configure Okta App Integration](../../assets/screenshots/5-configure-app-integration.png)

### Okta: Configure Group Claim

Click on the **Sign On** tab within your newly created Okta App Integration,&#x20;

You'll need to edit the groups claim type to return groups you consider useful in Spacelift Login Policies. For testing purposes, you could set it to **Matches regex** with .\* for the regex value.

![](../../assets/screenshots/8-okta-group-claims.png)

### Configure OIDC Settings

Switch back to the **General** tab. Now that we have the Okta App Integration setup, we'll need to take the **Client ID**, **Client Secret**, and **Okta domain**, to configure the Spacelift OIDC Settings.&#x20;

!!! info
    The Okta Domain will be set as the "Provider URL" in your Spacelift OIDC settings. **Ensure that you prefix this URL with https://**

![Copy the 3 Values back to Spacelift](../../assets/screenshots/6-configure-spacelift-oidc-settings.png)

![Copy/Paste the values into your Spacelift OIDC Settings, Click Save](../../assets/screenshots/7-configure-spacelift-oidc-settings-part-2.png)

### Okta OIDC Setup Completed

That's it! Your OIDC integration with Okta should now be fully configured. Feel free to make any changes to your liking within your Okta App Integration configuration for the app that you just created.

