# Notification policy

## Purpose

Notification [policies](./README.md) can be used to filter, route and adjust the body of notification messages sent by Spacelift. The policy works at the [space level](../spaces/README.md)
meaning that it does not need to be attached to a specific [stack](../stack/README.md), but rather is always evaluated if it can be accessed.
It's also important to note that all notifications go through the notification policy evaluation,
so depending on the rules defined any message can be directed to any provided route.

A notification policy can define the following rules:

- **inbox** - allows messages to be routed to the Spacelift notification inbox;
- **slack** - allows to route messages to a given slack channel;
- **webhook** - allows to route messages to a given webhook;

If no rules match no action is taken.

## Data input

This is the schema of the data input that each policy request can receive:

```json
{
  "run_updated:":{
    "state":"string",
    "username":"string",
    "note":"string",
    "run":{
      "creator_session":{
        "admin":"boolean",
        "creator_ip":"string",
        "login":"string",
        "name":"string",
        "teams":[
          "string"
        ],
        "machine":"boolean - whether the run was kicked off by a human or a machine"
      },
      "drift_detection":"boolean",
      "created_at":"number (timestamp in nanoseconds)",
      "id":"string",
      "runtime_config":{
        "before_init":[
          "string"
        ],
        "environment":"map[string]string",
        "project_root":"string",
        "runner_image":"string",
        "terraform_version":"string"
      },
      "state":"string",
      "triggered_by":"string or null",
      "type":"string - PROPOSED or TRACKED",
      "updated_at":"number (timestamp in nanoseconds)"
    },
    "stack":{
      "administrative":"boolean",
      "autodeploy":"boolean",
      "autoretry":"boolean",
      "branch":"string",
      "id":"string",
      "labels":[
        "string"
      ],
      "locked_by":"string or null",
      "name":"string",
      "namespace":"string or null",
      "project_root":"string or null",
      "repository":"string",
      "state":"string",
      "terraform_version":"string or null"
    }
  },
  "webhook_endpoints":[
    {
      "id":"custom-hook2",
      "labels":[
        "example-label1",
        "example-label2"
      ]
    }
  ],
  "internal_error":{
    "error":"string",
    "message":"string",
    "severity":"string - INFO, WARNING, ERROR"
  }
}
```

!!! warning
    The final JSON object received as input will depend on the type of notification being sent. For example, you will always receive `webhook_endpoints` data
    but will only receive the `internal_error` object if the notification is an internal error or the `run_updated` object if notification is about
    a [run](../run/README.md) being updated.

## Policy in practice

Using the notification policy, you can completely re-write notifications or control where and when they are sent. Let's look into how
the policy works for each of the defined routes.

### Inbox notifications

Inbox notifications are what you receive in your [Spacelift notification inbox](../../product/notifications.md). By default, these are errors that happened during
some kind of action execution inside Spacelift and are always sent even if you do not have a policy created.
However using the policy allows you to alter the body of those errors to add additional context, or even more importantly
it allows you to create your own unique notifications.

The inbox rule accepts multiple configurable parameters:

- `title` - a custom title for the message (**Optional**)
- `body` - a custom message body (**Optional**)
- `severity` - the severity level for the message (**Optional**)

#### Creating new inbox notifications

For example here is a inbox rule which will send `INFO` level notification messages to your inbox
when a tracked run has finished:

```opa
package spacelift

 inbox[{
  "title": "Tracked run finished!",
  "body": sprintf("http://example.app.spacelift.io/stack/%s/run/%s has finished", [stack.id, run.id]),
  "severity": "INFO",
 }] {
   stack := input.run_updated.stack
   run := input.run_updated.run
   run.type == "TRACKED"
   run.state == "FINISHED"
 }
```

