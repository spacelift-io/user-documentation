# Hello, Spacelift!

Spacelift is a specialized CI/CD platform designed to address the collaborative challenges of Infrastructure as Code (IaC). While traditional CI/CD tools excel at stateless applications, infrastructure management presents unique challenges that Spacelift was specifically built to solve.

## Infrastructure as Code: The Multiplayer Challenge

Infrastructure as Code projects create a unique set of challenges:

- **Coordination**: Multiple team members working on the same infrastructure can create conflicts
- **Dependencies**: Infrastructure components often depend on one another, creating complex deployment ordering requirements
- **Security**: Infrastructure credentials have significant privileges and require careful handling
- **State management**: Unlike application code, infrastructure changes rely on tracking what's currently deployed - this is particularly important for tools like OpenTofu, Terraform and Pulumi, which externally store a "digital twin" of your infrastructure state

Spacelift transforms infrastructure management from a risky solo endeavor into a collaborative experience with guardrails.

## The Graph of Graphs Problem

Most organizations face what we call the "graph of graphs" problem - the challenge of managing not just individual infrastructure stacks, but the complex relationships between them:

1. **Stack Dependencies**: Infrastructure projects often depend on outputs from other stacks
2. **Deployment Order**: Changes must be applied in the correct sequence to maintain system integrity
3. **Cross-team Collaboration**: Different teams maintain different components with interdependencies

Spacelift's [Stack Dependencies](concepts/stack/stack-dependencies.md) feature elegantly solves this by allowing you to:

- Define explicit relationships between stacks
- Automatically receive outputs from upstream stacks as inputs
- Trigger dependent stacks when upstream changes occur
- Visualize the complete dependency graph of your infrastructure

## Self-service Infrastructure with Blueprints

Blueprints enable controlled self-service for your organization, allowing platform teams to create standardized infrastructure templates while giving application teams the freedom to deploy what they need.

With [Blueprints](concepts/blueprint/README.md), you can:

- **Standardize Infrastructure**: Create templated stack configurations that enforce best practices
- **Enable Self-service**: Allow developers to provision infrastructure without deep IaC expertise
- **Maintain Governance**: Embed security guardrails and compliance controls directly in templates
- **Streamline Onboarding**: Reduce the time needed for teams to provision new environments

Blueprints transform the platform team from a bottleneck into enablers of developer productivity while maintaining control over infrastructure standards and security.

## Key Features

Spacelift supports a wide range of IaC tools including:

- [OpenTofu](https://opentofu.org/) and [Terraform](vendors/terraform/README.md)
- [Ansible](vendors/ansible/README.md)
- [Terragrunt](vendors/terragrunt/README.md)
- [Pulumi](vendors/pulumi/README.md)
- [AWS CloudFormation](vendors/cloudformation/README.md) and [AWS CDK](vendors/cloudformation/integrating-with-cdk.md)
- [Kubernetes](vendors/kubernetes/README.md)

With enterprise-grade capabilities:

- **Policy as Code**: Define [governance rules](concepts/policy/README.md) for who can do what, when, and how
- **Private Workers**: Run jobs within your own infrastructure for enhanced security
- **RBAC & Spaces**: Organize resources and control access with fine-grained permissions
- **Cloud Integrations**: Native integration with AWS, Azure, and GCP for secure credential management
- **VCS Integrations**: Connect with GitHub, GitLab, Bitbucket, and Azure DevOps

## Getting Started

New to Spacelift? We recommend exploring our documentation in this order:

1. [Core Concepts](concepts/stack/README.md) - Understand stacks, runs, and policies
2. [Stack Dependencies](concepts/stack/stack-dependencies.md) - Learn how to manage inter-project dependencies
3. [Blueprints](concepts/blueprint/README.md) - Discover how to enable self-service infrastructure
4. [Integrations](integrations/source-control/README.md) - Connect Spacelift to your existing tools
5. [Workers](concepts/worker-pools/README.md) - Execute jobs securely in your environment

If you're ready to try Spacelift, sign up for a free trial in [the EU region 🇪🇺](https://spacelift.io/free-trial), [the US region 🇺🇸](https://spacelift.io/free-trial) or [contact our team](https://spacelift.io/contact) for a personalized demo.
