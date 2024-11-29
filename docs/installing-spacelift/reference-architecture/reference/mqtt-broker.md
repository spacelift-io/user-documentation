---
description: MQTT broker configuration reference documentation.
---

# MQTT Broker

Spacelift requires an MQTT broker for worker communication. There are currently two supported broker types:

- [AWS IoT Core](https://aws.amazon.com/iot-core/). Recommended for customers with existing Self-Hosted installation that were setup before the built-in broker became available.
- A built-in MQTT broker bundled with the Spacelift server service. Recommended for new installations and any installations outside of AWS.

## Configuration

The following environment variables can be used to configure your MQTT broker:

| Environment variable            | Required      | Description                                                                                  |
| ------------------------------- | ------------- | -------------------------------------------------------------------------------------------- |
| `MQTT_BROKER_TYPE`              | No            | Can be set to either `iotcore` (AWS IoT Core) or `builtin`. Defaults to `iotcore`.           |
| `MQTT_BROKER_ENDPOINT`          | Yes           | The endpoint workers use to connect to the MQTT broker.                                      |
| `MQTT_BROKER_BUILTIN_LOG_LEVEL` | No            | The log level used by the built-in MQTT broker. Defaults to `error`.                         |
| `MQTT_BROKER_IOTCORE_NAMESPACE` | For `iotcore` | The top-level namespace to use for MQTT topics when using IoT Core. Defaults to `spacelift`. |

## IoT Core

### Message queue type

When using IoT Core, you must use SQS instead of the built-in Postgres [message queue](./message-queues.md). This is required because our IoT Core implementation relies on an IoT topic rule to automatically publish messages from workers onto the IoT message queue.

### Broker endpoint

When using IoT Core the endpoint should be in the format `<id>-ats.iot.<region>.amazonaws.com`. You can find this address by running the following AWS CLI command (replacing `<region>` with the AWS region of your install):

```shell
aws iot describe-endpoint --endpoint-type iot:Data-ATS --region "<region>" --no-cli-pager --output json  | jq -r '.endpointAddress'
```

### Topic Namespace

Spacelift uses the following two IoT topic formats:

- `<namespace>/readonly/<workerpool-ulid>/<worker-ulid>` - used for Spacelift to send messages to workers.
- `<namespace>/writeonly/<workerpool-ulid>/<worker-ulid>` - used for workers to send messages to Spacelift.

The namespace can be anything you want, and defaults to `spacelift`. The only requirement is that it needs to match the topic rule setup when configuring your [IoT SQS queue](./message-queues.md#iot-core-topic-rule).

## Built-in broker

### Broker endpoint

When using the built-in IoT broker the endpoint should be in the format `<hostname>:<port>`. You can choose any hostname and port number for the broker other than `1983` (which is reserved for the HTTP server). The only requirement is that it is accessible from your workers.
