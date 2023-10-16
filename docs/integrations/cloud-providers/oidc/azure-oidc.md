# Microsoft Azure

## Configuring workload identity federation

In order to enable Spacelift runs to access Azure resources, you need to set up Spacelift as a valid identity provider for your account. This is done using [workload identity federation](https://learn.microsoft.com/en-us/azure/active-directory/develop/workload-identity-federation){: rel="nofollow"}. The set up process involves creating an App Registration, and then adding federated credentials that tell Azure which Spacelift runs should be able to use which App Registrations. This process can be completed via the Azure Portal, Azure CLI or Terraform. For illustrative purposes we will use the Azure Portal.

The first step is to go to the Azure AD section of the Azure Portal, go to _App registrations_, and then click on the _New registration_ button:

![New registration](<../../../assets/screenshots/oidc-federation-azure-create-app-registration.png>)

Specify a name for your registration, select the _Accounts in this organizational directory only_ option, and click on the _Register_ button:

![Register](<../../../assets/screenshots/oidc-federation-azure-register-app.png>)

On the overview page, take a note of the _Application (client) ID_ and _Directory (tenant) ID_ - you will need them later when configuring the Terraform provider.

![App registration overview](<../../../assets/screenshots/oidc-federation-azure-app-registration-overview.png>)

Next, go to the _Certificates & secrets_ section, select the _Federated credentials_ tab and click on the _Add credential_ button:

![Add credential](<../../../assets/screenshots/oidc-federation-azure-add-credential.png>)

On the next screen, choose _Other issuer_ as the _Federated credential scenario_:

![Other issuer](<../../../assets/screenshots/oidc-federation-azure-add-credential-other-issuer.png>)

The next step is to configure the trust relationship between Spacelift and Azure. In order to do this, we need to fill out the following pieces of information:

- Issuer - the URL of your Spacelift account, for example `https://myaccount.app.spacelift.io`.
- Subject identifier - the subject that a token must contain to be able to get credentials for your App. This uses the format mentioned in the [Standard claims](README.md#standard-claims) section.
- Name - a name for this credential.
- Audience - the hostname of your Spacelift account, for example `myaccount.app.spacelift.io`.

Take a look at the following screenshot for an example allowing a proposed run to use our App:

![Proposed run reader](<../../../assets/screenshots/oidc-federation-azure-proposed-run-reader.png>)

Workload federation in Azure requires the subject claim of the OIDC token to exactly match the federated credential, and doesn't allow wildcards. Because of this you will need to repeat the same process and add a number of different federated credentials in order to support all the different types of runs for your Stack or module. For example for a stack called `azure-oidc-test` in the `legacy` space you need to add credentials for the following subjects:

```text
space:legacy:stack:azure-oidc-test:run_type:TRACKED:scope:read
space:legacy:stack:azure-oidc-test:run_type:TRACKED:scope:write
space:legacy:stack:azure-oidc-test:run_type:PROPOSED:scope:read
space:legacy:stack:azure-oidc-test:run_type:TASK:scope:write
space:legacy:stack:azure-oidc-test:run_type:DESTROY:scope:write
```

And for a module called `my-module` in the `development` space you need to add the following:

```text
space:development:stack:my-module:run_type:TESTING:scope:read
space:development:stack:my-module:run_type:TESTING:scope:write
```

After adding all the credentials for a stack, it should look something like this:

![Stack credentials added](<../../../assets/screenshots/oidc-federation-azure-stack-credentials.png>)

!!! info
    Please see the [Standard claims](README.md#standard-claims) section for more information about the subject format.

## Configuring the Terraform Provider

Once workload identity federation is set up, the AzureRM provider [can be configured](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/guides/service_principal_oidc){: rel="nofollow"} without the need for any static credentials. To do this, enable the `use_oidc` feature of the provider, and use the `oidc_token_file_path` setting to tell the provider where to find the token:

```terraform
provider "azurerm" {
  features {}
  use_oidc             = true
  oidc_token_file_path = "/mnt/workspace/spacelift.oidc"
}
```

Next, add the following environment variables to your stack:

- `ARM_CLIENT_ID` - the client ID of the App registration created in the previous section.
- `ARM_TENANT_ID` - the tenant ID of the App registration created in the previous section.
- `ARM_SUBSCRIPTION_ID` - the ID of the Azure subscription you want to use.

!!! info
    Note - before you can use your App registration to manage Azure resources, you need to assign the correct [RBAC permissions](https://learn.microsoft.com/en-us/azure/role-based-access-control/overview){: rel="nofollow"} to it.
