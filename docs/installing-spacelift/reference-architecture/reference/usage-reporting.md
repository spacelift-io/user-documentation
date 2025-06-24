---
description: Usage reporting reference documentation.
---

# Usage reporting

Spacelift supports three methods for reporting usage: automatic, manual, and via script. Please choose the method that best suits your environment and operational requirements to ensure timely and accurate reporting.

## Automatic

**Best for**: Standard deployments with internet access.

The easiest way to enable usage reporting is to set the `SPACELIFT_PUBLIC_API` environment variable to point to our public API (`https://app.spacelift.io`). Ensure that the [Drain](./general-configuration.md#command-reference) service can access this endpoint.

| Environment variable   | Required | Description                                                                                         |
| ---------------------- | -------- | --------------------------------------------------------------------------------------------------- |
| `SPACELIFT_PUBLIC_API` | No       | Should be pointed at Spacelift's public API (`https://app.spacelift.io`). Defaults to empty string. |

## Manual

**Best for**: Air-gapped environments or networks with restricted internet access.

If your instance cannot reach the public API (e.g., due to network restrictions), you can export usage data manually:

Navigate to **Organization Settings** in the Spacelift UI, select **Usage Export** from the left menu, choose the desired date range and click **Export** to download the report. Finally, share the file with your Spacelift contact.

![](<../../../assets/screenshots/usage_export_download.png>)

## Python script

**Best for**: Automated workflows or programmatic access to usage data.

You can also use the [self-hosted-usage-data-exporter](https://github.com/spacelift-io/self-hosted-usage-data-exporter){: rel="nofollow"} script to fetch and optionally upload usage data.

By default, it generates a local report. Use the `--send-to-spacelift` flag to upload it automatically to Spacelift’s backend, eliminating the need to share the file manually.
