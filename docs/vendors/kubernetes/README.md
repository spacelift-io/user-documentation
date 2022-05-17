---
description: From this article you can learn how Kubernetes is integrated into Spacelift
---

# Kubernetes

## What is Kubernetes?

Kubernetes is a portable, extensible, open-source platform for managing containerized workloads and services, that facilitates both declarative configuration and automation. It has a large, rapidly growing ecosystem. Kubernetes services, support, and tools are widely available. For more information about Kubernetes, see the [reference documentation](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/).

## How does Spacelift work with Kubernetes?

Spacelift supports Kubernetes via `kubectl`.

## What is `kubectl`?

The Kubernetes command-line tool, [`kubectl`](https://kubernetes.io/docs/reference/kubectl/kubectl/), allows you to run commands against Kubernetes clusters. You can use `kubectl` to deploy applications, inspect and manage cluster resources, and view logs. For more information including a complete list of `kubectl` operations, see the [`kubectl` reference documentation](https://kubernetes.io/docs/reference/kubectl/).

## Why use Spacelift with Kubernetes?

Spacelift helps you manage the complexities and compliance challenges of using Kubernetes. It brings with it a GitOps flow, so your Kubernetes Deployments are synced with your Kubernetes Stacks, and pull requests show you a preview of what they're planning to change. It also has an extensive selection of [policies](../../concepts/policy/), which lets you [automate compliance checks](../../concepts/policy/terraform-plan-policy.md) and [build complex multi-stack workflows](../../concepts/policy/trigger-policy.md).

You can also use Spacelift to mix and match Terraform, Pulumi, CloudFormation, and Kubernetes Stacks and have them talk to one another. For example, you can set up Terraform Stacks to provision the required infrastructure (like an ECS/EKS cluster with all its dependencies) and then deploy the following via a Kubernetes Stack.

**Anything that can be run via `kubectl` can be run within a Spacelift stack.**

To find out more about Kubernetes Workload Resources, read the[ reference documentation](https://kubernetes.io/docs/concepts/workloads/controllers/).
