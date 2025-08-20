# Microsoft Azure

## About the integration

Spacelift provides support for managing Azure resources via the Terraform [Azure Provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs){: rel="nofollow"}. The documentation for the Azure Provider outlines the different authentication methods it supports, and it should always be considered the ultimate source of truth.

This page explains how to configure the following authentication methods in Spacelift:

- [Spacelift-managed integration](azure.md#spacelift-managed-integration): The simplest way to get your cloud integration up and running. Handles automatic secret creation and rotation.
- [Static credentials](azure.md#static-credentials): Useful when using the [public worker pool](../../concepts/worker-pools/README.md#public-worker-pool), or workers that are not hosted in Azure. Simple to setup, but requires you to manually manage secret rotation.
- [Managed service identities](azure.md#managed-identities): Ideal when using [private workers](../../concepts/worker-pools) hosted in Azure. Requires managing your own workers, but secret rotation is handled automatically by Azure.

!!! tip
    This guide explains how to configure the Azure provider using environment variables. Although you can add these environment variables directly to individual stacks, it may be worth creating a [Spacelift context](../../concepts/configuration/context.md) to store your Azure credentials. This allows you to easily add the same credentials to any stack that requires them.

## Spacelift-managed integration

See [Integrate Spacelift with Microsoft Azure](../../getting-started/integrate-cloud/Azure.md) to configure the integration through the Spacelift UI, provide admin consent, and set up proper permissions in Azure.

## Static credentials

To use static credentials, you need to create an Azure service principal, grant it access to your Azure subscription, and then configure the Azure Provider to use the service principal via environment variables.

If you already know how to create and manage service principals, feel free to skip to the [configure via environment](azure.md#configure-via-environment) section.

### Create a service principal

Create a service principal using this command, substituting `<subscription-id>` with your own subscription ID:

```bash
az ad sp create-for-rbac --name spacelift-sp --role="Contributor" --scopes="/subscriptions/<subscription-id>"
```

This will output something like:

```bash
Changing "spacelift-sp" to a valid URI of "http://spacelift-sp", which is the required format used for service principal names
Creating 'Contributor' role assignment under scope '/subscriptions/458fd769-5a4c-4df2-a339-8981094d8899'
The output includes credentials that you must protect. Be sure that you do not include these credentials in your code or check the credentials into your source control. For more information, see Create an Azure service principal with the Azure CLI.
{
  "appId": "5ffa3670-74db-4a9d-b213-179d2d315888",
  "displayName": "spacelift-sp",
  "name": "http://spacelift-sp",
  "password": "A4xFo3z-Hv9BMOFlmHfXP2ESXugHMdaike",
  "tenant": "d3fe1fdc-160d-4f06-a5c0-f1485b1b0366"
}
```

The command creates a new service principal called `spacelift-sp`, and grants it the _Contributor_ role on your subscription. It also outputs the `appId`, `password` and `tenant` for the service principal. Make a note of these because you'll need them later.

!!! info
    If you would rather assign permissions separately, you can run the following command to create a Service Principal with no role assignments:

    ```bash
    az ad sp create-for-rbac --name spacelift-sp --skip-assignment
    ```

### Configure via environment

Azure provides two options for authenticating service principals:

- **Client secrets**: A randomly generated string.
- **Client certificates**: An x509 certificate.

Either option can be used depending on your requirements, and the configuration required for both is very similar.

#### Authenticating with a client secret

To configure the Azure provider using a client secret, add the following [environment variables](../../concepts/configuration/environment.md#environment-variables) to your Spacelift stack:

- `ARM_CLIENT_ID`: The `appId` returned when you created your service principal. This is known as the _Application ID_ or _Client ID_ within Azure.
- `ARM_CLIENT_SECRET`: The `password` returned when you created your service principal.
- `ARM_SUBSCRIPTION_ID`: Your subscription ID.
- `ARM_TENANT_ID`: The `tenant` returned when you created your service principal.

Once finished, your environment should look something like this:

![Configured Azure environment with secret authentication](<../../assets/screenshots/image (83).png>)

#### Authenticating with a client certificate

To configure the Azure provider using a client certificate, first add your PFX as a [mounted file](../../concepts/configuration/environment.md#mounted-files) to your environment:

![Mounted file](<../../assets/screenshots/image (84).png>)

!!! warning
    You should treat this certificate like any other credential, and mark it as a _secret._

Next, add the following [environment variables](../../concepts/configuration/environment.md#environment-variables) to your Spacelift stack:

- `ARM_CLIENT_ID`: The `appId` returned when you created your service principal. This is known as the _Application ID_ or _Client ID_ within Azure.
- `ARM_CLIENT_CERTIFICATE_PATH`: The path to the certificate you uploaded in the previous step.
- `ARM_CLIENT_CERTIFICATE_PASSWORD`: The password for your certificate.
- `ARM_SUBSCRIPTION_ID`: Your subscription ID.
- `ARM_TENANT_ID`: The `tenant` returned when you created your service principal.

Once finished, your environment should look something like this:

![Configured Azure environment with certificate authentication](<../../assets/screenshots/image (85).png>)

### Credential expiry and rotation

When using static credentials, you are in charge of managing credential rotation. The client secret returned by the `az ad sp create-for-rbac` command will expire after one year. At that point, any stacks using that client secret will stop working until a new one is added and the Spacelift environment is updated.

## Managed identities

Azure [managed identities](https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/){: rel="nofollow"} assigns an identity to an Azure virtual machine that is then used for role assignment. With managed identities, you can grant your Spacelift private workers permission to manage your Azure resources without having to store any credentials in Spacelift _or_ deal with credential rotation.

To use a managed identity, you need to take the following steps:

1. Set up a [private worker pool](../../concepts/worker-pools/README.md).
2. Create an Azure VM with a managed identity, and install the worker binary on it.
3. Configure the [Azure provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/guides/managed_service_identity#configuring-terraform-to-use-a-managed-identity){: rel="nofollow"} to use the managed identity for authentication by adding these environment variables to your stack:
      - `ARM_USE_MSI`: Set to `true` to indicate you want to use a managed identity.
      - `ARM_SUBSCRIPTION_ID`: Your subscription ID.
      - `ARM_TENANT_ID`: Your Microsoft Entra tenant.
4. If you are using a user-assigned identity, add the following variable to your stack:
       - `ARM_CLIENT_ID`: The client ID of your user-assigned identity.

Once finished, your environment should look something like this:

![Azure environment configured with managed identities](<../../assets/screenshots/image (86).png>)
