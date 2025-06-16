---
description: Disaster recovery guidance for Self-Hosted installations.
---

# Disaster recovery

This page outlines some considerations to take when creating a disaster recovery plan for your Spacelift installation. Because disaster recovery plans are very specific to your organization and the way that your are deploying Spacelift, this page does not provide step-by-step instructions for enabling disaster recovery, but instead aims to explain the parts of your Spacelift installation that you need to think about when planning for a disaster.

## Stateless components

Spacelift consists of the following stateless components:

- The server.
- The drain.
- The scheduler.

These components do not store any data internally, and rely on the [stateful components](#stateful-components) for storage. In the event of a disaster, you can simply deploy new copies of these components and point them at replacement dependencies.

You can also have backup copies of these components already deployed and ready. However please note that these components will only successfully start up if they are able to connect to a valid Postgres database.

## Stateful components

The two main stateful components in a Spacelift installation are:

- The [Postgres database](../external-dependencies.md#database).
- The [object storage](../external-dependencies.md#object-storage-backend) buckets.

### Database

The Postgres database contains the main configuration information for your Spacelift installation. You should make sure it is backed up according to your standard organization requirements.

In the event of a disaster, you will want to make sure that this database is available to your replacement Spacelift services. Depending on your deployment scenario, this can involve options like the following:

- Restoring the database from a recent backup.
- Failing over to a secondary region.
- Using a globally available database that is available from a backup region.

### Object storage

We use different object storage buckets for different purposes. Some of these buckets only contain short-lived data used for temporary processing within Spacelift, whereas other buckets contain more critical data that you will want to make sure is available in the event of a disaster. The following buckets contain critical data that you will not want to lose in the event of a disaster:

- Modules.
- Policy inputs.
- Run logs.
- States.

The loss of data in your other object storage buckets may lead to temporary issues like run failures, but will not cause a problem long term.

In the event of a disaster you will want to make sure that your object storage data is available to your replacement Spacelift services. This may involve using buckets that are automatically replicated across multiple regions, or by setting up replication to copy your data to one or more backup regions.

!!! info
    If you are architecting a multi-region failover solution, you may want to consider setting up replication rules to copy objects back to your primary region in the case of a failover to your backup region. This means that if you want to later fail back to your primary region (particularly when running pre-planned DR tests) any data created in the backup region will be copied back.

## Encryption

In the event of a disaster, it is crucial that you have access to the key used to encrypt data in the Spacelift database.

### KMS

When using [KMS keys for encryption](../reference/encryption.md#kms), it is important to carefully choose between using a single or multi-region key because this property cannot be changed after key creation. If you want to setup a backup region for disaster recovery purposes, make sure to use a global key, and replicate that key to your backup region.

### RSA

When using [RSA keys for encryption](../reference/encryption.md#rsa) you should ensure that the RSA key you are using is available in the case of a disaster.

## Message queues

Although the message queues do technically store data, this information is generally very short-lived and it is not an issue if some data in your queues is lost during a disaster. In addition, when using the [Postgres message queue implementation](../reference/message-queues.md#postgres) all of your queue data is stored in your Postgres database meaning that you only need to take the database into consideration.

## Workers

### Built-in MQTT broker

When using the [built-in MQTT broker](../reference/mqtt-broker.md#built-in-broker) you do not need to do anything other than ensure that your Spacelift Server and MQTT broker DNS entries point at the correct services after disaster recovery. In this situation the workers should reconnect automatically, and failing that you can manually restart them.

### IoT Core

When using [IoT Core](../reference/mqtt-broker.md#iot-core) as your MQTT broker there are a few other considerations to make:

- You must setup a [custom IoT broker domain configuration](https://docs.aws.amazon.com/iot/latest/developerguide/iot-custom-endpoints-configurable-custom.html){: rel="nofollow"} if you want to be able to failover to a backup region. This allows you to update your DNS to point at a backup region in the case of a disaster without needing to re-register your workers.
- You should configure the `MQTT_BROKER_ENDPOINT` [environment variable](../reference/mqtt-broker.md#configuration) to point at your custom domain name.
- You should configure the `AWS_SECONDARY_REGION` [environment variable](../reference/general-configuration.md#aws) to point at your backup region. This ensures that your worker certificates are automatically replicated to your backup region.
