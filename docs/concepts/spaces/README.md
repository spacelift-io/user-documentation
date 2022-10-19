# Spaces (Feature Preview)

## Introduction
With increased usage comes a bigger need for access control and self-service.  Having a single team of admins doesn't scale when you start having tens or hundreds of people using Spacelift daily. You'd like to defer partial admin rights to those teams, enable them to manage their own limited environments, but without giving them keys to the whole account and other teams' environments.

In Spacelift, this can be achieved by splitting up your account into multiple Spaces.

Spaces are containers that can be filled with various kinds of Spacelift entities: Stacks, Policies, Contexts, Modules, Worker Pools, and Cloud Integrations.

Initially, you start with a root and legacy space. The root space is the top-level space of your accounts, while the legacy space is here for compatibility raesons with how things worked pre-spaces. You can then create more spaces, ending up with a big tree of segregated environments.

## What problems do Spaces solve?
First and foremost, Spaces let you give users limited admin access. This means that, in their space, they can create Stacks, Policies, etc. while not interfering with workloads present in other Spaces.

However, this you could already partially achieve with multiple accounts. What Spaces additionaly bring is the ability to share resources among all these isolated environments, which means you can have a single worker pool and a single set of policies that can be reused by the whole organization.

You can find more details about all of these in the sections below:
- link1
- link2
- link3
