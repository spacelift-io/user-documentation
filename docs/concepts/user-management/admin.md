# Admin / Owner

Users with **Owner** and **root Admin** roles have access to **Organization settings**. This means they can manage access for the rest of the collaborators within your Spacelift account.

## Access control settings

Access control settings can be found by hovering over your name/avatar in the lower-left corner and selecting **Organization settings**.

## Select your management strategy

!!! danger
    Changing your Management strategy will invalidate all active sessions, except the session making the change.

Account administrators can choose between Identity access management and Login policy strategies in the **Management strategy** section. Once a strategy is enabled, the rules from the other no longer apply.

!!! warning
    Regardless of management strategy, GitHub organization or [SSO](../../integrations/single-sign-on/README.md) admins and private account owners always retain admin access to their respective Spacelift accounts. This is to avoid a situation where a bad management strategy locks out everyone from the account.

## Users

You can view a list of all users by clicking **Users** in the _Identity management_ section. The list includes all individuals who have (or had) access to your account through the Identity access management strategy.

The list displays:

- **Name**: The user's Spacelift username.
- **Method**: The identity provider used to authenticate the user. Generally matches the account's identity provider, but if the provider changes, this column helps audit outdated access or transfer permissions to users with the new identity provider.
- **Status**: The status of the user's account.
    - **QUEUED**: User invitation was issued and will be sent once the Management strategy is changed to User management.
    - **PENDING**: User invitation was sent and can be accepted.
    - **EXPIRED**: User invitation was sent, but the user did not accept it within 24h. A new invitation must be issued for a user to be able to access Spacelift.
    - **ACTIVE**: User has accepted an invitation to Spacelift and has permissions set in User management as long as User management is the selected access strategy.
    - **INACTIVE**: User was previously able to access Spacelift, but the identity provider for your account has changed. The user needs to be invited again and must login through the new identity provider to continue using Spacelift.
- **Last login**: The time and date of the user's last login.

You can also click the **three dots** at the end of each row to **See details**, **Manage roles**, or **Revoke access**.

### See details

The details drawer contains all the same information as in the users list. It also includes what user groups, if any, have been assigned to the user from IdP group mapping.

### Manage roles

Allows you to select a **Role** and a **Space** to grant the user specific permissions within Spacelift.

### Revoke access

Removes all access rules and permissions for the user.

## Inviting new users

To invite new users to your account, click **Invite user** in the top right corner. You will be able to send them an email invitation link and determine their access level [during the invitation process](../../getting-started/invite-teammates/README.md#add-single-users).

### Resending user invitation

If a user did not receive an invitation email or their invitation has expired, you can select **Resend invite** from the three dots menu. If a pending or expired invite for a given email address already exists, you cannot issue a new invite.

### Revoking user invitation

At any time you can revoke a user invitation by clicking the **three dots** in a user's row and choosing **Revoke invite**. Once the invitation is revoked, it will no longer allow user access to your account. If you wish to invite a user with a given email at a later date, you can issue a new invitation.

### Slack integration

After setting up the [Slack integration](../../integrations/chatops/slack.md), you can provide the user's Slack ID to give them the same permissions when interacting through Slack as they would have when interacting through the Spacelift website.

You can also grant permissions to entire Slack channels by navigating to _Integrate Services_ > _Integrations_, clicking **View** on the _Slack_ card, and clicking **Manage access**. You can input a human-readable name along the Slack channel ID. You can then add space permissions the same way you would for users and groups.

## IdP group mapping

Groups are reported by your identity provider for each user during authentication. You can add permissions to those groups that will be honored inside Spacelift. To do that, set up [IdP group mapping](./README.md#access-through-idp-group-mapping).

!!! warning
    Group permissions will only be applied to the user if the group name in Spacelift **exactly matches** the group name in your identity provider including capital letters and whitespaces.
