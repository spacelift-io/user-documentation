# User management

Spacelift is made for collaboration. In order to collaborate, you need collaborators. User Management is an easy way to invite new members to your organization and manage their permissions, together with third-party integrations and group access. If you prefer to write a policy rather than using our UI, please check out [Login Policies](../policy/login-policy.md).

!!! warning
    User Management doesn't affect GitHub organization or [SSO](../../integrations/single-sign-on/README.md) admins and private account owners who always get admin access to their respective Spacelift accounts. This is to avoid a situation where a mistake in User Management locks out everyone from the account.

## User

Users are individuals invited through their email and authenticated using your account's Identity Provider. Users can have personal permissions assigned.

## IdP group mapping

Group is a group of users as provided by your Identity Provider. If you assign permissions to a Group, all users that your Identity Provider reports as being members of a given group will have the same access, unless the user's permissions are higher than the ones they would get from being a member of a Group.

## Roles in User Management

User Management leverages Spacelift's [RBAC system](../authorization/rbac-system.md) to assign roles to users, groups for selected [Spaces](../spaces/README.md).

## Invitation process

New users can be invited through email by account admins and owners. Detailed instructions can be found
on [the Admin page](admin.md).

Once a user is invited, they will receive an email from Spacelift that will take them to your identity provider page.

![invitation email containing a button to accept the invitation](<../../assets/screenshots/user-management/invitation-email.png>)

Once the user authenticates with your identity provider, they will be redirected to the application.

## Migrating from Login Policy

If you were previously using [Login Policy](../policy/login-policy.md) you can queue invites to User Management for your users while still having Login Policy enabled. Once you switch to the User Management strategy, the invites will be sent to your users' emails and allow them to sign in through your Identity Provider. Remember, that you can always go back if it turns out something was misconfigured.

## Related topics

- **[Authorization & RBAC](../authorization/README.md)**: Complete guide to Spacelift's authorization system
- **[Assigning Roles to Users](../authorization/assigning-roles-users.md)**: Detailed role assignment guide
- **[Assigning Roles to Groups](../authorization/assigning-roles-groups.md)**: Team-based permission management
