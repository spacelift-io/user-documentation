# User Management

Spacelift is made for collaboration. In order to collaborate, you need collaborators. User Management is an easy way to invite new members to your organization and manage their permissions, together with third party integrations and group access. If you prefer to write a policy rather than using our UI, please check [Login Policy](../policy/login-policy.md).

!!! warning
    User Management doesn't affect GitHub organization or [SSO](../../integrations/single-sign-on/README.md) admins and private account owners who always get admin access to their respective Spacelift accounts. This is to avoid a situation where a mistake in User Management locks out everyone from the account.

## Roles

User Management works by setting one of the following roles for users, groups and integrations for selected [Spaces](../spaces/README.md).

- **Read** - cannot create or modify neither stacks nor any attachable entities, but can view them
- **Write** - an extension to Read, as it can actually trigger runs in the stacks it sees
- **Admin** - can create and modify stacks and attachable entities, as well as trigger runs

## User

Users are individuals invited through their email and authenticated using your account's Identity Provider. Users can have personal permissions assigned.

## Group

Group is a group of users as provided by your Identity Provider. If you assign permissions to a Group, all users that your Identity Provider reports as being member of given group will have the same access, unless user's permissions are higher than the ones they would get from being the member of a Group.

## Invitation process

New users can be invited through email by account admins and owners. Detailed instructions can be found in [Admin page](admin.md) of this documentation.

Once a user is invited, they will receive an email from Spacelift that will take them to your identity provider page.

![invitation email containing a button to accept invitation](<../../assets/screenshots/usermanagement/invitation_email.png>)

Once user authenticates with your identity provider, they will be redirected to a landing page that asks for confirmation code sent to their email.

![confirmation code landing page with input box for confirmation code](<../../assets/screenshots/usermanagement/confirmation_landing.png>)

Alternatively, instead of typing the code manually, user can click the button found in confirmation code email to confirm the email address ownership.

![confirmation code email with confirmation code and button to confirm email address ownership](<../../assets/screenshots/usermanagement/confirmation_email.png>)

## Migrating from Login Policy

If you were previously using [Login Policy](../policy/login-policy.md) you can invite users to User Management while still having Login Policy enabled. Once all users have accepted their invitations, you can switch to User Management as your desired strategy. Remember, that you can always go back if it turns out something was misconfigured.
