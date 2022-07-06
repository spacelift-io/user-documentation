---
description: >-
  This document defines what we support in terms of our products, services, and
  applications. Part of providing effective support is defining what is outside
  the scope of support.
---

# Statement of Support

## Scope of Support

Scope of support, in the simplest terms, is what we support and what we do not. Ideally, we would support everything. However, without reducing the quality of our support or increasing the price of our products this would be impossible. These "limitations" help us to create a more consistent and efficient support experience.

Please understand that any support that might be offered beyond the scope defined here is done at the discretion of the Support Engineer and is provided as a courtesy.

## Spacelift SaaS

### Free, Cloud, and Enterprise Customers

Site Reliability Engineering is everyone's responsibility at Spacelift. All product team members who ship backend features also carry a pager. This means that often, by the time you notice something is amiss, there's someone already looking into it.

We recommend that all Spacelift.com customers use our status page at [https://spacelift.statuspage.io](https://spacelift.statuspage.io/) to keep informed of any incidents.

### Free Users

Technical and general support for those using the Free version of Spacelift is “Community First”. Like many other free SaaS products, users are first directed to find support through community sources such as the following:

- Spacelift Documentation: Extensive documentation on anything and everything Spacelift.
- Stack Overflow: Please search for similar issues before posting your own, as there's a good chance someone else had the same issue as you and has already found a solution.

### Spacelift SaaS Availability

You should check our status page at [https://spacelift.statuspage.io](https://spacelift.statuspage.io) to see if there is a known service outage and follow the linked issue for more detailed updates.

## Out of Scope

The following sections outline what is within the scope of support and what is not for Spacelift SaaS customers, and both customers and Free users.

### Spacelift SaaS Customers

| Out of Scope                                                 | Example                                                                  | What's in-scope then?                                                                                                                    |
| ------------------------------------------------------------ | ------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------- |
| Troubleshooting non-Spacelift components                     | How do I merge a branch?                                                 | Support will happily answer any questions and help troubleshoot any of the components of Spacelift                                       |
| Consulting on language or environment-specific configuration | I want to set up a YAML linter CI task for my project. How do I do that? | The Support Team will help you find the Spacelift documentation for the related feature and can point out common pitfalls when using it. |

### All SaaS Users

#### Training

Spacelift Support is unable to provide training on the use of the underlying technologies that Spacelift relies upon. Spacelift is a product aimed at technical users, and we expect our users and customers to be versed in the basic usage of the technologies related to features that they're seeking support for.

For example, a customer looking for help with a Kubernetes integration should understand Kubernetes to the extent that they could retrieve log files or perform other basic tasks without in-depth instruction.

#### Third Party Applications & Integrations

Spacelift Support cannot assist with the configuration or troubleshooting of third party applications, integrations, and services that may interact with Spacelift. We can ensure that Spacelift itself is sending properly formatted data to a third party in the bare-minimum configuration.

#### Creation of SSL/TLS Certificates

Spacelift Support cannot assist with the creation of SSL/TLS certificates, certificate signing requests, or the creation of certificate authorities.

## **Alpha & Beta Features**

### **Alpha Features**

Alpha features are not yet completely tested for quality and stability, may contain bugs or errors, and prone to see breaking changes in the future. You should not depend on them and the API / functionality is subject to change. As such, support is not provided for these features and issues with them or other code changes should be opened in the Spacelift issue tracker.

### Beta Features

Your Support Contract will cover support for Beta features. However, because they are not yet completely tested for quality and stability, we may not yet have identified all the corner cases, and may be prone to see breaking changes in the future, troubleshooting will require more time, usually need assistance from Development, that support will be conducted on a **commercially-reasonable effort** basis.