[View the example in the rego playground](https://play.openpolicyagent.org/p/WGRgvTbU77){: rel="nofollow"}.

### Slack messages

[Slack](../../integrations/slack.md) messages can also be controlled using the notification policy, but before creating any policies that interact with slack
you will need to [add the slack integration to your Spacelift account](../../integrations/slack.md#linking-your-spacelift-account-to-the-slack-workspace).

!!! info
    The documentation section about [Slack](../../integrations/slack.md) includes additional information like: available actions,
    slack access policies and more. Consider exploring that part of documentation first.

Another important point to mention is that the rules for slack require a `channel_id` to be defined. This can be found at the bottom of a channel's _About_ section in Slack:

![](../../assets/screenshots/slack-channel-info.png)

Now you should be ready to define rules for routing slack messages. Slack rules allow you to make the same filtering
decisions as any other rule in the policy. They also allow you to edit the message bodies themselves in order to create custom messages.

The slack rules accept multiple configurable parameters:

- `channel_id` - the slack channel to which the message will be delivered (**Required**)
- `message` - a custom message to be sent (**Optional**)

#### Filtering and routing messages

For example if you wanted to receive only finished runs on a specific slack channel you would define a rule like this:

```opa
package spacelift

slack[{"channel_id": "C0000000000"}] {
  input.run_updated != null

  run := input.run_updated.run
  run.state == "FINISHED"
}
```

[View the example in the rego playground](https://play.openpolicyagent.org/p/kPtk55QHPK){: rel="nofollow"}.

#### Changing the message body

Together with filtering and routing messages you can also alter the message body itself, here is an example
for sending a custom message where a run which tries to attach a policy requires confirmation:

```opa
package spacelift

slack[{
  "channel_id": "C0000000000",
  "message": sprintf("http://example.app.spacelift.io/stack/%s/run/%s is trying to attach a policy!", [stack.id, run.id]),
}] {
  stack := input.run_updated.stack
  run := input.run_updated.run
  run.type == "TRACKED"
  run.state == "UNCONFIRMED"
  change := run.changes[_]
  change.phase == "plan"
  change.entity.type == "spacelift_policy_attachment"
}
```

[View the example in the rego playground](https://play.openpolicyagent.org/p/KyN5EHeyhk){: rel="nofollow"}.

### Webhook requests

Webhook notifications are a very powerful part of the notification policy. Using them one is able to not only
receive webhooks on specific events that happen in Spacelift, but also craft unique requests to be consumed
by some third party.

The notification policy relies on named webhooks which can be created and managed in the [Webhooks section of Spacelift](../../integrations/webhooks.md).
Any policy evaluation will always receive a list of possible webhooks together with their labels as input.
The data received in policy input should be used to determine which webhook will be used when sending the request.

!!! info
    This section of documentation requires you have configured at least one [Named Webhook](../../integrations/webhooks.md).
    Consider exploring that part of documentation first.

The webhook policy accepts multiple configurable parameters:

- `endpoint_id` - endpoint id (slug) to which the webhook will be delivered  (**Required**)
- `headers` - a key value map which will be appended to request headers (**Optional**)
- `payload` - a custom valid JSON object to be sent as request body (**Optional**)
- `method` - a HTTP method to use when sending the request (**Optional**)

#### Filtering webhook requests

Filtering and selecting webhooks can be done by using the received input data. Rules can be created where only
specific actions should trigger a webhook being sent.
For example we could define a rule which would allow a webhook to be sent about any drift detection run:

```opa
package spacelift

webhook[{"endpoint_id": endpoint.id}] {
  endpoint := input.webhook_endpoints[_]
  endpoint.id == "drift-hook"
  input.run_updated.run.drift_detection == true
  input.run_updated.run.type == "PROPOSED"
}
```

[View the example in the rego playground](https://play.openpolicyagent.org/p/qiMTWbTJxm){: rel="nofollow"}.

#### Creating a custom webhook request

All requests sent will always include the default headers for verification, a payload which is
appropriate for the message type and the `method` set as `POST`. However by using the webhook rule
we can modify the body of the request, change the method or add additional headers.
For example if we wanted to define a completely custom request for a [tracked run](../run/README.md) we would define a rule like this:

```opa
package spacelift

webhook[wbdata] {
  endpoint := input.webhook_endpoints[_]
  endpoint.id == "testing-notifications"
  wbdata := {
    "endpoint_id": endpoint.id,
    "payload": {
      "custom_field": "This is a custom message",
      "run_type": input.run_updated.run.type,
      "run_state": input.run_updated.run.state,
      "updated_at": input.run_updated.run.updated_at,
    },
    "method": "PUT",
    "headers": {
      "custom-header": "custom",
    },
  }

  input.run_updated.run.type == "TRACKED"
}
```

[View the example in the rego playground](https://play.openpolicyagent.org/p/fbfiiYEots){: rel="nofollow"}.
