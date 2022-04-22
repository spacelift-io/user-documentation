# Security

At Spacelift, your security is our first and foremost priority. We're aware of the utmost importance of security in our service and we're grateful for your trust. Here's what we're doing to earn and maintain this trust.

## Encryption

All of our data is encrypted at rest and in transit. With the exception of intra-VPC traffic between the web server and the load balancer protected by a restrictive [AWS security group](https://docs.aws.amazon.com/vpc/latest/userguide/VPC\_SecurityGroups.html), all other traffic is handled using secure transport protocols. All the data sources (S3, database, SNS topics and SQS queues) are encrypted at rest using [AWS KMS](https://aws.amazon.com/kms/) keys with restricted and audited access.

[Customer secrets](../concepts/configuration/environment.md#a-note-on-visibility) are extra encrypted at rest in a way that should withstand even an internal attacker.

## Responsible disclosure

If you discover a vulnerability, we would like to know about it so we can take steps to address it as quickly as possible. We would like to ask you to help us better protect our clients and our systems.

Please do the following:

* email your findings to [security@spacelift.io](mailto:security@spacelift.io);\

* do not take advantage of the vulnerability or problem you have discovered, for example by downloading more data than necessary to demonstrate the vulnerability or deleting or modifying other people's data;\

* do not reveal the problem to others until it has been resolved;\

* do not use attacks on physical security, social engineering, distributed denial of service, spam or applications of third parties, and;\

* do provide sufficient information to reproduce the problem, so we will be able to resolve it as quickly as possible;

What we promise:

* we will respond to your report within 3 business days with our evaluation of the report and an expected resolution date;\

* if you have followed the instructions above, we will not take any legal action against you in regard to the report;\

* we will handle your report with strict confidentiality, and not pass on your personal details to third parties without your permission;\

* we will keep you informed of the progress towards resolving the problem;\

* In the public information concerning the problem reported, we will give your name as the discoverer of the problem (unless you desire otherwise), and;\

* as a token of our gratitude for your assistance, we offer a reward for every report of a security problem that was not yet known to us. The amount of the reward will be determined based on the severity of the leak and the quality of the report;

We strive to resolve all problems as quickly as possible, and we would like to play an active role in the ultimate publication on the problem after it is resolved.
