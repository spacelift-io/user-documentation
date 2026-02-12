# Microsoft Azure

{% if is_saas() %}
!!! hint
    This feature is only available to paid Spacelift accounts. Please check out our [pricing page](https://spacelift.io/pricing){: rel="nofollow"} for more information.
{% endif %}

## Configure workload identity federation

Set up Spacelift as a valid identity provider for your account to allow Spacelift runs access to Azure resources. This is done using [workload identity federation](https://learn.microsoft.com/en-us/azure/active-directory/develop/workload-identity-federation){: rel="nofollow"}.

The setup process involves creating an App Registration, and then adding federated credentials that tell Azure which Spacelift runs should be able to use which App Registrations. This process can be completed via the Azure Portal, Azure CLI or Terraform. For illustrative purposes we will use the Azure Portal.

!!! info
    These instructions show you how to setup federation using a Microsoft Entra App, but the same approach can also be used with a user-assigned managed identity.

### Create an App registration

1. Navigate to the Azure AD section of the Azure Portal.
2. Go to _App registrations_, then click **New registration**.
    ![New registration](<../../../assets/screenshots/oidc-federation-azure-create-app-registration.png>)
3. Enter a name for your registration, select the _Accounts in this organizational directory only_ option, and click **Register**.
    ![Register](<../../../assets/screenshots/oidc-federation-azure-register-app.png>)
4. On the overview page, take note of the _Application (client) ID_ and _Directory (tenant) ID_ for configuring the Terraform provider later.
    ![App registration overview](<../../../assets/screenshots/oidc-federation-azure-app-registration-overview.png>)
5. Go to the _Certificates & secrets_ section, select the **Federated credentials** tab and click **Add credential**.
    ![Add credential](<../../../assets/screenshots/oidc-federation-azure-add-credential.png>)
6. **Federated credential scenario**: Select **Other issuer**.
    ![Other issuer](<../../../assets/screenshots/oidc-federation-azure-add-credential-other-issuer.png>)

### Configure the trust relationship

The next step is to configure the trust relationship between Spacelift and Azure. Fill out the following pieces of information:

- **Issuer**: The URL of your Spacelift account, for example `https://myaccount.app.spacelift.io`.
- **Subject identifier**: The subject that a token must contain to be able to get credentials for your App. This uses the format mentioned in the [standard claims](./README.md#standard-claims) section.
- **Name**: A name for this credential.
- **Audience**: The hostname of your Spacelift account, for example `myaccount.app.spacelift.io`.

Take a look at the following screenshot for an example allowing a proposed run to use our App:

![Proposed run reader](<../../../assets/screenshots/oidc-federation-azure-proposed-run-reader.png>)

Workload federation in Azure requires the subject claim of the OIDC token to exactly match the federated credential, and doesn't allow wildcards. Because of this you will need to repeat the same process and add a number of different federated credentials in order to support all the different types of runs for your Stack or module.

For example, for a stack called `azure-oidc-test` in the `legacy` space (with space ID `legacy-01KJMM56VS4W3AL9YZWVCXBX8D`) you need to add credentials for the following subjects:

```text
space:legacy-01KJMM56VS4W3AL9YZWVCXBX8D:stack:azure-oidc-test:run_type:TRACKED:scope:read
space:legacy-01KJMM56VS4W3AL9YZWVCXBX8D:stack:azure-oidc-test:run_type:TRACKED:scope:write
space:legacy-01KJMM56VS4W3AL9YZWVCXBX8D:stack:azure-oidc-test:run_type:PROPOSED:scope:read
space:legacy-01KJMM56VS4W3AL9YZWVCXBX8D:stack:azure-oidc-test:run_type:TASK:scope:write
space:legacy-01KJMM56VS4W3AL9YZWVCXBX8D:stack:azure-oidc-test:run_type:DESTROY:scope:write
```

And for a module called `my-module` in the `development` space (with space ID `development-01JS2ABCDEFGHIJK123456789`) you need to add the following:

```text
space:development-01JS2ABCDEFGHIJK123456789:stack:my-module:run_type:TESTING:scope:read
space:development-01JS2ABCDEFGHIJK123456789:stack:my-module:run_type:TESTING:scope:write
```

After adding all the credentials for a stack, it should look something like this:

![Stack credentials added](<../../../assets/screenshots/oidc-federation-azure-stack-credentials.png>)

!!! info
    Please see the [Standard claims](README.md#standard-claims) section for more information about the subject format.

### Using custom subject templates

If you have configured a [custom OIDC subject template](subject-template.md) that includes the `{spacePath}` placeholder, you will need to update your federated credentials to match the new subject format.

For example, if your custom template is:

```text
space:{spaceId}:space_path:{spacePath}:{callerType}:{callerId}:run_type:{runType}:scope:{scope}
```

And you have a stack `azure-test` in the space `/root/production/us-east-1`, you would need to add credentials like:

```text
space:us-east-1:space_path:/root/production/us-east-1:stack:azure-test:run_type:TRACKED:scope:read
space:us-east-1:space_path:/root/production/us-east-1:stack:azure-test:run_type:TRACKED:scope:write
space:us-east-1:space_path:/root/production/us-east-1:stack:azure-test:run_type:PROPOSED:scope:read
space:us-east-1:space_path:/root/production/us-east-1:stack:azure-test:run_type:TASK:scope:write
space:us-east-1:space_path:/root/production/us-east-1:stack:azure-test:run_type:DESTROY:scope:write
```

This is particularly useful when you have identically-named spaces in different branches of your space hierarchy (e.g., `/root/production/us-east-1` vs `/root/staging/us-east-1`), as it allows you to distinguish between them in your federated credentials.

!!! warning
    Remember that Azure does not support wildcards in federated credentials, so you must add an exact match for each combination of run type and scope that you want to support, even when using custom subject templates.

!!! hint
    See the [Customizing the OIDC Subject Claim](subject-template.md) guide for more information on how to configure custom subject templates and migrate existing federated credentials safely.

## Configure the Terraform provider

Once workload identity federation is set up, the [AzureRM provider can be configured](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/guides/service_principal_oidc){: rel="nofollow"} without the need for any static credentials.

1. Enable the `use_oidc` feature of the provider.
2. Use the `oidc_token_file_path` setting to tell the provider where to find the token:

    ```terraform
    provider "azurerm" {
    features {}
    use_oidc             = true
    oidc_token_file_path = "/mnt/workspace/spacelift.oidc"
    }
    ```

3. Next, add the following environment variables to your stack:
   - `ARM_CLIENT_ID`: The client ID of the App registration created in the previous section.
   - `ARM_TENANT_ID`: The tenant ID of the App registration created in the previous section.
   - `ARM_SUBSCRIPTION_ID`: The ID of the Azure subscription you want to use.

Before you can use your App registration to manage Azure resources, you need to assign the correct [RBAC permissions](https://learn.microsoft.com/en-us/azure/role-based-access-control/overview){: rel="nofollow"} to it.
