# Login Policy Best Practices

When creating a Login policy, it's important to follow some best practices to ensure that your policy is secure and easy to manage.

Some high level best practices are:

- When creating a Login policy, it's important to use a descriptive name that clearly indicates the purpose of the policy. This will make it easier to identify the policy in the future and ensure that it is applied correctly.
- When creating a Login policy, it's important to limit the scope of the policy to only the resources that are necessary. This will help to reduce the risk of unauthorized access and ensure that the policy is easy to manage.
- It's important to regularly review and update your Login policy to ensure that it remains up-to-date and reflects the current state of your organization. This will help to ensure that the policy continues to provide the necessary level of access control and security.
- Granting access to individuals is less safe than granting access to teams and restricting access to account members. In the latter case, when they lose access to your GitHub org, they automatically lose access to Spacelift. But when whitelisting individuals and not restricting access to members only, you'll need to remember to explicitly remove them from your Spacelift login policy, too.
- We recommend having only one login policy as what sounds reasonable within a policy may not yield the expected results when the decisions are merged.

## API Keys

API Keys are essentially virtual users so they get evaluated with login policy except for ones in the "root" space set with admin key.

You can reference an API key in the policy by using the string `api::{id}` where `{id}` is the ID of the API key. As an example, this following policy will allow api key with the ID `01J5BMM8WC0FDVY94HFR0FJFN3` admin access:

```rego
admin { input.session.login == "api::01J5BMM8WC0FDVY94HFR0FJFN3" }
allow { input.session.login == "api::01J5BMM8WC0FDVY94HFR0FJFN3" }
```

## Admins

## Rule Callout

When you make someone an `admin` via a rule, you must also `allow` them into the platform with an `allow` rule. This is because the `admin` rule only grants them the ability to manage the platform, not to log in.

The following policy will _not_ work.

```rego
admin { input.session.login == "jimmy-developer@spacelift.io" }
```

The following policy will work, and Jimmy will be a platform admin.

```rego
admin { input.session.login == "jimmy-developer@spacelift.io" }
allow { input.session.login == "jimmy-developer@spacelift.io" }
```

In practice, any time you define an **allow** or **admin** rule, you should think of restricting access using a **deny** rule, too.

The following example will allow jimmy-developer to login as an admin, will allow anyone to login on the `Engineering` team, but will deny anyone not a member.

```rego
admin { input.session.login == "jimmy-developer@spacelift.io" }
allow { input.session.teams[_] == "Engineering" }
deny  { not input.session.member }
```

## GitHub Callout

Login policies don't affect GitHub organization or [SSO](../../../integrations/single-sign-on/README.md) admins and private account owners who always get admin access to their respective Spacelift accounts. This is to avoid a situation where a bad login policy locks out everyone from the account.

## Rules

There are a few things to keep in mind while writing your login policy:

- OPA string comparisons are case-sensitive so make sure to use the proper case, as defined in your Identity Provider when comparing values.
    - It might be helpful to [enable sampling on the policy](../README.md#sampling-policy-inputs) to see the exact values passed by the Identity Provider.
- Any change made (create, update or delete) to a login policy will invalidate all active sessions, except the session making the change.

When writing your login policy, watch the `input.session.member` fields, it may be useful for your **deny** rules.
When writing your login policy, watch the `input.session.teams` fields, it may be useful for your **allow** and **admin** rules.

## Examples

We maintain a [library of example policies](https://github.com/spacelift-io/spacelift-policies-example-library/tree/main/login){: rel="nofollow"} that are ready to use or that you could tweak to meet your specific needs.
If you cannot find what you are looking for in the library, please reach out to [our support](../../../product/support/README.md#contact-support) and we will help guide you.
