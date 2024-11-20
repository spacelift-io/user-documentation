---
description: Information about Spacelift support options.
---

# Support  

{% if is_saas() %}
Spacelift offers support at three different levels depending on the product tier you purchased. Please refer to your agreement with Spacelift to clarify which support level applies.
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
| Plan       | How to get support                                                                                                          |
| ---------- | --------------------------------------------------------------------------------------------------------------------------- |
| **Bronze** | Message us at [support@spacelift.io](mailto:support@spacelift.io) (preferred) or open a conversation in the chat widget in the bottom-right corner of the screen |
| **Silver** | Open a support ticket in the shared Slack channel (preferred, when available), message us at [support@spacelift.io](mailto:support@spacelift.io) or open a conversation in the chat widget in the bottom-right corner of the screen |
| **Gold**   | Open a support ticket in the shared Slack channel (preferred, when available), message us at [support@spacelift.io](mailto:support@spacelift.io) or open a conversation in the chat widget in the bottom-right corner of the screen |

{% else %}

| Plan       | How to get support                                                                                                          |
| ---------- | --------------------------------------------------------------------------------------------------------------------------- |
| **Gold**   | Open a support ticket in the shared Slack channel (preferred, when available), message us at [support@spacelift.io](mailto:support@spacelift.io) or open a conversation in the chat widget in the bottom-right corner of the screen |

{% endif %}

Questions related to:

- billing, purchasing, or invoicing should be sent to [ar@spacelift.io](mailto:ar@spacelift.io).
- your current subscriptions, add-ons, or renewals should be sent to your Customer Success Manager (if assigned) or [cs@spacelift.io](mailto:cs@spacelift.io).

## Support via Slack Channels  

For tickets opened in Slack channels, our commitment to meeting the service level agreements (SLAs) as described below is contingent upon having the Slack support channel integrated within our workspace, equipped with our monitoring and ticketing tools.

To ensure optimal support and SLA compliance, we recommend that all support interactions occur within the designated channels within our Slack workspace.

## Support SLA  

The SLA times listed below are the timeframes in which you can expect the first response. Spacelift will make a reasonable effort to adhere to the response times provided below and resolve any issues to your satisfaction as quickly as possible. However, the SLA times are not to be considered an expected time to resolution.

{% if is_saas() %}
| Severity             | Bronze              | Silver              | Gold               |
| -------------------- | ------------------- | ------------------- | ------------------ |
| **Critical**<br>24 x 7                    | 4 hours             | 3 hours            | 1 hour             |
| **Major**<br>_4 am - 8 pm ET, business days_* | Reasonable best effort | 8 business hours   | 4 business hours   |
| **Minor**<br>_4 am - 8 pm ET, business days_* | Reasonable best effort | 48 business hours  | 24 business hours  |
| **General Guidance**<br>_4 am - 8 pm ET, business days_* | Reasonable best effort | 72 business hours  | 72 business hours  |

{% if is_self_hosted() %}

| Severity             | Gold               |
| -------------------- | ------------------ |
| **Critical**<br>24 x 7                    | 1 hour             |
| **Major**<br>_4 am - 8 pm ET, business days_* | 4 business hours  |
| **Minor**<br>_4 am - 8 pm ET, business days_* | 24 business hours |
| **General Guidance**<br>_4 am - 8 pm ET, business days_* | 72 business hours |

{% endif %}
\* _Business day_ - any day in which normal business operations are conducted (Mon-Fri, except for US public holidays)

### Definitions of Severity Level  

Below you will find the definition of severity for each issue:

- **Severity 1 - Critical**: A critical issue of Spacelift product with very high impact (e.g., a customer-facing service is down for all customers).
- **Severity 2 - Major**: A major issue of Spacelift product with significant impact (e.g., a customer-facing service is down for a subset of customers).
- **Severity 3 - Minor**:  A minor issue of Spacelift product with low impact:
    - Spacelift use has a minor loss of operational functionality, regardless of the environment or usage (e.g., a system bug creates a minor inconvenience to users).
    - Important Spacelift features are unavailable or somewhat slowed, but a workaround is available.
- **Severity 4 - General Guidance**: Implementation or production use of Spacelift is continuing, and work is not impeded (e.g., information, an enhancement, or documentation clarification is requested, but there is no impact on the operation of the services provided by Spacelift).

Severity is assessed by Spacelift engineers based on the information at their disposal. Make sure to clearly and thoroughly communicate the extent and impact of an incident when reaching out to support to ensure it gets assigned the appropriate severity.

## Scope of Support  

The scope of support, in the simplest terms, is what we support and what we do not. Ideally, we would support everything. However, without reducing the quality of our support or increasing the price of our product, this would be impossible. These "limitations" help create a more consistent and efficient support experience.

Please understand that any support that might be offered beyond the scope defined here is done at the discretion of the Support Engineer and is provided as a courtesy

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
{% if is_saas() %}

### Availability and Downtimes  

We will use commercially reasonable efforts to:
    - maintain uptime of the SaaS services provided by Spacelift 99.8% of the time measured in a given calendar month,
    - give you at least 24 hours prior notice of all scheduled maintenance of the SaaS services provided by Spacelift.

You can check the current SaaS services’ availability status at [our status page](https://spacelift.statuspage.io/){: rel="nofollow"} and subscribe to be notified of any events.

Please be aware that the availability of the services provided by Spacelift might be affected by factors beyond our control, such as third party failures, interruptions or outages (which are not taken into account to calculate the uptime).
{% endif %}
