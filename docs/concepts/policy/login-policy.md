# Login policy

## Purpose

<p align="center"><strong>Do not use import modules, such as import rego.v1. Instead, you must write policies using standard Rego syntax. <br>
  The Open Policy Agent (OPA) will then read and evaluate these policies to make decisions.</strong></p>

Login policies dictate who can access a Spacelift account, how access is granted, and the extent of this access (which might include admin privileges). Login policies take effect immediately and impact subsequent login attempts. Unlike other policy types, login policies are global; you cannot attach them to individual stacks. 

API keys, similar to virtual users, function according to login policies unless you create them in the "root" space with an admin key.

Login policies **do not apply** to:
* GitHub organizations or [SSO](../../integrations/single-sign-on/README.md) admins
*	Private account owners
    * Private account owners have admin access to their respective Spacelift accounts. Admin access prevents an all-user account lockout if, for example, there is a poorly written policy.

!!! warning
    When you create, update, or delete a login policy, all active sessions are logged out with the exception of the session where you initiated the create/update/delete changes.

A login policy can define the true-false, allow-deny (Boolean) rules:

- **allow** – permits the user to log in as a _non-admin_.
- **admin** – allows the user to log in as an _account-wide admin_; you do not need to explicitly **allow** admin users.
- **deny** – prevents login access despite the result of other (**allow** and **admin**) rules.
- **deny_admin** – denies the current user **admin** access to the stack despite the outcome of other rules.
- **space_admin/space_write/space_read** – manages access levels to _spaces_. For additional information, read: [Spaces – Access Control](../spaces/access-control.md).

If there is not a policy that applies to a particular login action, the system denies login access by default.

Granting admin rights is a significant decision, as these users will have full control in Spacelift. They will be able to perform a range of tasks to include creating and deleting stacks, triggering runs or tasks, and creating, deleting, and attaching contexts and policies. If this control is not necessary, consider applying the **space_admin** rule because it provides a more limited and restricted admin access.

!!! danger
    When you define an **allow** or **admin** rule, consider adding a **deny** rule to restrict access where necessary. For additional information, read: **Examples** (below)

## Data Input

Spacelift collects data during each login attempt. This data includes:
* The user’s IP address and login attempt time.
* User information, such as the username and any associated team or group name.
* The user who created the session and from what location.
* Account _spaces_ and their descriptions.

Below is the data input schema that each policy request receives:


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

