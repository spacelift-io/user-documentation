# Login policy

## Purpose

!!! info
    Please note, we currently don't support importing rego.v1

Login policies can allow users to log in to the account, and optionally give them admin privileges, too. Unlike all other policy types, login policies are global and can't be attached to individual stacks. They take effect immediately once they're created and affect all future login attempts.

!!! info
    API Keys are essentially virtual users so they get evaluated with login policy except for ones in the "root" space set with admin key.

!!! warning
    Login policies don't affect GitHub organization or [SSO](../../integrations/single-sign-on/README.md) admins and private account owners who always get admin access to their respective Spacelift accounts. This is to avoid a situation where a bad login policy locks out everyone from the account.

!!! danger
    Any change made (create, update or delete) to a login policy will invalidate all active sessions, except the session making the change.

A login policy can define the following types of boolean rules:

- **allow** - allows the user to log in as a _non-admin_;
- **admin** - allows the user to log in as an account-wide _admin_ - note that you don't need to explicitly **allow** admin users;
- **deny** - denies login attempt, no matter the result of other (**allow** and **admin**) rules;
- **deny_admin** - denies the current user **admin** access to the stack, no matter the outcome of other rules;
- **space_admin/space_write/space_read** - manages access levels to spaces. More on that in [Spaces Access Control](../spaces/access-control.md);

If no rules match, the default action will be to deny a login attempt.

Note that giving folks admin access is a big thing. Admins can do pretty much everything in Spacelift - create and delete stacks, trigger runs or tasks, create, delete and attach contexts and policies, etc. Instead, you can give users limited admin access using the **space_admin** rule.

!!! danger
    In practice, any time you define an **allow** or **admin** rule, you should probably think of restricting access using a **deny** rule, too. Please see the examples below to get a better feeling for it.

## Data input

This is the schema of the data input that each policy request will receive:

```json
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
    OPA string comparisons are case-sensitive so make sure to use the proper case, as defined in your Identity Provider when comparing values.

    It might be helpful to [enable sampling on the policy](./README.md#sampling-policy-inputs) to see the exact values passed by the Identity Provider.

Two fields in the session object may require further explanation: _member_ and _teams_.

### Account membership

When you first log in to Spacelift, we use GitHub as the identity provider and thus we're able to get some of your details from there with username (login) being the most important one. However, each Spacelift account is linked to one and only one GitHub account. Thus, when you log in to a Spacelift account, we're checking if you're a member of that GitHub account.

When that GitHub account is an organization, we can explicitly query for your organization membership. If you're a member, you get the member field set to _true_. If you're not - it's _false_. For private accounts it's different - they can only have one member, so the check is even simpler - if your login is the same as the name of the linked GitHub account, you get the member field set to _true_. If it isn't - it's _false_.

When using Single Sign-On with SAML, every successful login attempt will necessarily require that the _member_ field is set to _true -_ if the linked IdP could verify you, you **must** be a member.

!!! warning
    Watch this field very closely - it may be _very_ useful for your **deny** rules.

#### Teams

When using the default identity provider (GitHub), Teams are only queried for organization accounts - if you're a member of the GitHub organization linked to a Spacelift account, Spacelift will query GitHub API for the full list of teams you're a member of. This list will be available in the `session.teams` field. For private accounts and non-members, this list will be empty.

Note that Spacelift treats GitHub team membership as transitive - for example let's assume Charlie is a member of the _Badass_ team, which is a child of team _Awesome_. Charlie's list of teams includes both _Awesome_ and _Badass_, even though he's not a **direct** member of the team _Awesome_.

For Single Sign-On, the list of teams is pretty much arbitrary and depends on how the SAML assertion attribute is mapped to your user record on the IdP end. Please see the [relevant article](../../integrations/single-sign-on/README.md#setting-up-the-integration) for more details.

!!! warning
    Watch this field very closely - it may be _very_ useful for your **allow** and **admin** rules.

## Examples

!!! tip
    We maintain a [library of example policies](https://github.com/spacelift-io/spacelift-policies-example-library/tree/main/login){: rel="nofollow"} that are ready to use or that you could tweak to meet your specific needs.

    If you cannot find what you are looking for below or in the library, please reach out to [our support](../../product/support/README.md#contact-support) and we will craft a policy to do exactly what you need.

    We recommend having only one login policy as what sounds reasonable within a policy may not yield the expected results when the decisions are merged.

There are three possible use cases for login policies - granting access to folks in your org who would otherwise not have it, managing access for external contributors or restricting access to specific circumstances. Let's look into these use cases one by one.

### Managing access levels within an organization

In high-security environments where the principle of least access is applied, it's quite possible that nobody on the infra team gets admin access to _GitHub_. Still, it would be pretty useful for those people to be in charge of your _Spacelift_ account. Let's create a login policy that will allow every member of the DevOps team to get admin access, and everyone in Engineering to get regular access - we'll give them more granular access to individual stacks later using [stack access policies](stack-access-policy.md). While at it, let's also explicitly deny access to all non-members just to be on the safe side.

```opa
package spacelift

