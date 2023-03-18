---
description: Receiving Spacelift notifications using webhooks
---

# Webhooks

Spacelift can be configured to send webhook notifications for various events to an HTTP endpoint of your choice.

## Setting up webhooks

Webhooks can be set up by Spacelift administrators. They can be easily created or modified in the `Webhooks` section.

### Navigate to the webhooks section

![](<../assets/screenshots/named-hooks-nav.png>)

### Fill required fields

![](<../assets/screenshots/named-hooks1.png>)

!!! info
    The `Secret` parameter is optional and is used to validate the received payload.
    You can learn more about it in the [validating payload](webhooks.md#validating-payload) section.

### Reference webhooks in policy rules

Webhook messages are delivered using the [notification policy](../concepts/policy/notification-policy.md).
When defining rules, the policy expects you to reference the webhook by its `ID` which you
can copy from the webhook list view:

![](<../assets/screenshots/named-hooks2.png>)

### Exploring deliveries

Webhook deliveries and their response statuses are stored and can be explored by selecting a specific webhook
and viewing its details. You'll be presented with a list of deliveries, their status codes and when they happened.
You can also click on each delivery to view more details about it:

![](<../assets/screenshots/named-hooks3.png>)

## Default webhook payloads

The following section documents the default webhook payloads sent for each event type. However, if required, webhook payloads can be customized via a [notification policy](../concepts/policy/notification-policy.md).

### Run events

Here's an example of the default webhook payload for a notification about a finished tracked run:

```json
{
    "account": "spacelift-io",
    "state": "FINISHED",
    "stateVersion": 4,
    "timestamp": 1596979684,
    "run": {
        "id": "01EF9PFPNFFM2MQXTJKHK1B869",
        "branch": "master",
        "commit": {
            "authorLogin": "marcinwyszynski",
            "authorName": "Marcin Wyszynski",
            "hash": "0ee3a3b7266daf5a1d44a193a0f48ce995fa75eb",
            "message": "Update demo.tf",
            "timestamp": 1596705932,
            "url": "https://github.com/spacelift-io/demo/commit/0ee3a3b7266daf5a1d44a193a0f48ce995fa75eb"
        },
        "createdAt": 1596979665,
        "delta": {
            "added": 0,
            "changed": 0,
            "deleted": 0,
            "resources": 1
        },
        "triggeredBy": "marcinw@spacelift.io",
        "type": "TRACKED"
    },
    "stack": {
        "id": "spacelift-demo",
        "name": "Spacelift demo",
        "description": "",
        "labels": []
    }
}
```

The payload consists of a few fields:

- `account` is the name (subdomain) of the account generating the webhook - useful in case you're pointing webhooks from various accounts at the same endpoint;
- `state` is a string representation of the run state at the time of the notification being triggered;
- `stateVersion` is the ordinal number of the state, which can be used to ensure that notifications that may be sent or received out-of-order are correctly processed;
- `timestamp` is the unix timestamp of the state transition;
- `run` contains information about the run, its associated commit and delta (if any);
- `stack` contains some basic information about the parent [Stack](../concepts/stack/README.md) of the `run`;

### Internal error events

```json
{
  "title": "Invalid Stack Slug Triggered",
  "body": "policy tried to trigger Stack 'this-is-not-a-stack' which either doesn't exist or this policy doesn't have access to",
  "error": "policy triggered for Stack that doesn't exist",
  "severity": "ERROR",
  "account": "spacelift-io"
}
```

Internal errors will always have the same fields set and some of them will be static for an event:

- `title` is the title (summary) of the error.
- `body` is the is the full explanation of what went wrong.
- `error` is a description of the error that happened.
- `severity` can be one of three different constants: `INFO`, `WARNING`, `ERROR`.
- `account` is the account for which the error happened.

## Validating payload

In order to validate the incoming payload, you will need to have the secret handy - the one you've generated yourself when creating or updating the webhook.

Every webhook payload comes with two signature headers generated from the combination of the secret and payload. `X-Signature` header contains the SHA1 hash of the payload, while `X-Signature-256` contains the SHA256 hash. We're using the exact same mechanism as GitHub to generate signatures, please refer to [GitHub docs](https://docs.github.com/en/developers/webhooks-and-events/webhooks/securing-your-webhooks#validating-payloads-from-github){: rel="nofollow"} for details.

## Attaching webhooks to stacks

!!! warning
    We recommend that you use [notification policies](../concepts/policy/notification-policy.md) to
    route stack events to your webhooks. Stack webhook integrations are provided for backwards compatibility.

Webhooks can be set up by Spacelift administrators on per-stack basis. In order to do that, navigate to the _Integrations_ section of the stack settings view. From the list of available integrations, select the _Add webhook_ option:

![](../assets/screenshots/Mouse_Highlight_Overlay_and_Edit_stack_·_Spacelift_demo.png)

!!! info
    You can set up as many webhooks for a Stack as you need, though each one _must_ have a unique endpoint.

You will be presented with a simple setup form that requires you to provide and endpoint to which the payload is sent, and an _optional_ secret that you can use to [validate](webhooks.md#validating-payload) that the incoming requests are indeed coming from Spacelift:

![](<../assets/screenshots/Mouse_Highlight_Overlay_and_Edit_stack_·_Spacelift_demo (1).png>)

Please note that it's up to you to come up with a reasonably non-obvious secret.

Once saved, the webhook will appear on the list of integrations:

![](../assets/screenshots/Mouse_Highlight_Overlay.png)

!!! info
    Unlike some other secrets in Spacelift, the webhook secret can be viewed by anyone with read access to the stack. If you suspect foul play, consider regenerating your secret.

By default webhooks are enabled which means that they are triggered every time there's a run state change event on the Stack they are attached to. If you want to temporarily disable some of the endpoints, you can do that without having to delete the whole integration.

To do that, just click on the Edit button on the desired webhook integration section:

![](<../assets/screenshots/Mouse_Highlight_Overlay (1).png>)

...and click on the Enabled toggle to see it going _gray_:

![](<../assets/screenshots/Mouse_Highlight_Overlay (2).png>)

Reversing this action is equally simple - just follow the same steps making sure that the toggle goes _green_:

![](<../assets/screenshots/Mouse_Highlight_Overlay (3).png>)
