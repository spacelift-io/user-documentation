# FedRAMP

Spacelift provides a FedRAMP Moderate Authorized environment for U.S. government agencies and contractors who need to meet federal security requirements. Our FedRAMP environment lets government organizations keep their development velocity while staying compliant with strict security standards.

## What is FedRAMP?

FedRAMP (Federal Risk and Authorization Management Program) is a U.S. government-wide program that standardizes security assessment, authorization, and continuous monitoring of cloud products and services. The program ensures federal data hosted in the cloud is consistently protected at the highest security standards.

FedRAMP compliance is required for cloud service providers working with U.S. federal agencies. Spacelift meets the **FedRAMP Moderate** compliance level, which covers the security standards needed for government workloads.

## Why Choose Spacelift's FedRAMP Environment?

### Security Standards

FedRAMP certification means your infrastructure management meets strict government security requirements:

- Rigorous security architecture and controls
- Strong encryption and approved cryptographic libraries
- Regular security patching and updates
- Continuous monitoring and compliance validation

### Operational Benefits

- Keep your existing development workflows while meeting compliance requirements
- No need to manage your own Infrastructure as Code platform
- Get the same Spacelift features you're used to, just in a secure environment
- Enterprise-level support with government-specific expertise

## Eligibility

The FedRAMP environment is exclusively available to eligible organizations, including:

- **U.S. Federal Government Agencies**: Primary users of FedRAMP authorized services.
- **Government Contractors**: Organizations working under contract with the federal government handling government data.
- **State and Local Governments**: Increasingly adopting FedRAMP to enhance data and system security.
- **Businesses Seeking Government Contracts**: Organizations pursuing federal contracts typically required to use FedRAMP authorized services.

## Resources Separation Strategies

FedRAMP and commercial workloads must be isolated from one another. You can achieve this in two ways:

### Isolation Delivered by Spacelift

To achieve full logical separation at the tenant level you need to create a second Spacelift account. The benefits of this approach include having a separate admin account, separate Identity Provider (IdP) configuration, separate audit and billing. This provides complete logical isolation between environments and ensures maximum security and compliance.

### Isolation Configured by The Customer

Spacelift supports strong multi-project isolation within a single tenant using [Spaces](../concepts/spaces/README.md), [RBAC](../concepts/authorization/README.md), [private worker pools](../concepts/worker-pools/README.md) and [Identity Provider (IdP) independent MFA](./security/mfa.md). Each Space functions as a self-contained boundary for stacks, policies, integrations, and contexts, allowing teams to operate independently without interference.

- **Spaces with role-based access control (RBAC) and resource isolation**. Each Space isolates stacks, policies, worker pools, contexts, and integrations. You can restrict which users or groups have access to each Space.
- **Separate Private Worker Pools** that run within your own infrastructure, enabling network and execution-level isolation. The temporary run state is encrypted so only your workers can decrypt it.
- **Separate customer-managed encryption keys (Bring Your Own Key / BYOK)** per worker pool or per integration for data-level separation, so Spacelift does not hold the decryption key.
- **Policy-driven governance**. Use Spacelift’s [policy types](../concepts/policy/README.md) (Login, Plan, Push, Approval, etc.) to enforce separation rules or guardrails over actions, role assignments, and allowed operations.
- **IdP-independent MFA (multi-factor authentication)**. You can enforce MFA policies that are not tied exclusively to a particular identity provider, applying additional security layers for users logging in through any IdP.
- **Integration with external secret managers**. You can use [pre-initialization hooks](../concepts/run/README.md#initializing) to fetch secrets directly from your own infrastructure, ensuring that sensitive data never leaves your environment and that Spacelift never has access to those secrets.

**Note that with this approach, commercial workloads must meet FedRAMP standards since they are hosted in the FedRAMP environment.**

## Platform Features and Limitations

Before getting started, it's important to understand how the FedRAMP environment differs from our standard SaaS platform. The FedRAMP environment provides identical functionality with two key security-driven limitations:

- **No Public Workers**: For security compliance, public workers are not available
- **Limited Error Collection**: Private worker error collection by Spacelift for troubleshooting is restricted. You are free to collect errors the way you see fit

!!! hint
    Since public workers aren't available in the FedRAMP environment, you cannot use them to programmatically set up the first [private worker pool](../concepts/worker-pools/README.md).

    You can work around this by running your initial Infrastructure as Code through your favorite CI/CD pipeline (e.g., GitHub Actions) to get your first private worker pool configured.

## Getting Started

1. Contact a Spacelift Account Executive.
2. Sign a Mutual Non-Disclosure Agreement (MNDA).
3. Complete identity verification.
4. Receive the FedRAMP trial sign-up URL.
5. Create your Spacelift account (initially disabled for compliance).
6. Share account URL with Account Executive for activation.
7. Begin configuration once account is enabled.

The identity verification process is secure and follows best practices. Spacelift and their vendors only store verification results, never the ID documents themselves.

## Infrastructure and Hosting

Our FedRAMP environment is built on a robust, compliant infrastructure designed for government workloads.

### Hosting Details

- **Primary Region**: AWS `us-east-2` (commercial partition).
- **Disaster Recovery**: Available in AWS `us-west-1`.
- **Compliance Partner**: Knox Systems provides the FedRAMP-compliant AWS environment. Spacelift is listed on [Knox Systems' FedRAMP Marketplace listing](https://marketplace.fedramp.gov/products/F1206111371){: rel="nofollow"}.

## Getting Help

Need to get started with FedRAMP Spacelift or have questions about compliance requirements? Here's how to reach us:

- **Sales inquiries**: Contact our sales team for pricing and trial access.
- **Existing customers**: Reach out to your Account Executive or Customer Success Manager.

Our team can help determine if the FedRAMP environment is right for your organization's specific compliance and operational needs.
