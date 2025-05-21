# Cloud Integrations

Cloud integrations allow Spacelift to manage your resources without the need for long-lived static credentials. When using infrastructure-as-code automation tools such as OpenTofu, Terraform, AWS CloudFormation, or Pulumi, these tools typically require credentials to execute. Usually, these are very powerful credentials, administrative credentials, sometimes. And these can do _a lot of damage_. Typically, you'd provide those credentials statically - think AWS credentials, GCP service keys, etc. This is dangerous, and against security best practices.

That's why Spacelift integrates with identity management systems from major cloud providers to dynamically generate short-lived access tokens that can be used to configure their corresponding OpenTofu/Terraform providers.

{% if is_saas() %}
Currently, [AWS](aws.md), [Azure](azure.md) and [GCP](gcp.md) are natively supported. A generic [OpenID Connect](oidc/README.md) integration is also available to work with any compatible service provider.
{% else %}
Currently [AWS](aws.md) is natively supported. A generic [OpenID Connect](oidc/README.md) integration is also available to work with any compatible service provider.
{% endif %}

!!! hint
    This feature is designed for clients using the shared public worker pool. When hosting Spacelift workers on your infrastructure you can use your cloud providers' ambient credentials (eg. EC2 instance role or EKS worker role on AWS).
