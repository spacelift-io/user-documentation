# Invite teammates to your Spacelift instance

You have two options for inviting people to your Spacelift account:

- Add [single users](#add-single-users).
- Add [users via policies](#add-users-via-policies).

!!! warning
    Granting access to individuals is more risky than granting access to only teams and account members. In the latter case, when an account member loses access to your organization, they automatically lose access to Spacelift. But when allowlisting individuals and _not_ restricting access to members only, you'll need to explicitly remove the individuals from your Spacelift login policy.

Before you go live with Spacelift, we recommend you use [login policies](../../concepts/policy/login-policy.md) and configure the [Single Sign-On (SSO) integration](../../integrations/single-sign-on/README.md), if applicable.

## Add single users

1. From the LaunchPad, click **Invite teammates**.
      - Alternatively, click your name in the bottom left, then **Organization settings**.
2. In the "Collaborate with your team" section:
      1. **Email**: Enter the email address of the user to add.
      2. **Role**: Select the user's role, admin or user.
      3. Click **Send invite**.

## Add users via policies

While we recommend using policies to implement [team-based access](../../concepts/policy/login-policy.md#teams) to Spacelift in most cases, you can add single users to get started.

![](<../../assets/screenshots/getting-started/invite-teammates/create-policy.png>)

1. Click your name in the bottom left, then **Organization settings**, then **Management strategy**.
2. Beside _login policy_, click **Enable**, then **Enable** again.
3. Click the _Login policy_ tab, then click **Create policy**.
4. **Name**: Enter a name for your policy. Choose a name that explains who or what the policy grants access to.
5. **Labels**: Organize policies by assigning labels to them.
6. Click **Continue**.
7. Fill in the policy code through one of these options:
      - Review the provided policy code and remove comments from pieces you want to use.
      - Copy and paste (and edit) one of the examples provided that matches the [identity provider](../../README.md#create-your-spacelift-account) you used to sign up for the Spacelift account.
8. Click **Create**.

### Policy examples

=== "GitHub"
    This example uses GitHub usernames to grant access to Spacelift.

    ```opa
    package spacelift

    admins  := { "alice" }
    allowed := { "bob", "charlie", "danny" }
    login   := input.session.login

    admin { admins[login] }
    allow { allowed[login] }
    deny  { not admin; not allow }
    ```
    !!! tip
        GitHub organization admins are automatically Spacelift admins. There is no need to grant them permissions in the Login policy.

=== "GitLab, Google, Microsoft"
    This example uses email addresses to grant access to Spacelift.

    ```rego
    package spacelift

    admins  := { "alice@example.com" }
    allowed := { "bob@example.com" }
    login   := input.session.login

    admin { admins[login] }
    allow { allowed[login] }
    # allow { endswith(input.session.login, "@example.com") } Alternatively, grant access to every user with an @example.com email address
    deny  { not admin; not allow }
    ```

Now your colleagues can access your Spacelift account as well.

✅ Step 4 of the LaunchPad is complete! Now you can explore and configure Spacelift as needed. Consider triggering your [first stack run](../../README.md#trigger-your-first-run), or creating a [policy](../../concepts/policy/README.md#creating-policies) or a [context](../../concepts/configuration/context.md#creating).

![LaunchPad Step 4 complete](<../../assets/screenshots/getting-started/invite-teammates/LaunchPad-step-4-complete.png>)
