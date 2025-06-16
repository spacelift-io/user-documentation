---
description: Deploy Spacelift to your own AWS account!
---

# Spacelift Self-Hosted

Alongside our SaaS product, we also provide a self-hosted version of Spacelift that you can install into an AWS account that you control.

## Documentation

You can find the documentation for the latest version of self-hosted [here](./self-hosted/latest/). You can find our installation guide [here](./self-hosted/latest/installing-spacelift/install-methods.html).

## Differences between SaaS and Self-Hosted

The main difference is that our SaaS product is fully managed and maintained by us, whereas in Self-Hosted you are responsible for installing and maintaining a Spacelift install in your own AWS account. This provides you with full control of your Spacelift instance, but also requires more effort at your end to install and maintain.

In general, Self-Hosted includes all the functionality available in our Enterprise tier, except where those features don't make sense for Self-Hosted. The caveat to this is that new features become available in our SaaS product first, and will not become available in Self-Hosted at least until a new release is published.

The following is a list of features that are not available in Self-Hosted:

- [VCS Agents](./concepts/vcs-agent-pools.md) - Self-Hosted installations should be able to connect directly to your VCS system.
- Public worker pool - in Self-Hosted you manage your own workers.
- Azure and GCP [cloud integrations](./integrations/cloud-providers/README.md) - for now we recommend that you use [OIDC Federation](./integrations/cloud-providers/oidc/README.md) instead.

## Supported AWS Regions

At the moment we support all AWS commercial cloud regions, as well as GovCloud regions.

## How to Try Self-Hosted

If you are interested in trying out Self-Hosted, please [join us for a 15 minute alignment call](https://spacelift.io/schedule-demo).
