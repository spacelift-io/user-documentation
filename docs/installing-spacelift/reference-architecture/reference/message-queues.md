---
description: Documents the types of message queues supported by Spacelift.
---

# Message queues

Spacelift uses a number of message queues to support asynchronous processing. We support two options for message queues: AWS SQS, or a built-in message broker that uses your Postgres database.

For new installations we suggest using the Postgres message broker. The main exception to this is if you want to use AWS IoT Core rather than our built-in MQTT broker. In that case you **must** use SQS as IoT Core can only deliver messages to SQS queues by design.

## Configuration

The following environment variables can be used to configure message queues:

| Environment variable                 | Required  | Description                                                                                                                    |
| ------------------------------------ | --------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `MESSAGE_QUEUE_TYPE`                 | No        | Can be set to either `sqs` or `postgres`. Defaults to `sqs`.                                                                   |
| `MESSAGE_QUEUE_SQS_ASYNC_FIFO_URL`   | For `sqs` | The URL of the SQS queue used for processing async jobs in FIFO order. Required when `MESSAGE_QUEUE_TYPE` is set to `sqs`.     |
| `MESSAGE_QUEUE_SQS_ASYNC_URL`        | For `sqs` | The URL of the SQS queue used for processing async jobs. Required when `MESSAGE_QUEUE_TYPE` is set to `sqs`.                   |
| `MESSAGE_QUEUE_SQS_CRONJOBS_URL`     | For `sqs` | The URL of the SQS queue used for processing cronjobs. Required when `MESSAGE_QUEUE_TYPE` is set to `sqs`.                     |
| `MESSAGE_QUEUE_SQS_DLQ_FIFO_URL`     | For `sqs` | The URL of the SQS queue used as the deadletter queue for async FIFO jobs. Required when `MESSAGE_QUEUE_TYPE` is set to `sqs`. |
| `MESSAGE_QUEUE_SQS_DLQ_URL`          | For `sqs` | The URL of the SQS queue used as the deadletter queue for async jobs. Required when `MESSAGE_QUEUE_TYPE` is set to `sqs`.      |
| `MESSAGE_QUEUE_SQS_EVENTS_INBOX_URL` | For `sqs` | The URL of the SQS queue used for processing events. Required when `MESSAGE_QUEUE_TYPE` is set to `sqs`.                       |
| `MESSAGE_QUEUE_SQS_IOT_URL`          | For `sqs` | The URL of the SQS queue used for processing IoT messages from workers. Required when `MESSAGE_QUEUE_TYPE` is set to `sqs`.    |
| `MESSAGE_QUEUE_SQS_WEBHOOKS_URL`     | For `sqs` | The URL of the SQS queue used for processing inbound VCS webhooks. Required when `MESSAGE_QUEUE_TYPE` is set to `sqs`.         |

## SQS

When using SQS the following queues need to be created, along with the suggested configuration options:

| Name                    | Visibility timeout | Message retention | Description                                                                                         |
| ----------------------- | ------------------ | ----------------- | --------------------------------------------------------------------------------------------------- |
| Async                   | 300s               | Default           | Used for processing async tasks.                                                                    |
| Async (FIFO)            | 300s               | Default           | Used for processing async tasks that must be processed in a certain order (e.g. run state changes). |
| Cronjobs                | 300s               | 3600s             | Used to trigger scheduled task processing.                                                          |
| Deadletter queue        | 300s               | Default           | Used to store messages that have failed processing too many times.                                  |
| Deadletter queue (FIFO) | 300s               | Default           | Used to store messages from FIFO queues that have failed processing too many times.                 |
| Events inbox            | 300s               | Default           | Used for processing async tasks.                                                                    |
| IoT                     | 45                 | Default           | Used for processing messages sent by Spacelift workers to the IoT Core MQTT broker.                 |
| Webhooks                | 600s               | Default           | Used for processing messages received from VCS system webhooks.                                     |

In addition, you should use the following configuration options for all the queues:

- A max receive count of `3`.
- The "Async (FIFO)" queue should have its redrive policy configured to send messages to the "Deadletter queue (FIFO)".
- All other queues should use the "Deadletter queue".

### IoT Core topic rule

In order to allow messages sent from Spacelift workers to be processed by the backend services, an IoT Core topic rule needs to be created to publish messages sent to certain topics onto your IoT SQS queue.

The rule should look something like this:

```terraform
resource "aws_iot_topic_rule" "iot-to-sqs" {
  # var.iot_namespace is configurable, but needs to match whatever you use for `MQTT_BROKER_IOTCORE_NAMESPACE` (defaults to `spacelift`).
  name        = var.iot_namespace
  description = "Send all messages published in the ${var.iot_namespace} namespace to the ${aws_sqs_queue.iot.name} queue"
  enabled     = true
  sql         = "SELECT *, Timestamp() as timestamp, topic(3) as worker_pool_ulid, topic(4) as worker_ulid FROM '${var.iot_namespace}/writeonly/#'"
  sql_version = "2016-03-23"

  sqs {
    # queue_url should reference your IoT queue
    queue_url  = aws_sqs_queue.iot.id

    # role_arn should point to a role that is able to perform `sqs:SendMessage` on the IoT SQS queue.
    role_arn   = aws_iam_role.iot.arn
    use_base64 = true
  }
}
```

## Postgres

The Postgres message broker doesn't require any specific additional configuration other than setting the `MESSAGE_QUEUE_TYPE` environment variable to `postgres`.

## Monitoring & scaling

For detailed information on monitoring message queue performance and metrics, see the [observability guide](../guides/observability.md#message-queues).
