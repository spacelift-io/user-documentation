# Cloud providers

!!! info
    This feature is mostly designed for clients using the shared public worker pool. When hosting Spacelift workers on your infrastructure you can use your cloud providers' ambient credentials (eg. EC2 instance role or ECS task role on AWS).

Cloud provider integrations allow Spacelift to manage your resources without the need for long-lived static credentials. Terraform and Pulumi are used to manage infrastructure, which usually requires credentials. Usually, these are very powerful credentials. Administrative credentials, sometimes. And these can do _a lot of damage_. Typically, you'd provide those credentials statically - think AWS credentials, GCP service keys, etc.

This is dangerous, and against security best practices. That's why Spacelift integrates with identity management systems from major cloud providers to dynamically generate short-lived access tokens that can be used to configure their corresponding Terraform providers.

Currently, [AWS](aws.md), [Azure](azure.md) and [GCP](gcp.md) are fully supported.
