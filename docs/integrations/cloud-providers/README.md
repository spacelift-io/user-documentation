# Spacelift cloud provider integrations

Infrastructure-as-code automation tools such as Terraform, AWS CloudFormation, or Pulumi require powerful credentials to execute. Typically, you'd provide static credentials (such as AWS credentials, GCP service keys, etc.), which goes against security best practices. Spacelift's cloud integrations manage your resources _without_ the need for long-lived static credentials, dynamically generating short-lived access tokens to connect cloud providers with IaC providers.

Spacelift currently supports [AWS](AWS.md){% if is_saas() %}, [Azure](Azure.md), and [GCP](GCP.md){% endif %} natively. A generic [OpenID Connect](../../integrations/cloud-providers/oidc/README.md) integration is also available to work with any compatible service provider.

!!! hint "Public vs private workers"
    This feature is designed for customers using the shared public [worker pool](../../concepts/worker-pools/README.md). When hosting Spacelift workers on your own infrastructure, you can use your cloud providers' ambient credentials (e.g. EC2 instance role or EKS worker role on AWS).

## Set up your cloud provider integration

{% if is_saas() %}
Select your cloud provider to set up the integration:

- [Amazon Web Services (AWS)](./aws.md)
- [Microsoft Azure](./azure.md)
- [Google Cloud Platform (GCP)](./gcp.md)
{% endif %}
{% if is_self_hosted() %}
- Configure [Amazon Web Services (AWS)](./aws.md).{% endif %}

You can also use [OIDC](../../integrations/cloud-providers/oidc/README.md) for available cloud providers.
