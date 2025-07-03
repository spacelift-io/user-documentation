# Login policy

!!! info
    We do not support importing rego.v1 at this time. For more details, see the [introduction](../policy/README.md).

## Purpose

Login policies allow users to log in to the Spacelift account and can grant admin privileges. Unlike all other policy types, login policies are global and can't be attached to individual stacks. They take effect immediately once they're created and affect all future login attempts.

API Keys are treated as virtual users and evaluated with login policy unless they are in the "root" space set with an admin key.

!!! tip
    GitHub or [SSO](../../integrations/single-sign-on/README.md) admins and private account owners always have admin access to their respective Spacelift accounts, regardless of login policies, so login policy errors can't lock everyone out of the account.

!!! danger
    Any changes (create, update, or delete) made to a login policy will invalidate **all** active sessions except the session making the change.

A login policy can define the following types of boolean rules:

- **allow**: Allows the user to log in as a _non-admin_
- **admin**: Allows the user to log in as an account-wide _admin_. You don't need to explicitly **allow** admin users
- **deny**: Denies the login attempt, regardless of other (**allow** and **admin**) rules
- **deny_admin**: Denies the current user **admin** access to the stack, regardless of other rules
- **space_admin/space_write/space_read**: Manages access levels to spaces. Learn more in [Spaces Access Control](../spaces/access-control.md)

If no rules match, the default action will be to **deny** a login attempt.

