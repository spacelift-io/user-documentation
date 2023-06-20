# Admin / Owner

Users with **Owner** and **root Admin** roles have access to **Organization settings**. This means they can manage access for the rest of collaborators within your Spacelift account. The following article details the configuration options and user invitation procedures available to them.

## Access settings

Access settings can be found by clicking the button in the lower-left corner with your avatar and selecting **Organization settings**.

## Select your Management Strategy

Account administrator can choose between User management and Login policy strategies in **Management strategy** tab. Once selected, the rules from the other strategy no longer apply.

!!! warning
    Strategy selection does not affect GitHub organization or [SSO](../../integrations/single-sign-on/README.md) admins and private account owners who always get admin access to their respective Spacelift accounts. This is to avoid a situation where a bad management strategy locks out everyone from the account.

## Users

User list can be accessed by selecting **Users** tab in left drawer.

The user list consists of all individuals who have or had access to your account through User Management access strategy.

Below is a longer description of fields that we believe might not be obvious at first glance.

### Role

Displayed Role badge is different than space access role. It describes user's role within the organization, instead of specific space permissions. This badge can have one of three values:

- **OWNER** - account admin, SSO admin or GitHub organization being the owner of given account.
- **ADMIN** - user who has direct admin permissions to **root** space. This badge does not take group or integration permissions into account.
- **USER** - users without admin permissions to **root** space.

### Space

Number of spaces that user has direct permissions to. Does not take Groups into account.

### Group

Number of groups that user was the member of during last login, as reported by account's Identity Provider.

### Login method

Identity Provider that was used for authenticating given user. It will usually be the same as account's current Identity Provider, but in a rare occasion that Identity Provider changes, this will allow for auditing old access or transferring permissions to users within new Identity Provider.

### Status

- **PENDING** - user invitation was sent and can be accepted or user still needs to confirm their ownership of invitation email with a code found in confirmation code email.
- **EXPIRED** - user invitation was sent, but user did not accept it before it expired. New invitation must be issued for user to be able to access your Spacelift account.
- **ACTIVE** - user has accepted invitation to your Spacelift account and has permissions set in User Management as long as User Management is the selected access strategy.
- **INACTIVE** - user was previously able to access your Spacelift account, but Identity Provider changed and so this user needs to be invited again and login through new Identity Provider in order to continue using Spacelift.

## Inviting new users

To invite new users to your account, click on the 'Invite user' button located in the top right corner. You will be able to send them an email invitation link and determine their access level during the invitation process.

### Resending user invitation

If user did not receive invitation email or their invitation has expired, you can select **Resend invite** from the three dots menu. Issuing new invite is not possible if there already exists a pending or expired invite for given email address.

### Revoking user invitation

At any time you can revoke user invitation by choosing **Revoke invite** from the three dots menu. Once the invitation is revoked, it will no longer allow user access to your account. If you wish to invite user with given email at a later date, you can issue new invitation.

## Managing user access

You can manage access rules for anyone who logs into your account by selecting the **Access details** option from the three dots menu.

### Slack integration

After setting up [Slack integration](../../integrations/chatops/slack.md), you can provide user's Slack ID to give them the same permissions when interacting through Slack as they would have when interacting through Spacelift website.

## Groups

Groups are reported by your Identity Provider for each user during authentication. You can add permissions to those groups that will be honored inside Spacelift. In order to do that, go to **Groups** tab and click **Add Group access**. Then select appropriate Spaces and Roles the same way you would for a single User.

!!! warning
    Group permissions will only be applied to user if group name in Spacelift exactly matches group name in your Identity Provider including capital letters and whitespaces.

### Slack integration

After setting up [Slack integration](../../integrations/chatops/slack.md) you can also grant permissions to entire Slack channels after selecting **Integrations** tab and clicking **Create integration** button in the top-right corner. You can input a human-readable name along the Slack channel ID. You can then add Space permissions the same way you would for Users and Groups.