Open Policy Agent (OPA) is the engine that reads or evaluates policies to make yes/no (allow/deny) decisions. Without OPA, this evaluation cannot occur. OPA string comparisons are case-sensitive, requiring that you use the exact case that your identity provider (GitHub, for example) defines when comparing these values. For guidance, access [Sampling Policy Inputs](./README.md#sampling-policy-inputs) to view the exact values that the identity provider (IdP) passes.

Two fields in the _session object_, data passed to a login policy, may require further explanation: _member_ and _team_.

### Account Membership

When you initially log in to Spacelift, our team uses GitHub as your IdP – retrieving details such as your login username. Each Spacelift account is linked to one specific GitHub account. During log in, Spacelift checks to determine if you are a member of that linked GitHub account.

**GitHub Organization Account**
* Spacelift checks to determine if you are a member of that GitHub org.
* If yes, member: true
* If no, member: false

**Private GitHub Account**
* These accounts can only have one member.
* If your GitHub username matches the account name,  member: true
* If no match, member: false

**Security Assertion Markup Language (SAML)/SSO**
* If you are using SAML SSO, a successful log in indicates that the IdP verified the user.
* **member** is always true when valid login credentials entered.

The **member** field helps Spacelift determine account access, based on login policies. 

**This field can be extremely useful for your _deny_ rules.**

#### Teams

Teams are only queried for organization accounts when using the default GitHub IdP.  If you are a member of the GitHub organization linked to a Spacelift account, Spacelift will query the GitHub API for the full list of teams that include you as a member. This list will be available in the **session.teams** field. For private accounts and non-members, this list will be empty.

Spacelift treats GitHub team membership as transitive such that a _child_ team is part of a _parent_ team. For example, Charlie is a member of team _Brother_, which is a child of team _Family_. Charlie's list of teams includes both _Brother_ and _Family_, even though he is not a direct member of team _Family_.

For SSO, the list of teams is arbitrary and depends on how the SAML assertion attribute is mapped to your user record specific to the IdP. For additional information, read [SAML Setup Guides](../../integrations/single-sign-on/README.md#setting-up-the-integration).

**The _team_ field can be extremely useful for your _allow_ and _admin_ rules.**

## Examples

Our team maintains a [library of example policies](https://github.com/spacelift-io/spacelift-policies-example-library/tree/main/examples/login){: rel="nofollow"} that you can use _as-is_ or customize to meet your needs. If you cannot find what you need below or in the library, contact [Support](../../product/support/README.md#contact-support). This team will create a policy per your specifications. 

!!! tip
    We recommend a single login policy, as combining policies can yield unexpected results when you merge their decisions.

Below are use cases for login policies:
1. Managing access levels within an organization
1. Granting access to unauthorized org users
1. Restricting access to specific circumstances
1. Granting limited admin access
1. Rewriting teams

Let's review each use case.

### Managing Access Levels within an Organization

In high-security environments where the principle of least access is applied, it is possible that no one on the Infrastructure team gets admin access to GitHub. Still, it would be useful for these team members to oversee your Spacelift account. Let's create a login policy that grants **admin access** to the DevOps team, allows **regular access** for the Engineering team, and **denies access** to anyone who is not a member of this Spacelift account. We will give these non-members more granular access to individual stacks later using [Stack Access Policies](stack-access-policy.md). 

```opa
package spacelift

teams := input.session.teams

# Make sure to use the GitHub team names, not IDs (e.g., "Example Team" not "example-team")
# and to omit the GitHub organization name
admin { teams[_] == "DevOps" }
allow { teams[_] == "Engineering" }
deny  { not input.session.member }
```

You can experiment with this [example](https://play.openpolicyagent.org/p/LpzDekpDOU){: rel="nofollow"}.

Managing access levels within an organization is also important for SSO integrations. Only the [integration creator](../../integrations/single-sign-on/README.md#setting-up-the-integration) gets administrative permissions by default. All other administrators must be granted their access using a login policy.

### Granting Access to Unauthorized Org Users

**This feature is not available when using [SSO](../../integrations/single-sign-on/README.md). Your IdP _must_ be able to successfully validate each user trying to log in to Spacelift.**

On occasion, you might need to grant Spacelift account access to people who are not part of your GitHub organization, such as short-term consultants. These users might need **regular access** or even **admin access**. Similarly, you might have friends working on a hobby project in a personal GitHub account that could benefit from Spacelift access.

Below are example policies:
* One that **whitelists specific users** for **regular access**.
* One that gives **admin access** to a single user.

=== "GitHub"

This example uses GitHub usernames to grant access to Spacelift. More specifically, this example grants **admin access** to _alice_, **regular access** to _bob_, _charlie_, and _danny_, and denies access to all others.

    ```opa
    package spacelift

    admins  := { "alice" }
    allowed := { "bob", "charlie", "danny" }
    login   := input.session.login

    admin { admins[login] }
    allow { allowed[login] }
    deny  { not admins[login]; not allowed[login] }
    ```
You can experiment with this [example](https://play.openpolicyagent.org/p/ZsOJayumFw){: rel="nofollow"}.

=== "Google"

This example uses email addresses that Google manages to grant access to Spacelift.

    ```rego
    package spacelift

    admins  := { "alice@example.com" }
    login   := input.session.login

    admin { admins[login] }
    allow { endswith(input.session.login, "@example.com") }
    deny  { not admins[login]; not allow }
    ```

!!! warning
    Granting access to individuals is less secure than both granting access to teams _and_ restricting access to account members. In the latter case, when they lose access to your GitHub org, they automatically lose access to Spacelift. However, if you whitelist individuals and do not restrict access to members, you must remove them from your Spacelift login policy when their access changes.

### Restricting Access to Specific Circumstances

Stable and secure infrastructure is crucial to your business continuity. Changes to your infrastructure carry some risks, so you may want to  restrict access to it. The example below is extreme, but it shows a comprehensive policy where you restrict Spacelift access to users logging in from the office IP solely to business hours. This example policy denies login access on weekends, before 9:00AM or after 5:00PM PT/LA, and if the user’s IP address is not within a specific range (which is specific to the office location). You may want to use elements of this policy to create your own version, or you might prefer to maintain this policy to support everyone's work-life balance.

This example only defines the **deny** rule. You might want to add **allow** and **admin** rules, either in this policy or in a separate one.


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

The [playground example](https://play.openpolicyagent.org/p/4J3Nz6pYgC){: rel="nofollow"} might be helpful.

### Granting Limited Admin Access

You might need to grant users admin access that is limited to specific resources, allowing them to manage only those resources and nothing else in the account. For additional information, read: [Spaces](../spaces/README.md).

### Rewriting Teams

In addition to Boolean rules regulating access to your Spacelift account, the login policy exposes the **team** rule. This rule allows you to dynamically rewrite the list of teams received from the IdP. This operation allows you to define Spacelift roles independent of the IdP. To demonstrate this use case, imagine you want to define a Superwriter role that meets this criteria:

* User logs in from an office VPN.
* User is a member of the DevOps team, as defined by your IdP.
* User is not a member of the Contractors team, as defined by your IdP.


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

The **team** rule overwrites the original list of teams. If it evaluates to a non-empty collection, it will **replace** the original list of teams in the session. In the above example, the Superwriter role will become the only team for the evaluated user session.

If you do not prefer the above example but, instead, want to retain the original list of teams, you can modify the above example as follows:


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

Since the user session is updated, the modified team list is included in the input data for any policy that uses user information.
For example, [Access Policies](./stack-access-policy.md) can use these updated team values.

## Default Login Policy

If the account does not have any defined login policies, the system will allow access to account members:

```opa
package spacelift

allow { input.session.member }
```
