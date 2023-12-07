# FAQ

Spacelift has many features and hidden nuggets so it is easy to overlook some of them but we have you covered with this list of frequently asked questions.

If you still cannot find the answer to your question below, please reach out to our [support team](../product/support/README.md).

{% if is_saas() %}

## Product

### How to submit a feature request?

![](../assets/screenshots/feature-request.png)

- Go to the "Resource center" section, in the bottom-left corner menu.
- Fill in your problem or request, what you are trying to achieve, and optionally, your current work around. Then, scroll down to submit your request.

If you wish to view feature requests you have previously submitted, you can access the portal through this pop-out. There, you'll be able to see the status of your requests.

Additionally, the portal allows you to vote on and join discussions about other requests, review new releases, and see upcoming features.

{% endif %}

### Providing Admin consent for Microsoft login

In order to sign up for Spacelift using an Azure AD account via our Microsoft login option, the Spacelift application needs to be installed into your Azure AD directory. To do this you either need to be an Azure AD administrator, or your Azure AD configuration needs to allow users to install applications.

If you don't have permission, you will receive the following message when attempting to sign up:

![](../assets/screenshots/faq-ms-login-admin-consent-required.png)

If this happens, it means that you need ask an Azure AD admin to provide Admin consent, as described in the [Microsoft documentation](https://learn.microsoft.com/en-us/azure/active-directory/manage-apps/grant-admin-consent?pivots=portal){: rel="nofollow"}.

To do this, your Azure AD admin can use a URL like the following to grant permission to Spacelift:

```text
https://login.microsoftonline.com/<tenant-id>/adminconsent?client_id=fba648b0-4b78-4224-b510-d96ff51eeef9
```

!!! info
    NOTE: make sure to replace `<tenant-id>` with your Azure AD Tenant ID!

After granting admin consent, your administrator will be redirected to Spacelift and receive the following error message, which can be safely ignored:

![](../assets/screenshots/faq-ms-login-empty-code-error.png)

After admin consent has been provided, you should be able to sign-up for Spacelift using your Microsoft account.

## Platforms

### Terraform

#### How do I import the Terraform state for my stack?

The Terraform state file can be imported during the [creation of a stack](../concepts/stack/creating-a-stack.md#terraform).

#### How do I export the Terraform state for my stack?

The Terraform state file can be pulled and then exported using a [Task](../concepts/run/task.md).

For example, to export the state to an Amazon S3 bucket, you would run the following command as a Task:

```shell
terraform state pull > state.json && aws s3 cp state.json s3://<PATH>
```

!!! warning
    For that example to work, the stack needs to have write access to the AWS S3 bucket, possibly via an [AWS Integration](../integrations/cloud-providers/aws.md).

#### How do I switch from Spacelift managing the Terraform state to me managing it?

You would first need to [export the state file](#how-do-i-export-the-terraform-state-for-my-stack) to a suitable location.

The state management setting can not be changed once a stack has been created so you will need to recreate the stack and make sure that [the "Manage state" setting](../concepts/stack/creating-a-stack.md#terraform) is disabled.

### How do I manipulate the Terraform state file?

You can manipulate the Terraform state by running `terraform state <SUBCOMMAND>` commands in a [Task](../concepts/run/task.md).

This applies whether you or Spacelift manages the Terraform state file.

#### How do I import existing resources into a Terraform stack?

Just [run the `terraform import …` in a Task](../vendors/terraform/state-management.md#importing-resources-into-your-terraform-state).

This applies whether you or Spacelift manages the Terraform state file.

## Policies

### My policy works fine in the workbench but not on my stack/module

Except for the Login policies, all policies must be attached to stacks or modules to be evaluated so let's first confirm this by verifying that the stack or module is listed in the "Used by" section on the policy page. If it does not show up there, you will need to [attach the policy](../concepts/policy/README.md#attaching-policies).

If your policy is attached to your stack/module and you still do not see the expected behavior from that policy, you should make sure that [sampling is enabled](../concepts/policy/README.md#sampling-policy-inputs) for that policy, and then review the recorded samples in the [Policy Workbench](../concepts/policy/README.md#policy-workbench-in-practice). That should give you valuable insight.

If you do not see any sampled events despite sampling being enabled and having performed events that should have triggered events, make sure that the appropriate type was selected when the policy was created.

### I do not see some samples for my Login policy

Login policies are not evaluated for account creators and SSO admins who always get admin access to their respective Spacelift accounts. This is to avoid a situation where a bad Login policy locks out everyone from the account.

The side-effect is that you will not see samples for these users.

### Are Approval policies and run confirmation the same thing?

[Approval policies](../concepts/policy/approval-policy.md) and [run confirmation](../concepts/run/tracked.md#confirmed) are related but different concepts.

Just think about how GitHub's Pull Requests work - you can approve a PR before merging it in a separate step. Just like a PR approval means "I'm OK with this being merged", a run approval means "I'm OK with that action being executed" but nothing will happen until someone clicks on the "Merge" or "Confirm" button, respectively.

## Billing

### What counts as a user?

Everyone who logged in to the Services in a given month is counts as a user.

API keys are virtual users and are billed like regular users, too. Thus, each API key used during any billing cycle counts against the total number of users.

When setting up SSO, future logins will appear as new users since Spacelift cannot map those without your assistance. New users will count against your quota, and you may run out of seats. If you run into this problem, you can [contact us](https://spacelift.io/contact){: rel="nofollow"}.