!!! warning "Define Restrictions"
    Any time you define an **allow** or **admin** rule, consider restricting access using a **deny** rule, too. See an example [below](#managing-access-levels-within-an-organization).

Admins have significant privileges and can create and delete stacks; trigger runs or tasks; create, delete, and attach contexts and policies; etc. Unless full admin access is necessary, grant users _limited_ admin access using the **space_admin** rule.

## Data input

Each policy request will receive this data input:

```json title="data_input_schema.json"
{
  "request": {
    "remote_ip": "string - IP of the user trying to log in",
    "timestamp_ns": "number - current Unix timestamp in nanoseconds"
  },
  "session": {
    "creator_ip": "string - IP address of the user who created the session",
    "login": "string - username of the user trying to log in",
    "member": "boolean - is the user a member of the account",
    "name": "string - full name of the user trying to log in - may be empty",
    "teams": ["string - names of teams the user is a member of"]
  },
  "spaces": [
    {
      "id": "string - ID of the space",
      "name": "string - name of the space",
      "labels": ["string - label of the space"]
    }
  ]
}
```

!!! tip
    OPA string comparisons are case-sensitive. Use the proper case as defined in your Identity Provider when comparing values.

    We recommend enabling [sampling on the policy](./README.md#sampling-policy-inputs) to see the exact values passed by the Identity Provider.

Two fields in the `session` object require further explanation: _member_ and _teams_.

### _member_

=== "Using GitHub (Default Identity Provider)"

    When you first log in to Spacelift, we retrieve some details (such as username) from GitHub, our default identity provider. Each Spacelift account is linked to only one GitHub account. Thus, when you log in to a Spacelift account, we're checking if you're a member of the associated GitHub account.

    When the GitHub account is an organization, we can explicitly query for your organization membership. If you're a member, the `member` field is set to _true_. If you're not, it's _false_. Private accounts only have one member, so the check is even simpler: if your login is the same as the name of the linked GitHub account, the member field is set to _true_. If not, it's _false_.

=== "Using Single Sign-On"

    When using Single Sign-On with SAML, every successful login attempt will require that the `member` field is set to _true_. If the linked IdP could verify you, you **must** be a member.

!!! tip
    The `member` field is useful for your **deny** rules.

### _teams_

=== "Using GitHub (Default Identity Provider)"

    When using the default identity provider (GitHub), _teams_ are only queried for organization accounts. If you're a member of the GitHub organization linked to a Spacelift account, Spacelift will query the GitHub API for the full list of teams you're a member of. This list will be available in the `session.teams` field. For private accounts and non-members, the field will be empty.

    Spacelift treats GitHub team membership as transitive. For example, let's assume Charlie is a member of the _Badass_ team, which is a child of team _Awesome_. Charlie's list of teams includes both _Awesome_ and _Badass_, even though he's not a **direct** member of the team _Awesome_.

=== "Using Single Sign-On"

    For Single Sign-On, the list of teams depends on how the SAML assertion attribute is mapped to your user record on the IdP end. Please see [Single Sign-On](../../integrations/single-sign-on/README.md#setting-up-saml) for more details.

!!! tip
    The `teams` field is useful for your **allow** and **admin** rules.

## Login policy examples

!!! abstract "Example Policies Library"
    We maintain a [library of example policies](https://github.com/spacelift-io/spacelift-policies-example-library/tree/main/examples/login){: rel="nofollow"} that are ready to use as-is or tweak to meet your specific needs.

    If you can't find what you're looking for below or in the library, please reach out to [Spacelift support](../../product/support/README.md#contact-support) and we will craft a policy to meet your needs.

There are three main use cases for login policies: managing access within an organization, managing access for external contributors, or restricting access in specific circumstances.

We recommend having only _one login policy_ to avoid unexpected results when multiple policies are merged.

### Managing access levels within an organization

In high-security environments where the principle of least privilege is applied, it's possible nobody on the infrastructure team is given admin access to _GitHub_. Still, it would be useful for the infrastructure team to be in charge of your Spacelift account.

Let's create a login policy that will give every member of the DevOps team admin access and everyone in Engineering regular access. We'll give them more granular access to individual stacks later using [stack access policies](stack-access-policy.md). We'll also explicitly **deny** access to all non-members, just to be on the safe side.

```opa
package spacelift

teams := input.session.teams

# Make sure to use the GitHub team names, not IDs (e.g., "Example Team" not "example-team")
# and omit the GitHub organization name
admin { teams[_] == "DevOps" }
allow { teams[_] == "Engineering" }
deny  { not input.session.member }
```

Here's an [example to play with](https://play.openpolicyagent.org/p/LpzDekpDOU){: rel="nofollow"}.

This is also important for Single Sign-On integrations: only the [integration creator](../../integrations/single-sign-on/README.md) gets administrative permissions by default, so all other administrators must be granted their access using a login policy.

### Granting access to external contributors

!!! warning
    This feature is not available when using [Single Sign-On](../../integrations/single-sign-on/README.md) because your identity provider **must** be able to successfully validate each user trying to log in to Spacelift.

Sometimes people who are not members of your organization, such as consultants, need access to your Spacelift account. Other times, a group of friends working on a project in a personal GitHub account could use access to Spacelift. Here are examples of a policy that grants several allowlisted people regular access, and one person admin privileges:

=== "GitHub"

    This example uses GitHub usernames to grant access to Spacelift.

    ```opa
    package spacelift

    admins  := { "alice" }
    allowed := { "bob", "charlie", "danny" }
    login   := input.session.login

    admin { admins[login] }
    allow { allowed[login] }
    deny  { not admins[login]; not allowed[login] }
    ```

    Here's an [example to play with](https://play.openpolicyagent.org/p/ZsOJayumFw){: rel="nofollow"}.

=== "Google"
    This example uses email addresses managed by Google to grant access to Spacelift.

    ```rego
    package spacelift

    admins  := { "alice@example.com" }
    login   := input.session.login

    admin { admins[login] }
    allow { endswith(input.session.login, "@example.com") }
    deny  { not admins[login]; not allow }
    ```

!!! warning
    Granting access to individuals is more risky than granting access to only teams and account members. In the latter case, when an account member loses access to your GitHub organization, they automatically lose access to Spacelift. But when allowlisting individuals and not restricting access to members only, you'll need to explicitly remove the individuals from your Spacelift login policy.

### Restricting access in specific circumstances

Stable and secure infrastructure is crucial to business continuity. All changes to your infrastructure carry some risk, so you may want to restrict access to it. The example below shows a comprehensive policy that restricts Spacelift access to users logging in from the office IP during business hours. You may want to use elements of this policy to create your own (less draconian) version, or keep it this way to support everyone's work-life balance.

This example only defines deny rules, so you'll likely want to add some allow and admin rules, either in this policy or in a separate one.

```opa
package spacelift

now     := input.request.timestamp_ns
clock   := time.clock([now, "America/Los_Angeles"])
weekend := { "Saturday", "Sunday" }
weekday := time.weekday(now)
ip      := input.request.remote_ip

deny { weekend[weekday] }
deny { clock[0] < 9 }
deny { clock[0] > 17 }
deny { not net.cidr_contains("12.34.56.0/24", ip) }
```

Here's an [example to play with](https://play.openpolicyagent.org/p/4J3Nz6pYgC){: rel="nofollow"}.

### Granting limited admin access

Sometimes, you want to give a user admin access limited to a certain set of resources, so that they can manage them without having access to all other resources in that account. You can find more on this use case in [Spaces](../spaces/README.md).

### Rewriting teams

In addition to boolean rules regulating access to your Spacelift account, the login policy exposes the **team** rule, which allows you to dynamically rewrite the list of teams and define Spacelift roles independent of the identity provider. To illustrate this use case, imagine you want to define a `Superwriter` role for someone who's:

- logging in from an office VPN
- a member of the DevOps team, as defined by your IdP
- not a member of the Contractors team, as defined by your IdP

```opa title="Defining Superwriter"
package spacelift

team["Superwriter"] {
  office_vpn
  devops
  not contractor
}

contractor { input.session.teams[_] == "Contractors" }
devops     { input.session.teams[_] == "DevOps" }
office_vpn { net.cidr_contains("12.34.56.0/24", input.request.remote_ip)  }
```

Here, the **team** rule overwrites the original list of teams, so if it evaluates to a non-empty collection, it will **replace** the original list of teams in the session. In the above example, the `Superwriter` role will become the only team for the evaluated user session.

If you want to retain the original list of teams, you can modify the above example:

```opa title="Defining Superwriter While Retaining Teams List"
package spacelift

# This rule will copy each of the existing teams to the
# new modified list.
team[name] { name := input.session.teams[_] }

team["Superwriter"] {
  office_vpn
  devops
  not contractor
}

contractor { input.session.teams[_] == "Contractors" }
devops     { input.session.teams[_] == "DevOps" }
office_vpn { net.cidr_contains("12.34.56.0/24", input.request.remote_ip)  }
```

Here's an [example to play with](https://play.openpolicyagent.org/p/dM8P83sk4l){: rel="nofollow"}.

!!! tip
    Because the user session is updated, the rewritten teams are available in the data input provided to the policy types that receive user information. For example, the rewritten teams can be used in [Access policies](./stack-access-policy.md).

## Default login policy

If no login policies are defined on the account, Spacelift behaves as if it had this policy and **allows** all users:

```opa
package spacelift

allow { input.session.member }
```
