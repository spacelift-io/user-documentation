---
description: Networking reference documentation.
---

# Networking

Spacelift is made up of a number of containerised components, along with certain external dependencies like a Postgres database and object storage. The following sections explain the different components that make up Spacelift, explains the role they perform and the specific networking requirements that they have.

## Container registries

Spacelift relies on two container images to function: the _backend image_, and the _launcher image_. The environment you deploy Spacelift into (for example a Kubernetes or ECS cluster) needs to be able to pull the backend image. If you deploy your workers using our [Kubernetes operator](../../../concepts/worker-pools/kubernetes-workers.md) the Kubernetes cluster will need to be able to pull the launcher image as well.

## Server

The server runs an HTTP server as well as an MQTT broker. The server is responsible for serving the frontend, providing HTTP APIs, as well as enabling communication with Spacelift workers over MQTT. The server uses MQTT for certain aspects of worker communication to allow it to "broadcast" messages to workers, even if they are not directly accessible by the Spacelift backend components.

### Ingress

| Name | Port | Protocol | Optional/Required | Description                                                                            |
| ---- | ---- | -------- | ----------------- | -------------------------------------------------------------------------------------- |
| HTTP | 1983 | TCP      | Required          | Used for serving HTTP requests like the frontend, GraphQL API and inbound webhooks.    |
| MQTT | 1984 | TCP      | Optional          | Used for serving the MQTT broker server. Required when using the built-in MQTT broker. |

### Egress

| Name           | Port         | Protocol | Optional/Required | Description                                                          |
| -------------- | ------------ | -------- | ----------------- | -------------------------------------------------------------------- |
| Postgres       | User-defined | TCP      | Required          | Outbound access to the Postgres database. By default this is `5432`. |
| Object Storage | 443          | TCP      | Required          | Outbound access to your object storage buckets.                      |
| VCS            | 443          | TCP      | Required          | Outbound access to customer source control system.                   |
| Message Queue  | 443          | TCP      | Optional          | Only required when using [SQS](./message-queues.md#sqs).             |
| MQTT Broker    | 443          | TCP      | Optional          | Only required when using [IoT Core](./mqtt-broker.md#iot-core).      |
| KMS            | 443          | TCP      | Optional          | Only required when using [KMS](./encryption.md#kms).                 |

## Drain

The drain handles asynchronous job processing. This component is responsible for processing inbound webhooks from your VCS system, along with other tasks like run scheduling.

### Ingress

No inbound access to the drain is required.

### Egress

| Name           | Port         | Protocol | Optional/Required | Description                                                          |
| -------------- | ------------ | -------- | ----------------- | -------------------------------------------------------------------- |
| Postgres       | User-defined | TCP      | Required          | Outbound access to the Postgres database. By default this is `5432`. |
| Object Storage | 443          | TCP      | Required          | Outbound access to your object storage buckets.                      |
| VCS            | 443          | TCP      | Required          | Outbound access to your source control system.                       |
| Message Queue  | 443          | TCP      | Optional          | Only required when using [SQS](./message-queues.md#sqs)              |
| MQTT Broker    | 443          | TCP      | Optional          | Only required when using [IoT Core](./mqtt-broker.md#iot-core).      |
| KMS            | 443          | TCP      | Optional          | Only required when using [KMS](./encryption.md#kms).                 |

## Scheduler

The scheduler handles triggering routine cron jobs required for Spacelift to function. Processing of these jobs once they are triggered is handled by the drain.

### Ingress

No inbound access to the scheduler is required.

### Egress

| Name          | Port         | Protocol | Optional/Required | Description                                                          |
| ------------- | ------------ | -------- | ----------------- | -------------------------------------------------------------------- |
| Postgres      | User-defined | TCP      | Required          | Outbound access to the Postgres database. By default this is `5432`. |
| Message Queue | 443          | TCP      | Optional          | Only required when using [SQS](./message-queues.md#sqs)              |

## Workers

Workers are responsible for executing runs and tasks within Spacelift. This is where the execution of your infrastructure as code tools is performed. Workers do not need to be deployed to the same network as the Spacelift backend, allowing you to manage infrastructure in other cloud environments than the Spacelift backend is deployed to or even on-prem.

For more information on workers please see [our worker pool documentation](../../../concepts/worker-pools/README.md).

### Ingress

No inbound access to your workers is required.

### Egress

| Name                 | Port                | Protocol | Optional/Required | Description                                                                                                                                                                             |
| -------------------- | ------------------- | -------- | ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Spacelift Server     | 443                 | TCP      | Required          | Access to the Spacelift Server for making synchronous requests (for example notifying state changes and retrieving run log URLs).                                                       |
| MQTT Broker          | 443 or user-defined | TCP      | Required          | Used for receiving broadcast messages from the server (for example job scheduling messages). The exact hostname and port depends on the type of [MQTT broker](./mqtt-broker.md) in use. |
| Object Storage       | 443                 | TCP      | Required          | Used to access run information and upload run logs using pre-signed URLs generated by the Spacelift backend services.                                                                   |
| VCS                  | 443                 | TCP      | Required          | Access to your source control system to download source code.                                                                                                                           |
| Container registries | 443                 | TCP      | Required          | Access to the Spacelift launcher image (for Kubernetes workers), along with the registry containing any [custom runner images](../../../concepts/stack/stack-settings.md#runner-image). |
| Infrastructure       | User-defined        | TCP      | Required          | Access to the APIs for any infrastructure components you are using Spacelift to manage.                                                                                                 |
