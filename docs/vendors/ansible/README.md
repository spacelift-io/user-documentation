---
description: Managing Ansible Stacks through Spacelift.
---

# Ansible

You can find more details in the subpages:

- [Getting Started](getting-started.md)
- [Reference](reference.md)
- [Using Policies with Ansible stacks](policies.md)
- [Ansible Galaxy](ansible-galaxy.md)

## Why use Ansible?

Ansible is a versatile and battle-tested infrastructure configuration tool. It can do anything from software provisioning to configuration management and application deployment.

You can tap into the wealth of roles, playbooks, and collections available online to get started in no time.

## Why use Spacelift with Ansible?

Spacelift helps you manage the complexities and compliance challenges of using Ansible. It brings with it a GitOps flow, so your infrastructure repository is synced with your Ansible Stacks, and pull requests show you a preview of what they're planning to change. It also has an extensive selection of [policies](../../concepts/policy/README.md), which lets you [automate compliance checks](../../concepts/policy/terraform-plan-policy.md) and [build complex multi-stack workflows](../../concepts/policy/trigger-policy.md).

You can also use Spacelift to mix and match Terraform, Pulumi, AWS CloudFormation, Kubernetes, and Ansible Stacks and have them talk to one another. For example, you can set up Terraform Stacks to provision required infrastructure (like a set of AWS EC2 instances with all their dependencies) and then connect that to an Ansible Stack which then transactionally configures these EC2 instances using [trigger policies](../../concepts/policy/trigger-policy.md).