teams := input.session.teams

# Make sure to use the GitHub team names, not IDs (e.g., "Example Team" not "example-team")
# and to omit the GitHub organization name
admin { teams[_] == "DevOps" }
allow { teams[_] == "Engineering" }
deny  { not input.session.member }
```

Here's a [minimal example to play with](https://play.openpolicyagent.org/p/LpzDekpDOU){: rel="nofollow"}.

This is also important for Single Sign-On integrations: only the [integration creator](../../integrations/single-sign-on/README.md#setting-up-the-integration) gets administrative permissions by default, so all other administrators must be granted their access using a login policy.

### Granting access to external contributors

!!! danger
    This feature is not available when using [Single Sign-On](../../integrations/single-sign-on/README.md) - your identity provider **must** be able to successfully validate each user trying to log in to Spacelift.

Sometimes you have folks (short-term consultants, most likely) who are not members of your organization but need access to your Spacelift account - either as regular members or perhaps even as admins. There's also the situation where a bunch of friends is working on a hobby project in a personal GitHub account and they could use access to Spacelift. Here are examples of a policy that allows a bunch of whitelisted folks to get regular access and one to get admin privileges:

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

    Here's a [minimal example to play with](https://play.openpolicyagent.org/p/ZsOJayumFw){: rel="nofollow"}.

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
    Note that granting access to individuals is less safe than granting access to teams and restricting access to account members. In the latter case, when they lose access to your GitHub org, they automatically lose access to Spacelift. But when whitelisting individuals and not restricting access to members only, you'll need to remember to explicitly remove them from your Spacelift login policy, too.

### Restricting access to specific circumstances

Stable and secure infrastructure is crucial to your business continuity. And all changes to your infrastructure carry some risk, so you may want to somehow restrict access to it. The example below is pretty extreme but it shows a very comprehensive policy where you restrict Spacelift access to users logging in from the office IP during business hours. You may want to use elements of this policy to create your own - less draconian - version, or keep it this way to support everyone's work-life balance.

Note that this example only defines deny rules so you'll likely want to add some allow and admin rules, too - either in this policy or in a separate one.

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

There's a lot to digest here, so a [playground example](https://play.openpolicyagent.org/p/4J3Nz6pYgC){: rel="nofollow"} may be helpful.

### Granting limited admin access

Very often you'd like to give a user admin access limited to a certain set of resources, so that they can manage them without having access to all other resources in that account. You can find more on that use case in [Spaces](../spaces/README.md).

### Rewriting teams

In addition to boolean rules regulating access to your Spacelift account, the login policy exposes the **team** rule, which allows one to dynamically rewrite the list of teams received from the identity provider. This operation allows one to define Spacelift roles independent of the identity provider. To illustrate this use case, let's imagine you want to define a `Superwriter` role for someone who's:

- logging in from an office VPN;
- is a member of the DevOps team, as defined by your IdP;
- is not a member of the Contractors team, as defined by your IdP;

```opa
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

What's important here is that the **team** rule overwrites the original list of teams, meaning that if it evaluates to a non-empty collection, it will **replace** the original list of teams in the session. In the above example, the `Superwriter` role will become the only team for the evaluated user session.

If the above is not what you want, and you still would like to retain the original list of teams, you can modify the above example the following way:

```opa
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

A playground example of the above is available [here](https://play.openpolicyagent.org/p/dM8P83sk4l){: rel="nofollow"}.

!!! hint
    Because the user session is updated, the rewritten teams are available in the data input provided to the policy types that receive user information. For example, the rewritten teams can be used in [Access policies](./stack-access-policy.md).

## Default login policy

If no login policies are defined on the account, Spacelift behaves as if it had this policy:

```opa
package spacelift

allow { input.session.member }
```
