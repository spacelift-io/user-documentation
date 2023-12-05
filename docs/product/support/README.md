---
description: Information about Spacelift support options.
---

# Support

{% if is_saas() %}
Spacelift offers a variety of support options for all users on both paid and free tiers. You should be able to find help using the resources linked below, regardless of how you use Spacelift.
{% else %}
Spacelift offers a variety of support options depending on your needs. You should be able to find help using the resources linked below, regardless of how you use Spacelift.
{% endif %}

## Have you tried…

Before reaching out for support, have you tried:

- Searching [our documentation](../../README.md). Most answers can be found there.
{% if is_saas() %}- Checking [our status page](https://spacelift.statuspage.io/){: rel="nofollow"}. Our infrastructure team is on-call 24/7. This means that most of the time, by the time you notice something is amiss, someone is already looking into it. Also, some issues are caused by third parties having incidents that are out of our control (e.g., Source Control provider issues).{% endif %}
- Reviewing the [Scope of Support section](./README.md#scope-of-support) to understand what is within the scope of Spacelift support.

## Contacting Support

{% if is_saas() %}
| Plan            | How to get support                                           |
| --------------- | ------------------------------------------------------------ |
| **Free**        | Open a conversation in the Spacelift chat widget             |
| **Cloud**       | Open a support ticket in the shared Slack channel (preferred, when available) or open a conversation in the chat widget in the bottom-right corner of the screen |
| **Enterprise**  | Open a support ticket in the shared Slack channel (preferred, when available) or open a conversation in the chat widget in the bottom-right corner of the screen |
| **Self-Hosted** | For technical questions related to the Spacelift product, open a support ticket in the shared Slack channel (preferred, when available), or email <support@spacelift.io> if using Slack is not possible. |
{% else %}
For technical questions related to the Spacelift product, open a support ticket in the shared Slack channel (preferred, when available), or email <support@spacelift.io> if using Slack is not possible.
{% endif %}

Questions related to billing, purchasing, or subscriptions should be sent to [ar@spacelift.io](mailto:ar@spacelift.io).

## Support SLA

The SLA times listed below are the timeframes in which you can expect the first response. Spacelift will make the best effort to resolve any issues to your satisfaction as quickly as possible. However, the SLA times are not to be considered as an expected time-to-resolution.

{% if is_saas() %}

### Free Plan

Support to the Free plan users is provided on a best-effort basis. There is no commitment to a specific response time.

### Cloud Plan

| Severity             | First Response Time | Working Hours               |
| -------------------- | ------------------- | --------------------------- |
| **Critical**         | 1 hour              | 24x7                        |
| **Major**            | 24 hours            | 4 am - 8 pm (ET), Mon - Fri |
| **Minor**            | 48 hours            | 4 am - 8 pm (ET), Mon - Fri |
| **General Guidance** | 72 hours            | 4 am - 8 pm (ET), Mon - Fri |

### Enterprise Plan

| Severity             | First Response Time | Working Hours               |
| -------------------- | ------------------- | --------------------------- |
| **Critical**         | 1 hour              | 24x7                        |
| **Major**            | 8 hours             | 4 am - 8 pm (ET), Mon - Fri |
| **Minor**            | 48 hours            | 4 am - 8 pm (ET), Mon - Fri |
| **General Guidance** | 72 hours            | 4 am - 8 pm (ET), Mon - Fri |

### Self-Hosted Plan

{% endif %}

| Severity             | First Response Time | Working Hours               |
| -------------------- | ------------------- | --------------------------- |
| **Critical**         | 1 hour              | 24x7                        |
| **Major**            | 8 hours             | 4 am - 8 pm (ET), Mon - Fri |
| **Minor**            | 48 hours            | 4 am - 8 pm (ET), Mon - Fri |
| **General Guidance** | 72 hours            | 4 am - 8 pm (ET), Mon - Fri |

Spacelift has support engineers in Europe and the US. They observe local holidays, so the working hours might change on those days. We have engineers on-call 24/7 for Critical incidents, so those are not impacted by holidays.

### Definitions of Severity Level

- **Severity 1 - Critical**: A critical incident with very high impact (e.g., A customer-facing service is down for all customers).
- **Severity 2 - Major**: A major incident with significant impact. (e.g., A customer-facing service is down for a sub-set of customers).
- **Severity 3 - Minor**: A minor incident with low impact:
    - Spacelift use has a minor loss of operational functionality, regardless of the environment or usage (e.g., A system bug creates a minor inconvenience to customers).
    - Important Spacelift features are unavailable or somewhat slowed, but a workaround is available.
- **Severity 4 - General Guidance**: Implementation or production use of Spacelift is continuing, and work is not impeded (e.g., Information, an enhancement, or documentation clarification is requested, but there is no impact on the operation of Spacelift).

Severity is assessed by Spacelift engineers based on the information at their disposal. Make sure to clearly and thoroughly communicate the extent and impact of an incident when reaching out to support to ensure it gets assigned the appropriate severity.

## Scope of Support

The scope of support, in the simplest terms, is what we support and what we do not. Ideally, we would support everything. However, without reducing the quality of our support or increasing the price of our product, this would be impossible. These "limitations" help create a more consistent and efficient support experience.

Please understand that any support that might be offered beyond the scope defined here is done at the discretion of the Support Engineer and is provided as a courtesy.

### Spacelift Features and Adjacent Technologies

Of course, we provide support for all Spacelift features, but also for adjacent parts of the third parties we integrate with.

Here are some examples of what is in scope and what is not for some of the technologies we support:

| Technology         | In Scope                                                     | Out of Scope                                             |
| ------------------ | ------------------------------------------------------------ | -------------------------------------------------------- |
| **Cloud Provider** | Helping configure the permissions used with a [Cloud Integration](../../integrations/cloud-providers/README.md) | Helping architecture a cloud account                     |
| **IaC Tool**       | Helping troubleshoot a failed deployment                     | Helping architecture your source code                    |
| **VCS Provider**   | Helping troubleshoot events not triggering Spacelift runs    | Advising how to best configure a VCS provider repository |

### Requirements

Spacelift cannot provide training on the use of the underlying technologies that Spacelift integrates with. Spacelift is a product aimed at technical users, and we expect our users to be versed in the basic usage of the technologies related to features that they seek support for.

For example, a customer looking for help with a Kubernetes integration should understand Kubernetes to the extent that they can retrieve log files or perform other essential tasks without in-depth instruction.

{% if is_self_hosted() %}For Self-Hosted, we do not provide support for the underlying cloud account that hosts Spacelift. We expect the network, security, and other components to be configured and maintained in a way that is compatible with [Spacelift requirements](../administration/install.md){% endif %}

### Feature Preview

#### Alpha Features

Alpha features are not yet thoroughly tested for quality and stability, may contain bugs or errors, and be prone to see breaking changes in the future. You should not depend on them, and the functionality is subject to change. As such, support is provided on a best-effort basis.

#### Beta Features

We provide support for Beta features on a commercially-reasonable effort basis. Because they are not yet thoroughly tested for quality and stability, we may not yet have identified all the corner cases and may be prone to see breaking changes in the future. Also, troubleshooting might require more time and assistance from the Engineering team.
