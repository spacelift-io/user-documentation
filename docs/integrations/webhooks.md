---
description: Receiving Spacelift notifications using webhooks
---

# Webhooks

{% if is_saas() %}
!!! Info
    This feature is only available to paid Spacelift accounts. Please check out our [pricing page](https://spacelift.io/pricing){: rel="nofollow"} for more information.
{% endif %}

Spacelift can be configured to send webhook notifications for various events to an HTTP endpoint of your choice.

## Set up webhooks

Webhooks can be created or modified by Spacelift administrators in the _Webhooks_ section of the _Integrations_ page.

![Webhooks section of integrations page](<../assets/screenshots/integrations/webhooks-section.png>)

### Fill required fields

![Create a new webhook](<../assets/screenshots/named-hooks1.png>)

1. On the _Webhooks_ section of the _Integrations_ page, click **View**.
2. Click **Create webhook**.
3. Fill in the webhook details:
      1. **Name**: Enter a name for the webhook integration.
      2. **Endpoint URL**: Enter the endpoint URL the webhook will send information to.
      3. **Space**: Select the space that can access the webhook.
      4. **Secret** (optional): Enter the secret, if needed, to [validate the received payload](#validate-payload).
      5. **Enable webhook**: Enable or disable the webhook.
      6. **Retry on failure**: Enable to automatically retry webhook delivery (up to 3 times) when receiving 5xx HTTP responses.
      7. **Labels** (optional): Enter a label or labels to help sort your webhooks if needed.
      8. **Headers**: Enable, then enter the **Key** and **Value** pair to add to the webhook.
4. Click **Create**.

### Reference webhooks in policy rules

Webhook messages are delivered using the [notification policy](../concepts/policy/notification-policy.md). When defining rules, the policy expects you to reference the webhook by its `ID` which you can copy from the webhook list view:

![Copy webhook ID](<../assets/screenshots/named-hooks2.png>)

### Webhook deliveries

Webhook deliveries and their response statuses are stored and can be explored by selecting a specific webhook
and viewing its details. You'll be presented with a list of deliveries, their status codes and when they happened.

You can also click on each delivery to view more details about it:

![Webhook deliveries list](<../assets/screenshots/named-hooks3.png>)

## Default webhook payloads

These are the default webhook payloads sent for each event type. If required, webhook payloads can be customized via a [notification policy](../concepts/policy/notification-policy.md).

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

- `account`: The name (subdomain) of the account generating the webhook. This is useful for pointing webhooks from various accounts at the same endpoint.
- `state`: A string representation of the [run state](../concepts/run/README.md#common-run-states) at the time of the notification being triggered.
- `stateVersion`: The ordinal number of the state, which can be used to ensure that notifications that may be sent or received out-of-order are correctly processed.
- `timestamp`: The unix timestamp of the state transition.
- `run`: Contains information about the run, its associated commit and delta (if any).
- `stack`: Contains some basic information about the parent [Stack](../concepts/stack/README.md) of the `run`.

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

- `title`: The title (summary) of the error.
- `body`: The full explanation of what went wrong.
- `error`: A description of the error that occurred.
- `severity`: One of three different constants: `INFO`, `WARNING`, `ERROR`.
- `account`: The account for which the error happened.

## Validate payload

To validate the incoming payload, you will need the secret you generated when creating or updating the webhook.

The following section provides different instructions for validating the payload depending on whether your Spacelift account is in our FedRAMP environment or not:

=== "Standard"

    Every webhook payload comes with two signature headers generated from the combination of the secret and payload. `X-Signature` header contains the SHA1 hash of the payload, while `X-Signature-256` contains the SHA256 hash. We're using the exact same mechanism as GitHub to generate signatures, please refer to [GitHub docs](https://docs.github.com/en/developers/webhooks-and-events/webhooks/securing-your-webhooks#validating-payloads-from-github){: rel="nofollow"} for details.

=== "FedRAMP"

    Only the SHA-256 signature will be used for webhook payload validation. The `X-Signature` header containing the SHA1 hash will not be provided, ensuring compliance with FIPS requirements that prohibit the use of SHA-1 for cryptographic purposes.
    
    We're using the exact same mechanism as GitHub to generate signatures, please refer to [GitHub docs](https://docs.github.com/en/developers/webhooks-and-events/webhooks/securing-your-webhooks#validating-payloads-from-github){: rel="nofollow"} for details.

Spacelift is using the exact same mechanism as GitHub to generate signatures, so you can refer to [GitHub's docs](https://docs.github.com/en/developers/webhooks-and-events/webhooks/securing-your-webhooks#validating-payloads-from-github){: rel="nofollow"} for details.

## Attach webhooks to stacks

!!! warning
    We recommend that you use [notification policies](../concepts/policy/notification-policy.md) to route stack events to your webhooks. Stack webhook integrations are provided for backwards compatibility.

Webhooks can be set up by Spacelift administrators on per-stack basis.

1. On the _Stacks_ page, click the three dots beside the stack you would like to attach a webhook to.
2. Click **Settings**, then **Integrations**.
3. Click **Webhooks**.
4. Either select an existing webhook or click **Create webhook**.

![Webhooks section in stack settings page](<../assets/screenshots/stack/stack-settings-webhooks.png>)

!!! info
    You can set up as many webhooks as you need for a Stack, though each one _must_ have a unique endpoint.

### Fill in webhook details

![Create a webhook on stacks settings page](<../assets/screenshots/stack/stack-create-webhook.png>)

1. **Endpoint**: Enter the endpoint URL the webhook will send information to.
2. **Secret** (optional): Enter the secret, if needed, to [validate the received payload](#validate-payload). It is up to you to decide on a non-obvious secret.
3. **Enable webhook**: Enable or disable the webhook.
4. **Retry on failure**: Enable to automatically retry webhook delivery (up to 3 times) when receiving 5xx HTTP responses.

Once saved, the webhook will appear on the list of integrations:

![Saved webhooks in list](<../assets/screenshots/stack/stack-webhooks-list.png>)

!!! info
    Unlike some other secrets in Spacelift, the webhook secret can be viewed by anyone with _read_ access to the stack. If you suspect foul play, consider regenerating your secret.

### Disable existing webhook

Webhooks are enabled by default, so they are triggered every time there's a run state change event on the stack they are attached to. If you want to temporarily disable some of the endpoints, you can do that without having to delete the whole integration.

1. Navigate to the _Integrations_ page and click **View** in the _Webhooks_ card.
      - You can also navigate to the _Stacks_ page, click the three dots beside the stack name, then click **Settings** > **Integrations** > **Webhooks**.
2. Click **Edit webhook**.
3. Click the toggle beside **Enable webhook**. When disabled, the toggle will be gray.

![Disabled webhook](<../assets/screenshots/stack/disable-webhook.png>)

Enable the webhook again by repeating steps 1-3 and clicking the toggle to turn it _blue_:

![Enabled webhook](<../assets/screenshots/stack/enable-webhook.png>)

!!! info "Auto-disabled webhooks"

    Webhooks in Spacelift are automatically disabled after **10 or more consecutive failures**. This is a built-in protection mechanism to prevent continuous failed attempts.

    Spacelift sends a notification to your account when a webhook is auto-disabled. To re-enable the webhook, resolve the underlying issue that caused the failures, and then manually re-enable it.
