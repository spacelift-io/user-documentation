# Security

At Spacelift, your security is our first and foremost priority. We're aware of the utmost importance of security in our service and we're grateful for your trust. Here's what we're doing to earn and maintain this trust, and to keep Spacelift secure by design.

## Certifications

SOC2 Type II Certified

Certification performed by an independent external auditor, who confirms the effectiveness of internal controls in terms of **Spacelift Security: Confidentiality, Integrity, Availability, and Privacy of customer data.**

## Security Audits

Spacelift regularly engages with external security firms to perform audits and penetration testing at least once per year. Additionally, the Spacelift Security Team conducts internal security audits regularly in combination with automated security tooling.

## Encryption

All of our data is encrypted at rest and in transit. With the exception of intra-VPC traffic between the web server and the load balancer protected by a restrictive [AWS security group](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html), all other traffic is handled using secure transport protocols. All the data sources (S3, database, SNS topics and SQS queues) are encrypted at rest using [AWS KMS](https://aws.amazon.com/kms/){: rel="nofollow"} keys with restricted and audited access.

[Customer secrets](../concepts/configuration/environment.md#a-note-on-visibility) are extra encrypted at rest in a way that should withstand even an internal attacker.

## Security Features

### Single Sign-On (SSO)

In addition to the default login providers (currently GitHub, GitLab, and Google), Spacelift also supports the ability to configure Single Sign-On (SSO) via SAML or OIDC using your favorite identity provider. Using SSO, Spacelift can be configured in a password-less approach, helping your company follow a zero-trust approach. As long as your Identity Provider supports SAML or OIDC, and passing the `email` scope, you're good to go! You can learn more about our Single Sign-On support [here](../integrations/single-sign-on/README.md).

### Environment Variables

Spacelift allows for granular control of environment variables on your [Stacks](../concepts/stack/README.md) either by setting [environment](../concepts/configuration/environment.md) variables on a per-stack basis, or creating collections of variables as a [Context](../concepts/configuration/context.md). These environment variables can be created in two types: **plain** or **secret**.

### Private Worker Pools

Spacelift supports the ability to host the underlying compute resources that are accessing your codebase and executing your deployments, on your own infrastructure as a [Private Worker Pool](../concepts/worker-pools.md). This allows customers to optionally have full control over the security of their deployments. Furthermore, the image used by Spacelift private workers is [open source](https://github.com/spacelift-io/spacelift-worker-image), giving customers full transparency into their private workers.

### Access Private Version Control Systems

For customers that have private-hosted version control systems such as on-premise installations of GitHub Enterprise, or [other VCS providers](../integrations/source-control/github.md), Spacelift provides the ability to access your on-premise VCS securely using [VCS Agent Pools](../concepts/vcs-agent-pools.md).

A single VCS Agent Pool is a way for Spacelift to communicate with a single VCS system on your side. You run VCS Agents inside of your infrastructure and configure them with your internal VCS system endpoint. They will then connect to a gateway on our backend, and we will be able to access your VCS system through them.

Spacelift VCS Agent Pools utilize gRPC on HTTP2 for secure, high-performance connectivity.

### Policies

Spacelift policies provide a way to express rules as code to manage your infrastructure as a code environment. Users can build policies to control Spacelift login permissions, access controls, deployment workflows, and even govern the infrastructure itself to be deployed. Policies are based on the [Open Policy Agent](https://www.openpolicyagent.org/) project and can be defined using its rule language _Rego_. You can learn more about policies [here](../concepts/policy/README.md).

## Responsible disclosure

If you discover a vulnerability, we would like to know about it so we can take steps to address it as quickly as possible. We would like to ask you to help us better protect our clients and our systems.

Please do the following:

- email your findings to [security@spacelift.io](mailto:security@spacelift.io);

- do not take advantage of the vulnerability or problem you have discovered, for example by downloading more data than necessary to demonstrate the vulnerability or deleting or modifying other people's data;

- do not reveal the problem to others until it has been resolved;

- do not use attacks on physical security, social engineering, distributed denial of service, spam or applications of third parties, and;

- do provide sufficient information to reproduce the problem, so we will be able to resolve it as quickly as possible;

What we promise:

- we will respond to your report within 3 business days with our evaluation of the report and an expected resolution date;

- if you have followed the instructions above, we will not take any legal action against you in regard to the report;

- we will handle your report with strict confidentiality, and not pass on your personal details to third parties without your permission;

- we will keep you informed of the progress towards resolving the problem;

- in the public information concerning the problem reported, we will give your name as the discoverer of the problem (unless you desire otherwise), and;

- as a token of our gratitude for your assistance, we offer a reward for every report of a security problem that was not yet known to us. The amount of the reward will be determined based on the severity of the leak and the quality of the report;

We strive to resolve all problems as quickly as possible, and we would like to play an active role in the ultimate publication on the problem after it is resolved.
