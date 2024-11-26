---
description: Install Self-Hosted Spacelift using our reference architecture approach.
---

# Introduction

This page provides an overview of how to deploy Spacelift into your own environment. Our recommended approach is to deploy Spacelift into a Kubernetes cluster, however it is also possible to run Spacelift in other containerised environments like AWS ECS.

## Requirements

!!! Tip
    We recommend reading the external dependencies page below before proceeding with the installation process and checking specific configurations.
    The objective is to help you develop a clear understanding of how you intend to run Spacelift, essentially allowing you to customize your setup according to your needs.

Please see the [external dependencies](external-dependencies.md) page for the set of requirements for running Spacelift along with its external dependencies.

## Quick Start

If you just want to get up and running quickly, please check out one of our quick start guides:

- [Deploying to AKS](./guides/deploying-to-aks.md).
- [Deploying to ECS](./guides/deploying-to-ecs.md).
- [Deploying to EKS](./guides/deploying-to-eks.md).
- [Deploying to GKE](./guides/deploying-to-gke.md).
- [Deploying to an on-prem Kubernetes cluster](./guides/deploying-to-onprem.md).

Otherwise the rest of this page will provide an overview of the installation process for Spacelift.

## Configuration reference

For information about all of the available configuration options, please see the [configuration reference](./reference/README.md).

## Installation process

The main steps required to deploy Spacelift are:

1. [Get your license key and installation materials](#getting-your-license-key-and-installation-materials).
2. [Prepare your environment for installation](#preparing-your-environment).
3. [Deploy Spacelift](#deploying-spacelift).
4. [Perform first setup](#first-setup).

The following sections explain each of these steps in detail.

### Getting your license key and installation materials

In order to install Spacelift you need a valid license key along with the installation materials containing resources like the required container images. Please reach out to your sales representative for more information.

### Preparing your environment

Before you can install Spacelift, you need an environment to install it into. Please see the [environment requirements](environment-requirements.md) page for more details.

### Deploying Spacelift

There are multiple ways you can deploy Spacelift - we'll ship the Docker images to you and you can choose to deploy them in a way that suits your environment. We also have a number of [quick start guides](./guides/README.md) available to get you up and running quickly.

### First setup

Once Spacelift has been deployed to your environment, follow our [first setup guide](./guides/first-setup.md) to get your account up and running.

## Upgrading

Spacelift supports zero downtime upgrades unless otherwise mentioned in the [changelog](../changelog.md). The process for upgrading to a new release is as follows:

1. Make any required infrastructure adjustments.
2. Push the latest container images to your registry.
3. Deploy the latest Spacelift backend components.
4. Redeploy your workers (note this is not required when using our [Kubernetes operator](../../concepts/worker-pools/kubernetes-workers.md)).
