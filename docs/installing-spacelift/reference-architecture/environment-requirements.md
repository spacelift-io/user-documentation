---
description: An overview of the requirements for the environment that Spacelift runs in.
---

# Environment Requirements

Spacelift consists of a number of containerised applications along with certain external dependencies. You are responsible for creating and maintaining the environment that Spacelift runs in.

Take the following steps to get your environment ready for running Spacelift:

1. [Choose your hostnames](#choose-your-hostnames).
2. [Create an encryption key for encrypting sensitive data and signing tokens](#create-an-encryption-key).
3. [Configure networking](#configure-networking).
4. [Deploy Postgres](#deploy-postgres).
5. [Deploy object storage](#deploy-object-storage).
6. [Deploy a runtime environment for Spacelift](#deploy-a-runtime-environment).

## Choose your hostnames

Spacelift requires two hostnames to operate:

1. The hostname to use for accessing the Spacelift UI and API (for example, `spacelift.example.com`).
2. The hostname for the MQTT broker used for worker communication (for example `workers.spacelift.example.com`).

!!! info
    The only requirement for the MQTT broker hostname is that it is accessible from your workers. This can be useful
    when deploying Spacelift to Kubernetes clusters because you can use the internal Kubernetes DNS name for the
    service that exposes the MQTT broker endpoint, for example `spacelift-mqtt.spacelift.svc.cluster.local`.

## Create an encryption key

Spacelift requires an encryption key to store sensitive information and to sign things like session tokens. Depending on the environment you are deploying into, there are different options available for configuring this. Please see the [encryption reference](./reference/encryption.md) documentation for more details.

## Configure networking

Spacelift needs to be able to access certain external dependencies like a Postgres database, object storage, and your VCS system. For a full breakdown of the Spacelift services along with their ingress and egress requirements please see our [networking reference](./reference/networking.md) documentation.

## Deploy Postgres

Spacelift requires a Postgres database running version 14 or later. Other than the version there are no specific requirements.

## Deploy object storage

Spacelift requires access to an object storage system like AWS S3 or Google Cloud Storage to function. For the full configuration requirements see our [object storage reference](./reference/object-storage.md) documentation.

## Setup container registries

Spacelift relies on two container images to operate:

- `spacelift-backend` - the container image containing the backend services.
- `spacelift-launcher` - the container image required for running workers in Kubernetes. This is optional when choosing another approach for running workers.

You will need to have access to at least one container registry to push these images to when installing Spacelift. This registry will need to be accessible from the [runtime environment](#deploy-a-runtime-environment) you are using to host Spacelift.

## Deploy a runtime environment

Spacelift is a containerised application and requires an orchestration platform capable of running containers to operate. We recommend that you deploy Spacelift to a Kubernetes cluster, but it is also possible to run Spacelift in other environments like AWS ECS.
