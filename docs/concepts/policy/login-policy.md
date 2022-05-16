# Login policy

## Purpose

Login policies can allow users to log in to the account, and optionally give them admin privileges, too. Unlike all other policy types, login policies are global and can't be attached to individual stacks. They take effect immediately once they're created and affect all future login attempts.

!!! warning
    Login policies don't affect GitHub organization or [SSO](../../integrations/single-sign-on.md) admins and private account owners who always get admin access to their respective Spacelift accounts. This is to avoid a situation where a bad login policy locks out everyone from the account.

!!! danger
    Any change made (create, update or delete) to a login policy will invalidate all active sessions, except the session making the change.

A login policy can define the following types of boolean rules:

* **allow** - allows the user to log in as a _non-admin_;
* **admin** - allows the user to log in as an _admin_ - note that you don't need to explicitly **allow** admin users;
* **deny** - denies login attempt, no matter the result of other (**allow** and **admin**) rules;
* **deny\_admin**:  denies the current user **admin** access to the stack, no matter the outcome of other rules;

If no rules match, the default action will be to deny a login attempt.

Note that giving folks admin access is a big thing. Admins can do pretty much everything in Spacelift - create and delete stacks, trigger runs or tasks, create, delete and attach contexts and policies, etc.

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
    "login": "string - username of the user trying to log in",
    "member": "boolean - is the user a member of the account",
    "name": "string - full name of the user trying to log in - may be empty",
    "teams": ["string - names of teams the user is a member of"]
  }
}
```

Two fields in the session object may require further explanation: _member_ and _teams_.

#### Account membership

When you first log in to Spacelift, we use GitHub as the identity provider and thus we're able to get some of your details from there with username (login) being the most important one. However, each Spacelift account is linked to one and only one GitHub account. Thus, when you log in to a Spacelift account, we're checking if you're a member of that GitHub account.

When that GitHub account is an organization, we can explicitly query for your organization membership. If you're a member, you get the member field set to _true_. If you're not - it's _false_. For private accounts it's different - they can only have one member, so the check is even simpler - if your login is the same as the name of the linked GitHub account, you get the member field set to _true_. If it isn't - it's _false_.

When using single sign-on with SAML, every successful login attempt will necessarily require that the _member_ field is set to _true -_ if the linked IdP could verify you, you **must** be a member.

!!! warning
    Watch this field very closely - it may be _very_ useful for your **deny** rules.

#### Teams

When using the default identity provider (GitHub), Teams are only queried for organization accounts - if you're a member of the GitHub organization linked to a Spacelift account, Spacelift will query GitHub API for the full list of teams you're a member of. This list will be available in the `session.teams` field. For private accounts and non-members, this list will be empty.

Note that Spacelift treats GitHub team membership as transitive - for example let's assume Charlie is a member of the _Badass_ team, which is a child of team _Awesome_. Charlie's list of teams includes both _Awesome_ and _Badass_, even though he's not a **direct** member of the team _Awesome_.

For single sign-on, the list of teams is pretty much arbitrary and depends on how the SAML assertion attribute is mapped to your user record on the IdP end. Please see the [relevant article](../../integrations/single-sign-on.md#setting-up-the-integration) for more details.

!!! warning
    Watch this field very closely - it may be _very_ useful for your **allow** and **admin** rules.

## Use cases

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

Here's a [minimal example to play with](https://play.openpolicyagent.org/p/LpzDekpDOU).

This is also important for single sign-on integrations: only the [integration creator](../../integrations/single-sign-on.md#setting-up-the-integration) gets administrative permissions by default, so all other administrators must be granted their access using a login policy.

### Granting access to external contributors

!!! danger
    This feature is not available when using [single sign-on](../../integrations/single-sign-on.md) - your identity provider **must** be able to successfully validate each user trying to log in to Spacelift.

Sometimes you have folks (short-term consultants, most likely) who are not members of your organization but need access to your Spacelift account - either as regular members or perhaps even as admins. There's also the situation where a bunch of friends is working on a hobby project in a personal GitHub account and they could use access to Spacelift. Here's an example of a policy that allows a bunch of whitelisted folks to get regular access and one to get admin privileges:

```opa
package spacelift

admins  := { "alice" }
allowed := { "bob", "charlie", "danny" }
login   := input.session.login

admin { admins[login] }
allow { allowed[login] }
deny  { not admins[login]; not allowed[login] }
```

Here's a [minimal example to play with](https://play.openpolicyagent.org/p/ZsOJayumFw).

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

There's a lot to digest here, so a [playground example](https://play.openpolicyagent.org/p/4J3Nz6pYgC) may be helpful.

### Rewriting teams

In addition to boolean rules regulating access to your Spacelift account, the login policy exposes the **team** rule, which allows one to dynamically rewrite the list of teams received from the identity provider. This operation allows one to define Spacelift roles independent of the identity provider. To illustrate this use case, let's imagine you want to define a _Superwriter_ role for someone who's:

* logging in from an office VPN;
* is a member of the DevOps team, as defined by your IdP;
* is not a member of the Contractors team, as defined by your IdP;

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

What's important here is that the **team** rule overwrites the original list of teams, meaning that if it evaluates to a non-empty collection, it will **replace** the original list of teams in the session. In the above example, the Superadmin role will become the only team for the evaluated user session.

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

A playground example of the above is available [here](https://play.openpolicyagent.org/p/dM8P83sk4l).

## Default login policy

If no login policies are defined on the account, Spacelift behaves as if it had this policy:

```opa
package spacelift

allow { input.session.member }
```
