# Google Cloud Platform (GCP)

!!! info
    We strongly recommend using [OIDC](oidc/README.md) for the GCP integration.

Spacelift's GCP integration allows Spacelift to manage your Google Cloud resources without the need for long-lived static credentials by creating a [service account](https://cloud.google.com/iam/docs/service-accounts){: rel="nofollow"} inside the project dedicated to your Stack. We show you the globally unique email of this service account, which you can add to your GCP organizations and/or projects with the right level of access.

With the service account already created, Spacelift generates temporary OAuth token for the service account as a `GOOGLE_OAUTH_ACCESS_TOKEN` variable in the environment of your [runs](../../concepts/run/README.md) and [tasks](../../concepts/run/task.md). This is [one of the configuration options](https://www.terraform.io/docs/providers/google/guides/provider_reference.html#access_token-1){: rel="nofollow"} for the Google Terraform provider, so you can define it like this:

```terraform
provider "google" {}
```

Many GCP resources require the [`project`](https://www.terraform.io/docs/providers/google/guides/provider_reference.html#project-1){: rel="nofollow"} identifier too, so if you don't specify a default in your provider, you will need to pass it to each individual resource that requires it.

## Integrate GCP in the Spacelift UI

### OAuth Scopes

You can customize the list of [OAuth scopes](https://developers.google.com/identity/protocols/googlescopes){: rel="nofollow"} that the token is granted when it's generated. When you're setting up your GCP integration through the web UI, we suggest the following list of scopes:

- `https://www.googleapis.com/auth/compute`
- `https://www.googleapis.com/auth/cloud-platform`
- `https://www.googleapis.com/auth/ndev.clouddns.readwrite`
- `https://www.googleapis.com/auth/devstorage.full_control`
- `https://www.googleapis.com/auth/userinfo.email`

This list is consistent with the [defaults requested by the Terraform provider](https://www.terraform.io/docs/providers/google/guides/provider_reference.html#scopes-1){: rel="nofollow"}.

## Set up integration

To set up the GCP integration in Spacelift, you must already have a [stack](../../concepts/stack/README.md) configured.

1. On the _Stacks_ tab, click the **three dots** beside the stack you would like to integrate with GCP.
2. Click **Settings**, then click **Integrations**.
3. Click **Attach cloud integration**.
4. Select **GCP**, then verify the OAuth scopes.
    - If you need to add additional scopes, click **Add another scope**, then type in the scope.
5. Click **Attach**.

![Set up GCP integration](<../../assets/screenshots/integrations/cloud-providers/gcp/UI-integration.png>)

Once the integration is attached, Spacelift will display its globally unique service account email. You will use this email to [set up access in GCP](gcp.md#set-up-access-in-gcp).

![Service account email](<../../assets/screenshots/Edit_stack_·_Spacelift_development (2).png>)

### Set up programmaticaly in Terraform

If you're using Spacelift Terraform provider to create the integration programmatically, you can do the following to configure the GCP integration and OAuth scopes:

```terraform
resource "spacelift_gcp_service_account" "gcp-integration" {
  stack_id = spacelift_stack.your-stack.id

  token_scopes = [
    "https://www.googleapis.com/auth/compute",
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/ndev.clouddns.readwrite",
    "https://www.googleapis.com/auth/devstorage.full_control",
    "https://www.googleapis.com/auth/userinfo.email",
  ]
}
```

If the service account linked to your administrative stack has sufficient privileges on the GCP organization, you can programmatically create a dedicated GCP project and set up the integration from the Google side of things:

```terraform
resource "google_project" "k8s-core" {
  name       = "Kubernetes core"
  project_id = "unicorn-k8s-core"
  org_id     = var.gcp_organization_id
}

resource "google_project_iam_member" "k8s-core" {
  project = google_project.k8s-core.id
  role    = "roles/owner"
  member  = "serviceAccount:${spacelift_stack_gcp_service_account.gcp-integration.service_account_email}"
}
```

## Set up access in GCP

To make the integration work, you need to make the dedicated service account a member of your organization and/or project, with an appropriate level of access. This is done in the [IAM & Admin](https://console.cloud.google.com/iam-admin/iam){: rel="nofollow"} view of GCP's web UI.

### Organization level

This is what you should see when adding a service account as a member on the organization level:

![Set as member on the organization level](<../../assets/screenshots/IAM_–_IAM___admin_–_spacelift_io_–_Google_Cloud_Platform.png>)

!!! info
    In the above example, we made the service account an owner of the organization, giving it full access to all resources. Depending on your use case, you may want to alter the permissions.

### Project level

The process of adding a service account as a member on the project level looks absolutely identical except that projects are represented by a different icon in the dropdown:

![Set as member on the project level](<../../assets/screenshots/IAM_–_IAM___admin_–_spacelift-developme…_–_Google_Cloud_Platform.png>)

It can take up to a minute for the membership data to propagate but once it does, your Spacelift-GCP integration should be active.
