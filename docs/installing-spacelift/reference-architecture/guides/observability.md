---
description: Observability guidelines for Self-Hosted Spacelift installations.
---

# Observability

This guide provides recommendations for monitoring your Self-Hosted Spacelift installation to ensure it's running correctly. Proper monitoring helps identify potential issues before they impact your operations and ensures the reliability of your Spacelift infrastructure.

## Metrics to Monitor

### Core Services

The following table shows the core metrics that you should monitor for each of your Spacelift services:

| Service           | Metric           | Description                  |
| ----------------- | ---------------- | ---------------------------- |
| **Server**        | CPU usage        | Processor utilization        |
|                   | Memory usage     | RAM consumption              |
| **Load balancer** | Response time    | Time to process API requests |
|                   | Error rate       | Percentage of 5xx responses  |
| **Scheduler**     | CPU usage        | Processor utilization        |
|                   | Memory usage     | RAM consumption              |
| **Drain**         | CPU usage        | Processor utilization        |
|                   | Memory usage     | RAM consumption              |
| **Database**      | CPU usage        | Processor utilization        |
|                   | Memory usage     | RAM consumption              |
|                   | Connection count | Active DB connections        |

### Message queues

The Drain service uses a number of different message queues to perform asynchronous processing of certain operations. The main metric you should monitor for the message queues is the queue length. When the drain is operating correctly, messages should be processed very quickly and you should not expect to see large backlogs (hundreds of messages) for long periods of time.

One caveat to this is the webhooks queue. Because webhooks processing involves making lots of requests to your source control system, they can sometimes take several minutes to process. It is not unusual to see small backlogs on the webhooks queue, or messages that take several minutes to process. This is ok as long as the messages are eventually being processed and the queue length is not constantly increasing.

The message queue length is easy to monitor for [SQS-based message queues](../reference/message-queues.md) - you can use the `ApproximateNumberOfMessagesVisible` metric [provided by SQS](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-available-cloudwatch-metrics.html){: rel="nofollow"}.

For the `postgres`-based message queue however, you will need [telemetry](#telemetry) enabled. When telemetry is enabled, we expose the following metrics:

- `postgres_queue.messages.sent` (counter) - incremented when a message is sent to the queue.
- `postgres_queue.messages.received` (counter) - incremented when a message is received from the queue.
- `postgres_queue.messages.changed_visibility` (counter) - incremented when a message visibility is changed.
- `postgres_queue.messages.deleted` (counter) - incremented when a message is deleted from the queue.
- `postgres_queue.messages.total` (gauge) - total number of messages in the queue.
- `postgres_queue.messages.visible` (gauge) - number of visible messages in the queue.

### Worker Pool Controller (Kubernetes)

For Kubernetes worker pool deployments, you can monitor the worker pool controller using Prometheus metrics. These metrics are available in the `spacelift_workerpool_controller` namespace. See the [Controller metrics](../../../concepts/worker-pools/kubernetes-workers.md#controller-metrics) section for more details.

| Metric                                                                     | Description                                                                        |
| -------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| `spacelift_workerpool_controller_run_startup_duration_seconds` (histogram) | Time between when a job assignment is received and the worker container is started |
| `spacelift_workerpool_controller_worker_creation_errors_total` (counter)   | Total number of worker creation errors                                             |
| `spacelift_workerpool_controller_worker_idle_total`  (gauge)               | Number of idle workers                                                             |
| `spacelift_workerpool_controller_worker_total` (gauge)                     | Total number of workers                                                            |

## Telemetry

Telemetry and tracing can help diagnose complex issues but is not required for basic monitoring. If you decide to implement tracing:

- Configure an appropriate backend (Datadog, AWS X-Ray, or OpenTelemetry).
- Focus on high-value traces (API requests, run execution, etc.).
- Use sampling in production to reduce overhead.

Refer to the [Telemetry reference](../reference/telemetry.md) for configuration options.

## Logging

Setting up proper log collection is strongly recommended - it’s a key part of running a healthy self-hosted installation. Without it, identifying and fixing issues becomes much harder and more time-consuming.

The sections below outline what logs are available and how to collect them across the different components of your Spacelift setup.

### Core services

All 3 core services (server, scheduler, and drain) log to `stdout` and `stderr`. We at Spacelift primarily use traces for debugging, so you won't find many "info" level logs. On the other hand, errors and terminal failures will be present.

### Docker-based worker pools

Our [Docker-based worker pools](../../../concepts/worker-pools/docker-based-workers.md) log to `/var/log/spacelift/error|info.log` files.

Note that in case of a startup failure, the worker will terminate immediately so you won't have a chance to see the logs. We provide an option to not terminate on failure for the below two types of deployments:

- [Cloudformation](../../../concepts/worker-pools/docker-based-workers.md) - the worker pool deployment stack has a [PowerOffOnError](../../../concepts/worker-pools/docker-based-workers.md#poweroffonerror) variable. If set to `false`, the worker pool will not terminate on startup failure.
- [terraform-aws-spacelift-workerpool-on-ec2](https://github.com/spacelift-io/terraform-aws-spacelift-workerpool-on-ec2){: rel="nofollow"} Terraform module - this module has a `selfhosted_configuration` variable that must be provided for self-hosted installations. The variable has an embedded `power_off_on_error` field.

### Kubernetes-based worker pools

The [Kubernetes-based worker pools](../../../concepts/worker-pools/kubernetes-workers.md) log to `stdout` and `stderr`. The documentation has a dedicated section on [troubleshooting](../../../concepts/worker-pools/kubernetes-workers.md#troubleshooting) that provides more details on how to retrieve logs. You can use any Kubernetes log collection tool (e.g., Fluentd, Fluent Bit, Loki) to collect and aggregate these logs.

## Further Reading

- [Telemetry Configuration](../reference/telemetry.md).
- [Prometheus Integration](../../../integrations/observability/prometheus.md).
- [Datadog Integration](../../../integrations/observability/datadog.md).
