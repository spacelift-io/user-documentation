# User Management

Spacelift is made for collaboration. In order to collaborate, you need collaborators. User Management is an easy way to invite new members to your organization and manage their permissions, together with third-party integrations and group access. If you prefer to write a policy rather than using our UI, please check out [Login Policies](../policy/login-policy.md).

!!! warning
    User Management doesn't affect GitHub organization or [SSO](../../integrations/single-sign-on/README.md) admins and private account owners who always get admin access to their respective Spacelift accounts. This is to avoid a situation where a mistake in User Management locks out everyone from the account.

## Roles

User Management works by setting one of the following roles for users, groups and [integrations](../user-management/admin.md#slack-integration) for selected [Spaces](../spaces/README.md).

- **Read** - cannot create or modify stacks or any attachable entities, but can view them
- **Write** - can perform actions like triggering runs, but cannot create or modify Spacelift resources
- **Admin** - can create and modify stacks and attachable entities, as well as trigger runs

## User

Users are individuals invited through their email and authenticated using your account's Identity Provider. Users can have personal permissions assigned.

## IdP group mapping

Group is a group of users as provided by your Identity Provider. If you assign permissions to a Group, all users that your Identity Provider reports as being members of a given group will have the same access, unless the user's permissions are higher than the ones they would get from being a member of a Group.

## Invitation process

New users can be invited through email by account admins and owners. Detailed instructions can be found on [the Admin page](admin.md) of this documentation.

Once a user is invited, they will receive an email from Spacelift that will take them to your identity provider page.

![invitation email containing a button to accept the invitation](<../../assets/screenshots/user-management/invitation-email.png>)

Once the user authenticates with your identity provider, they will be redirected to a landing page that asks for a confirmation code sent to their email.

![confirmation code landing page with an input box for confirmation code](<../../assets/screenshots/user-management/confirmation-landing.png>)

Alternatively, instead of typing the code manually, the user can click the button found in the confirmation code email to confirm the email address ownership.

![confirmation code email with confirmation code and button to confirm email address ownership](<../../assets/screenshots/user-management/confirmation-email.png>)

## Migrating from Login Policy

If you were previously using [Login Policy](../policy/login-policy.md) you can queue invites to User Management for your users while still having Login Policy enabled. Once you switch to the User Management strategy, the invites will be sent to your users' emails and allow them to sign in through your Identity Provider. Remember, that you can always go back if it turns out something was misconfigured.
