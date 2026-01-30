# Invite teammates to your Spacelift instance

You have a few options for inviting people to your Spacelift account:

- Add [single users](#add-single-users).
- Add [users via policies](#add-users-via-policies).
- Add groups with [IdP group mapping](../../concepts/authorization/assigning-roles-groups.md#idp-group-role-bindings).

!!! warning
    Granting access to individuals is more risky than granting access to only teams and account members. In the latter case, when an account member loses access to your organization, they automatically lose access to Spacelift. But when allowlisting individuals and _not_ restricting access to members only, you'll need to explicitly remove the individuals from your Spacelift login policy.

## Add single users

1. From the LaunchPad, click **Invite teammates**.
      - Alternatively, click your name in the bottom left, then **Organization settings**.
2. In the _Identity Management > Users_ section, click Invite user.
3. Fill in the user details:
      1. **Username** (optional): Enter the username for the new user, if different than email.
      2. **Email**: Enter the email address of the new user.
      3. **Slack member ID** (optional): Enter the user's Slack member ID to allow them to [interact with Spacelift via Slack](../../concepts/user-management/admin.md#slack-integration).
      4. **Role**: Select the [user's role(s)](../../concepts/authorization/rbac-system.md) from _space reader_, _space writer_, _space admin_, or _worker pool controller_.
      5. **Space**: Select the space the user will have access to. You can assign multiple Roles and Spaces with the **Add** button.
4. Click **Invite**.

## Add users via policies

![Create login policy](<../../assets/screenshots/getting-started/invite-teammates/create-policy.png>)

1. Click your name in the bottom left, then **Organization settings**, then **Management strategy**.
2. Beside _login policy_, click **Enable**, then **Enable** in the pop-up window.
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

    === "Rego v1"
        ```opa
        package spacelift

        admins  := { "alice" }
        allowed := { "bob", "charlie", "danny" }
        login   := input.session.login

        admin if admins[login]
        allow if allowed[login]
        deny if { not admin; not allow }
        ```

    === "Rego v0"
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

    === "Rego v1"
        ```rego
        package spacelift

        admins := {"alice@example.com"}
        allowed := {"bob@example.com"}
        login := input.session.login

        admin if admins[login]
        allow if allowed[login]
        # allow if endswith(input.session.login, "@example.com") Alternatively, grant access to every user with an @example.com email address
        deny if { not admin; not allow }
        ```

    === "Rego v0"
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

✅ Step 4 of the LaunchPad is complete! Now you can explore and configure Spacelift as needed. Consider triggering your [first stack run](../../README.md#trigger-your-first-run), or creating a [policy](../../concepts/policy/README.md#creating-policies) or a [context](../../concepts/configuration/context.md#creating-a-context).

![LaunchPad Step 4 complete](<../../assets/screenshots/getting-started/invite-teammates/LaunchPad-step-4-complete.png>)
