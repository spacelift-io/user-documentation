---
description: Integrating Spacelift with your favorite messaging platform
---

# Slack

At Spacelift, we're using Slack for internal communication. And we know that other tech companies do the same, so we've created a first-class integration that we ourselves enjoy using.

Here are examples of messages the Spacelift application sends to Slack;

![](../assets/screenshots/CleanShot 2022-09-23 at 09.46.15.png)

![](../assets/screenshots/CleanShot 2022-09-23 at 09.52.06.png)

## Linking your Spacelift account to the Slack workspace

As a Spacelift and Slack admin, you can link your Spacelift account to the Slack workspace by going to the _Slack_ section of the _Settings_ screen.

The integration is an OAuth2 exchange which installs Slack Spacelift app in your workspace.

Once you install the Spacelift app, the account-level integration is finished and the _Slack_ section of the _Settings_ screen informs you that the two are talking to one another:

![](../assets/screenshots/Mouse_Highlight_Overlay_and_Slack_integration_·_spacelift-io.png)

Installing the Slack app doesn't automatically cause Spacelift to flood your Slack channels with torrents of notifications. These are set up on a per-stack basis using [Slack commands](slack.md#available-commands) and the management uses the Slack interface.

Though before that happens, you need to allow requests coming from Slack to access Spacelift stacks.

## Managing access to Stacks with policies

Our Slack integration allows users in the Slack workspace to interact with stacks by adding the ability
to change their run state or view changes that are planned or were applied.

Similar to regular requests to our HTTP APIs, requests and actions coming from Slack are subject to the policy-based access validation. If you haven't had a chance to review the [policy](../concepts/policy/README.md) and [Spaces](../concepts/spaces/README.md) documentation yet, please do it now before proceeding any further - you're risking a chance of getting lost.

### Available actions

Currently, we allow:

- Confirming and discarding tracked runs.
- Viewing planned and actual changes.

Both of these actions require specific permissions to be configured using the login or access policies.
Confirming or discarding runs requires _Write_ level permissions while viewing changes requires _Read_ level permissions. The documention sections about policies below describe how to setup and manage these permissions.

!!! info
    The default stack access and login policy decision for Slack requests is to deny all access.

### Login policy

Using [login policies](../concepts/policy/login-policy.md) is the preferred way to control access for the Slack interation. Using them you can control who can access stacks which are in a specific [Space](../concepts/spaces/README.md).

They allow for granular stack access control using the provided policy data such as slack workspace details, Slack team information and user which interacted with the message data. Using the Login policy you can define rules which
would allow to have _Read_ or _Write_ level permissions for certain actions.

Login policies also don't need to be attached to a specific stack in order to work but are instead
evaluated during every stack mutation or read attempt from the integration.

!!! warning
    It's important to know that if you have multiple login policies, failing to evaluate one of them or
    having at least one of them result in a deny decision after the evaluation is done, will result in the
    overal decision being a `deny all`.

Here is an example of data which the login policy receives when evaluating stack access for the integration:

```json
{
  "request": {
    "timestamp_ns": "<int> - a unix timestamp for when this request happened"
  },
  "slack": {
    "channel": {
      "id": "<string> - a channel ID, example: C042YPN0000",
      "name": "<string> - a channel name, example: spc-finished"
    },
    "command": "<string>",
    "team": {
      "id": "<string> - a team ID for which this user belongs, example: T0431750000",
      "name": "<string> - a team name represented as string, example: slack-workspace-name"
    },
    "user": {
      "deleted": "<boolean>",
      "display_name": "<string>",
      "enterprise": {
        "enterprise_id": "<string>",
        "enterprise_name": "<string>",
        "id": "<string>",
        "is_admin": "<boolean>",
        "is_owner": "<boolean>",
      },
      "teams": {
         "id": "<string>",
         "name": "<string>"
      },
      "id": "<string> - a user which initially request ID, example: C042YPN1111",
      "is_admin": "<boolean> - is the user an admin",
      "is_owner": "<boolean> - is the workspace owner",
      "is_primary_owner": "<boolean>",
      "is_restricted": "<boolean>",
      "is_stranger": "<boolean>",
      "is_ultra_restricted": "<boolean>",
      "has_2fa": "<boolean>"
      "real_name": "<string>",
      "tz": "<string>"
    }
  },
  "spaces": [{
    "id": "<string> - an ID for a Space in spacelift",
    "labels": "<stringArray> - a list of labels attached to this space",
    "name": "<string> - name for a Space in spacelift"
  }, {
    "id": "<string>",
    "labels": "<stringArray>",
    "name": "<string>"
  }]
}
```

