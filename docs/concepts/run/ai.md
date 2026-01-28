---
description: >-
  This article explains how you can use Saturnhead AI to get feedback on your runs.
---

# AI

Spacelift provides a way to harvest the power of AI to summarize failed runs. By clicking **Explain** in the runs history page, Saturnhead will use an advanced LLM to digest the logs of your failed runs and provide useful insights into what went wrong.

## Enabling Saturnhead features

{% if is_saas() %}
!!! info
    This feature is only available to Enterprise plan customers. Please check out our [pricing page](https://spacelift.io/pricing){: rel="nofollow"} for more information.
{% endif %}

Saturnhead features must be enabled by an admin user in **Organization settings** > **Artificial Intelligence**. When enabling the Saturnhead Assist features for the first time, you'll be asked to accept the Terms and Conditions. Once accepted, all the users with read access to runs will be able to ask for assistance on failed runs.

![Enable Saturnhead AI Assist](<../../assets/screenshots/run/settings-ai-assist.png>)

Furthermore, admins can select the LLM model that will be used to provide assistance. Test different models to see which one works best for your organization.

## AI-empowered run summaries

After enabling the feature, the users with read access to the runs will be able to summarize failed executions.

!!! info
    This feature is only supported on stacks using OpenTofu or Terraform.

The results of a summary change per case due to the LLM being non-deterministic, but they generally provide the following information:

- Human-readable summary of the logs.
- Detailed information on what went wrong.
- Code snippet suggestions to help solve the issue.

There are 2 types of summary: **Summarize** and **Explain**.

- **Summarize** uses the output logs of the current phase to generate a human-readable summary. They're faster to execute and provide guidance on what went wrong in a specific step.

![Summary in the Spacelift UI](<../../assets/screenshots/run/trigger-step-summary.png>)

- By clicking **Explain**, Saturnhead will use the logs of the "Initialize", "Plan", and "Apply" phases combined to generate a global summary. This is ideal for catching issues that span across multiple phases. This summary is slower to run, but it is very helpful when dealing with more complex issues.

![Explain in the Spacelift UI](<../../assets/screenshots/run/trigger-run-summary.png>)

Once Saturnhead has analyzed the results of the run, it will display a message with the cause of the issue and potential fix solutions for the problem.

![Results of the Explain summary](<../../assets/screenshots/run/run-summarization-complete.png>)
