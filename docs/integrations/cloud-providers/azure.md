# Azure

## About the integration

Spacelift provides support for managing Azure resources via the Terraform [Azure Provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs). The documentation for the Azure Provider outlines the different authentication methods it supports, and it should always be considered the ultimate source of truth.

This page explains how to configure the following authentication methods in Spacelift:

* [Spacelift Managed Integration](azure.md#spacelift-managed-integration) - the simplest way to get up and running. Handles automatic secret creation and rotation, but is only supported on public workers.
* [Static Credentials](azure.md#static-credentials) - useful when using the public worker pool, or workers that are not hosted in Azure. Simple to setup, but requires you to manually manage secret rotation.
* [Managed Service Identities](azure.md#managed-service-identities) - ideal when using [private workers](../../concepts/worker-pools.md) hosted in Azure. Requires managing your own workers, but secret rotation is handled automatically by Azure.

!!! Info
This guide explains how to configure the Azure provider using environment variables. Although you can add these environment variables directly to individual stacks, it may be worth creating a [Spacelift Context](../../concepts/configuration/context.md) to store your Azure credentials. This allows you to easily add the same credentials to any stack that requires them.


## Spacelift Managed Integration

The Spacelift managed integration is great for situations where you want to get up and running quickly, and where you want the reassurance that the credentials for accessing your Azure account will be automatically rotated and stored securely. If you are not comfortable with Spacelift managing your Azure credentials, we would suggest that you use a private worker configured with a [Managed Identity](azure.md#managed-identities) for the most control and security.

### Credential storage and rotation

When an Azure integration is created, an associated Azure AD Application is created within Azure. We automatically create a client secret for that application, and rotate it roughly once every 24 hours. The secret is stored securely, encrypted using AWS [Key Management Service](https://aws.amazon.com/kms/).

### Creating an integration

To add a new integration, go to the _Azure_ page under your account settings_._ When you go there for the first time, the page will be empty, but will prompt you to add an integration:

![](https://lh5.googleusercontent.com/Twj5iwxAe9OdTL3zofwjh7DIutsg8NKJub0Y6zvNwmdDwqngYALmWHSSszTOaYfarVBdxmS7EzkbwuJIKbdbwb86\_SF2cz\_l9h5vgwY8-8g-OLAliM0S7OwqXNMai6loPz2XoQXF=s0)

Click on the _Add Integration_ button to start configuring your integration:



![](https://lh3.googleusercontent.com/eRpQfxiWazqKWfnHTmLYcIYL1hvcm4R\_Wi3tqaEVZw0WfpFJWQqYo7OoqDhpZppamrWjZBpl41i1ZtftBxcoYN1YSvok9p7gtpOFQhnPau9HousE4tghTDPQWZXQ7NXn0ADAzq21=s0)

Give **** your integration a name, and enter your Active Directory Tenant ID. You can also enter a default subscription ID at this point. You can specify the default subscription ID if you want to attach your integration to multiple stacks that are all going to use the same Azure subscription.

!!! Info
You can find your Tenant ID by going to the [Azure Active Directory](https://portal.azure.com/#blade/Microsoft\_AAD\_IAM/ActiveDirectoryMenuBlade/Overview) section of the Azure portal. You can also find your Azure subscriptions by going to the [Subscriptions](https://portal.azure.com/#blade/Microsoft\_Azure\_Billing/SubscriptionsBlade) section of the Azure portal.


### Providing admin consent

Once your integration has been created successfully, you will be taken to the integration details. It should look something like this:

![](https://lh5.googleusercontent.com/\_WAQuO6SvW0fNVQ2IeFu46K4DLluDbuG96v1SjMKbw1Y\_c0xWfa0CynIO5UHdNgiWiFc1qchVympyMuU9-0PtBN2nqhaV6JDCvev2KE4aLOo\_R1Yf8s7q-zEBRFdeFJOlpybv9IY=s0)

####

To install the Azure AD application for your Spacelift integration into your Azure account, click on the _Provide Consent_ button, which will redirect you to Azure. After logging into your Azure account, you should see a permissions screen like the following:



![](https://lh6.googleusercontent.com/sEumQpyMVV6BSJJZbdNlZbKRJskpskk7zRebcK6V9HU3NoR-04TYMllNiDqzUcnDzzn6JQNT1UWtyPoetRSmYUUX\_GLex9M65lgrJRMmFNtWYk3OSyrVZGCqw5gqHijmzqmYPb7F=s0)

Click on the Accept button to complete the admin consent process, at which point you should be redirected to your integration settings.

!!! Info
The admin consent process requires at least one permission to be requested in order to work. Although the application requests the “Sign in and read user profile” permission, it never signs in as any users in your account or accesses their information.


!!! Warning
Azure AD uses eventual consistency to replicate new Azure applications globally. Because of this you might see the following error message if you try to grant admin consent very quickly after the integration was created:

![](https://lh4.googleusercontent.com/lMmG294KwgxorLySgfwTJTV1NCD\_AmzogTK\_akgb-X6OhzZuw3s9xEZ9xlJujx4SSuRwdaVmICLwP73TaOz5okC9wgO7Z6aePq4FT8-qs9YMnj9jgNbVZg\_H41DLG8LPHxbxgJFB=s0)

This isn’t a problem. Just wait a few minutes and try again.


### Configuring Azure permissions

Now that you have granted admin consent, a new Enterprise Application will be created for your integration in Azure. You can view this in the [Enterprise Applications](https://portal.azure.com/#blade/Microsoft\_AAD\_IAM/StartboardApplicationsMenuBlade/AllApps/menuId/) section of Azure Active Directory:

![](https://lh4.googleusercontent.com/Gfv5uKYvNuVQ9\_CgZXO\_aYA8m52m9zQ\_aw3vG6BEDOVYNrXTczR6BkPBpYIU8JcpRuY8keionc4zIV-d99Ogkfar28CU6wyIOQ3kjSDBSLoURQsRVto0nwxBmbdbHW9SP9ygoFf1=s0)

If you go to the Access Control (IAM) section of the Azure subscription or resource group you want the integration to have access to, you should be able to add a new role assignment for the integration:

![](https://lh6.googleusercontent.com/epsMyvwvup1nlfsiYj8AVjBo58W82eg3KkbgC6n8Ebf3lHElT4MDa3dB\_OiiOs2gYX\_8s8zI5aHUMkzeQpT-VkhSzs5yY\_rC92hd4Z0xCoaawCAiLVLzlf3be3NgdVtdFjwPWNQp=s0)

!!! Info
The integration has no access to any of your Azure infrastructure unless you explicitly grant it the appropriate permissions.


### Attaching to a stack

To attach an integration to a Stack, edit the _Integrations_ settings for your stack, and choose the Azure option from the list:

![](https://lh4.googleusercontent.com/y5JlOLbGNy3CHq31t-WD7R7-FEHfdoKlVTBkAGVO68JKBWzBuUQ5gU8CVMfJYftu-S7lGuA\_GMPMv41waSzVQoPr1-kjBaC93ABw0SociL2TzVcLHekiPusoiITRRguOsFgqv2K5=s0)

Choose the integration you want to attach, specify a subscription ID if the integration you’ve chosen doesn’t have a default or you want to override the default, and specify whether the integration should be used for read, write or read and write operations:

![](https://lh6.googleusercontent.com/UoPoD0kQNWM4ft2POzbgfQyyussD0eqQUI35ARkW0mBbcI06bKaaVTPvbGvEJwmcKRYenb\_0\_r\_cIu-52gOE7mRmckixzO7ShHWADDEJyH9gMo-yPWrMsv-1izaL5ANbt-SyZWZo=s0)

Click on the Attach button to add the integration to your stack.

### Detaching from a stack

If you want to detach an integration from a stack, just click the Detach button next to the integration:

![](https://lh6.googleusercontent.com/9tKS3lPLHCga2CeguEi\_6JFnaPBEnb-xj4Lem5r3P1Xx0KxSJGyH\_hECzl3\_4XWQl8E5rAI7fqYlUuFFjo4MNAoj775y3TRB1-Dbirn2UKyB2d4fuP\_Ln6LT2PIuP5pBRhHlLmSs=s0)

### Deleting an integration

You can delete an Azure integration if you don’t need it anymore. To do that, go to the Azure Integrations settings screen, and click the Delete button next to the integration you want to remove:

![](https://lh4.googleusercontent.com/DAbsLUKrZJfbbltKK52CIMtJ9\_GilBjAMxIp9spuKz6b6H0Gwhr-Q63rQxFiPvoCqToNcwaIDKty1CmkRBezI2e2mkri27QkY9PbL135YxQznBS6Ur\_iQiOJEMSoMxoXkyAMRsjH=s0)

!!! Info
You can only delete an integration if it is not being used by any stacks, so you may have to detach the integration from any stacks it is attached to first.


#### Deleting the Enterprise Application

Deleting the integration does not remove the Enterprise Application that was added to your Azure AD account via the admin consent process. You need to do that yourself manually after deleting the integration.

## Static credentials

To use static credentials, you need to create an Azure Service Principal, grant it access to your Azure subscription, and then configure the Azure Provider to use the Service Principal via environment variables.

If you already understand how to create and manage Service Principals, feel free to skip to the [configuring via environment](azure.md#configuring-via-environment) section.

### Create a service principal

Create a Service Principal using the following command, substituting`<subscription-id>` with your own subscription ID:

```
az ad sp create-for-rbac --name spacelift-sp --role="Contributor" --scopes="/subscriptions/<subscription-id>"
```

This will output something like the following:

```
Changing "spacelift-sp" to a valid URI of "http://spacelift-sp", which is the required format used for service principal names
Creating 'Contributor' role assignment under scope '/subscriptions/458fd769-5a4c-4df2-a339-8981094d8899'
The output includes credentials that you must protect. Be sure that you do not include these credentials in your code or check the credentials into your source control. For more information, see https://aka.ms/azadsp-cli
{
  "appId": "5ffa3670-74db-4a9d-b213-179d2d315888",
  "displayName": "spacelift-sp",
  "name": "http://spacelift-sp",
  "password": "A4xFo3z-Hv9BMOFlmHfXP2ESXugHMdaike",
  "tenant": "d3fe1fdc-160d-4f06-a5c0-f1485b1b0366"
}
```

The command creates a new Service Principal called `spacelift-sp`, and grants it the _Contributor_ role on your subscription. It also outputs the `appId`, `password` and `tenant` for the Service Principal. Make a note of these because you'll need them later.

!!! Info
If you would rather assign permissions separately, you can run the following command to create a Service Principal with no role assignments:

```
az ad sp create-for-rbac --name spacelift-sp --skip-assignment
```


### Configuring via environment

Azure provides two options for authenticating Service Principals:

* Client secrets - a randomly generated string.
* Client certificates - an x509 certificate.

Either option can be used depending on your requirements, and the configuration required for both is very similar.

#### Authenticating with a client secret

To configure the Azure provider using a client secret, add the following [environment variables](../../concepts/configuration/environment.md#environment-variables) to your stack:

* `ARM_CLIENT_ID` - the `appId` returned when you created your Service Principal. This is known as the _Application ID_ or _Client ID_ within Azure.
* `ARM_CLIENT_SECRET` - the `password` returned when you created your Service Principal.
* `ARM_SUBSCRIPTION_ID` - your subscription ID.
* `ARM_TENANT_ID` - the `tenant` returned when you created your Service Principal.

Once finished, your environment should look something like this:

![](/assets/images/image%20%2883%29.png)

#### Authenticating with a client certificate

To configure the Azure provider using a client certificate, first add your PFX as a [mounted file](../../concepts/configuration/environment.md#mounted-files) to your environment:

![](/assets/images/image%20%2884%29.png)

!!! Warning
You should treat this certificate like any other credential, and mark it as a _secret._


Next, add the following [environment variables](../../concepts/configuration/environment.md#environment-variables) to your stack:

* `ARM_CLIENT_ID` - the `appId` returned when you created your Service Principal. This is known as the _Application ID_ or _Client ID_ within Azure.
* `ARM_CLIENT_CERTIFICATE_PATH` - the path to the certificate you uploaded in the previous step.
* `ARM_CLIENT_CERTIFICATE_PASSWORD` - the password for your certificate.
* `ARM_SUBSCRIPTION_ID` - your subscription ID.
* `ARM_TENANT_ID` - the `tenant` returned when you created your Service Principal.

Once finished, your environment should look something like this:

![](/assets/images/image%20%2885%29.png)

### Credential expiry and rotation

When using static credentials, you are in charge of managing credential rotation. When using the `az ad sp create-for-rbac` command, the client secret returned by the command will expire in 1 year. At that point, any stacks using that client secret will stop working until a new one is added and the Spacelift environment updated.

## Managed identities

Azure [Managed Identities](https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/) allow you to assign an identity to an Azure virtual machine, and then use that identity for role assignment. This means that you can grant your Spacelift private workers permission to manage your Azure resources,without having to store any credentials in Spacelift, or deal with credential rotation.

To use a managed identity, you need to take the following steps:

* Follow the [instructions](../../concepts/worker-pools.md) to setup a private worker pool.
* Create an Azure VM with a managed identity, and install the worker binary on it.
* Configure the [Azure provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/guides/managed\_service\_identity#configuring-terraform-to-use-a-managed-identity) to use the managed identity for authentication.

To configure the Azure provider to use the managed identity, add the following environment variables to your stack:

* `ARM_USE_MSI` - set to `true` to indicate you want to use a managed identity.
* `ARM_SUBSCRIPTION_ID` - your subscription ID.
* `ARM_TENANT_ID` - your Azure AD tenant.

In addition, if using a user-assigned identity, add the following variable to your stack:

* `ARM_CLIENT_ID` - the client ID of your user-assigned identity.

Once finished, your environment should look something like this:

![](/assets/images/image%20%2886%29.png)