!!! info
    The `slack` object in the policy input data is built using Slack provided data. See [their official documentation](https://api.slack.com/types/user){: rel="nofollow"} for always up-to-date and full explanation of the `slack` object fields.
  
Using the above data we can write policies which only allow for a specific user or slack team to access specific spaces in which your stacks reside.

For example here is a policy which would allow anyone from a specific slack team to alter stacks in a particular space:

```opa
package spacelift

# Allow access for anyone in team X
allow {
  input.slack.team.id == "X"
}

# Deny access for everyone except team X
deny {
  input.slack.team.id != ""
  input.slack.team.id != "X"
}

# Grant write access to stacks in Space Y for anyone in team X
space_write["Y"] {
  input.slack.team.id == "X"
}
```

### Access policy

!!! warning
    It's recommended to instead use the [login policies](../concepts/policy/login-policy.md) in order to
    manage slack access as [stack access policies](../concepts/policy/stack-access-policy.md) are **deprecated**.

In this case, we're using [stack access policies](../concepts/policy/stack-access-policy.md).
Unlike HTTP requests, policy inputs representing Slack interactions replace `"request"` and `"session"` sections with a single `"slack"` section, containing the following payload:

```json
{
  "command": "<string> - command received, if any",
  "user": {
    "id": "<string> - Slack user ID who generated the request",
    "deleted": "<bool> - is the user deleted",
    "display_name": "<string> - user display name",
    "has_2fa": "<bool> - does the user has 2FA enabled",
    "is_admin": "<bool> - is the user a workspace admin",
    "is_owner": "<bool> - is the user a workspace owner",
    "is_primary_owner": "<bool> - is the Slack user a workspace primary owner",
    "is_restricted": "<bool> - is this a guest user",
    "is_ultra_restricted": "<bool> - is this a single-channel guest",
    "is_stranger": "<bool> - does the belong to a different workspace",
    "real_name": "<string> - user real name",
    "tz": "<string> - user timezone",
    "enterprise": {
      "id": "<string> - Slack enterprise user ID, may be different from user.id",
      "enterprise_id": "<string> - unique ID for the Enterprise Grid organization this user belongs to",
      "enterprise_name": "<string> - display name for the Enterprise Grid organization",
      "is_admin": "<bool> - is the user user an Admin of the Enterprise Grid organization",
      "is_owner": "<bool> - is the user user an Owner of the Enterprise Grid organization",
      "teams": "<list<string> - an array of workspace IDs that are in the Enterprise Grid organization"
    }
  },
  "team": {
    "id": "<string> ID of the Slack team that generated the request",
    "name": "<string> Name of the Slack team"
  },
  "channel": {
    "id": "<string> ID of the Slack channel that generated the request",
    "name": "<string> Name of the Slack channel"
  }
}
```

!!! info
    For the most up-to-date explanation of Slack user intricacies, please always refer to [Slack's own documentation](https://api.slack.com/types/user){: rel="nofollow"}.

As you can see, that's quite a bit of data you can base your decisions on. For example, you can map some Slack channels as having certain level of access to certain Stacks - just make sure to keep these Slack channels private / invite-only. Here's an example stack access policy allowing Write level of access to requests coming from Slack's _#dev-notifications_ channel:

![](../assets/screenshots/Manage_stacks_from__dev-notifications_·_spacelift-io.png)

Any Stack with this policy attached will be accessible for writing from this Slack channel - but no other!

!!! info
    Note that different commands may have different required levels of access, so you can create more granular policies - for example giving a `#devops` channel _Write_ access, while giving only _Read_ access to various "notifications" channels.

## Available slash commands

!!! warning
    It's recommended to instead use the [notification policy](../concepts/policy/notification-policy.md) in order to
    manage slack messages received from Spacelift. These slash commands are **deprecated**.

Three slash commands are currently available:

- `/spacelift subscribe $stackId` - subscribes a particular Slack channel to run state changes for a given Stack - requires ;
- `/spacelift unsubscribe $stackId` - unsubscribes a particular Slack channel from run state changes for a given Stack;
- `/spacelift trigger $stackId` - triggers a tracked run for the specified Stack;
