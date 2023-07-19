# Admin / Owner

Users with **Owner** and **root Admin** roles have access to **Organization settings**. This means they can manage access for the rest of the collaborators within your Spacelift account. The following article details the configuration options and user invitation procedures available to them.

## Access settings

Access settings can be found by clicking the button in the lower-left corner with your avatar and selecting **Organization settings**.

## Select your Management Strategy

Account administrators can choose between User management and Login policy strategies in **Management strategy** tab. Once selected, the rules from the other strategy no longer apply.

!!! warning
    Strategy selection does not affect GitHub organization or [SSO](../../integrations/single-sign-on/README.md) admins and private account owners who always get admin access to their respective Spacelift accounts. This is to avoid a situation where a bad management strategy locks out everyone from the account.

!!! danger
    Changing your Management Strategy will invalidate all active sessions, except the session making the change.

## Users

The user list can be accessed by selecting **Users** tab in the left drawer.

The user list consists of all individuals who have or had access to your account through the User Management access strategy.

Below is a longer description of fields that we believe might not be obvious at first glance.

### Role

The displayed Role badge is different than the space access role. It describes the user's role within the organization, instead of specific space permissions. This badge can have one of three values:

- **OWNER** - account admin, SSO admin or GitHub organization being the owner of an account.
- **ADMIN** - a user who has direct admin permissions to **root** space. This badge does not take group or integration permissions into account.
- **USER** - users without admin permissions to **root** space.

### Space

The number of spaces that the user has direct permission to read (or more). Does not take Groups into account.

### Group

The number of groups that the user was a member of during the last login, as reported by the account's Identity Provider.

### Login method

Identity Provider that was used for authenticating given user. It will usually be the same as the account's current Identity Provider, but on a rare occasion that Identity Provider changes, this will allow for auditing old access or transferring permissions to users within the new Identity Provider.

### Status

- **QUEUED** - user invitation was issued and will be sent once Management Strategy is changed from Login Policy to User Management
- **PENDING** - user invitation was sent and can be accepted or the user still needs to confirm their ownership of the invitation email with a code found in the confirmation code email.
- **EXPIRED** - user invitation was sent, but the user did not accept it before it expired. A new invitation must be issued for a user to be able to access your Spacelift account.
- **ACTIVE** - user has accepted an invitation to your Spacelift account and has permissions set in User Management as long as User Management is the selected access strategy.
- **INACTIVE** - the user was previously able to access your Spacelift account, but Identity Provider changed and so this user needs to be invited again and login through the new Identity Provider to continue using Spacelift.

## Inviting new users

To invite new users to your account, click on the 'Invite user' button located in the top right corner. You will be able to send them an email invitation link and determine their access level during the invitation process.

### Resending user invitation

If a user did not receive an invitation email or their invitation has expired, you can select **Resend invite** from the three dots menu. Issuing a new invite is not possible if there already exists a pending or expired invite for a given email address.

### Revoking user invitation

At any time you can revoke a user invitation by choosing **Revoke invite** from the three dots menu. Once the invitation is revoked, it will no longer allow user access to your account. If you wish to invite a user with a given email at a later date, you can issue a new invitation.

## Managing user access

You can manage access rules for anyone who logs into your account by selecting the **Access details** option from the three dots menu.

### Slack integration

After setting up [Slack integration](../../integrations/chatops/slack.md), you can provide the user's Slack ID to give them the same permissions when interacting through Slack as they would have when interacting through the Spacelift website.

## IdP group mapping

Groups are reported by your Identity Provider for each user during authentication. You can add permissions to those groups that will be honored inside Spacelift. To do that, go to **IdP group mapping** tab and click **Map IdP group**. Then select appropriate Spaces and Roles the same way you would for a single User.

!!! warning
    Group permissions will only be applied to the user if the group name in Spacelift exactly matches the group name in your Identity Provider including capital letters and whitespaces.

### Slack integration

After setting up [Slack integration](../../integrations/chatops/slack.md) you can also grant permissions to entire Slack channels after selecting **Integrations** tab and clicking **Manage access** button in Slack card. You can input a human-readable name along the Slack channel ID. You can then add Space permissions the same way you would for Users and Groups.
