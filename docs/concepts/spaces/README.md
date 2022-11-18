# Spaces

## Introduction

With increased usage comes a bigger need for access control and self-service. Having a single team of admins doesn't scale when you start having tens or hundreds of people using Spacelift daily.

You may want to delegate partial admin rights to those teams, enable them to manage their own limited environments, but without giving them keys to the whole account and other teams' environments.

In Spacelift, this can be achieved by splitting your account into multiple Spaces.

Spaces are sets that can be filled with various kinds of Spacelift entities: [Stacks](../stack/README.md), [Policies](../policy/README.md), [Contexts](../configuration/context.md), [Modules](../../vendors/terraform/module-registry.md), [Worker Pools](../worker-pools.md), and [Cloud Integrations](../../integrations/cloud-providers/README.md).

Initially, you start with a `root` and a `legacy` space. The `root` space is the top-level space of your account, while the `legacy` space exists for backward compatibility with pre-spaces RBAC. You can then create more spaces, ending up with a big tree of segregated environments.

## What problems do Spaces solve?

First and foremost, Spaces let you give users limited admin access. This means that, in their space, they can create Stacks, Policies, etc. while not interfering with entities present in other Spaces.

Additionally, Spaces bring the ability to share resources between all these isolated environments, which means you can have a single worker pool and a single set of policies that can be reused by the whole organization.
