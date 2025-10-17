---
description: Find out about the latest changes to Spacelift.
---

# Changelog

## 2025-10-17

### Features

- **Dashboard**: The Dashboard is now accessible to all users, not just admins. Non-admin users can view most dashboard widgets, with the Launch Pad and User Activity widgets remaining admin-only.

## 2025-10-15

### Features

- **Filters**: Enhanced filtering interface with improved selection states, dropdown functionality, and visual styling for better user experience

## 2025-10-14

### Features

- **Personal Settings**: You can now find new "Spaces" view under your personal settings. This view lets you see the permissions you have for each space, making it easier to understand your access across Spacelift.

## 2025-10-10

### Features

- **VCS Integrations**: Completed migration to the new VCS integration interface. The legacy VCS integration UI has been removed, and the source code integrations can now be accessed using the new integrations screen.

## 2025-10-03

## Features

- You can now create API keys via the TF provider. See the [API keys resource documentation](https://search.opentofu.org/provider/spacelift-io/spacelift/latest/docs/resources/api_key) for more information.
- Added SSO OIDC claim mapping support. See the [custom claims mapping documentation](../integrations/cloud-providers/oidc/README.md#configuring-custom-claims-mapping) for more information.
- Added SSO SAML attribute mapping support. See the [custom attribute mapping documentation](../integrations/single-sign-on/README.md#custom-attribute-mapping-for-teams) for more information.

## 2025-10-01

### Features

- Run log retention period can now be configured at the organization level. This allows you to set how long run logs are retained before being automatically deleted. More details can be found in the [run log retention documentation](../../concepts/run#logs-retention).

## 2025-09-30

### Features

- Detailed policy schema can now be retrieved from a public URL served by the Spacelift API. Each policy type has a detailed JSON schema definition which can be used for validation or provided to LLMs to generate policies. The schema can be found at [.well-known/policy-contract.json](https://app.spacelift.io/.well-known/policy-contract.json).

## 2025-09-16

### Features

- Run details now display both the API key ID and name when triggered by an API key. Previously only the key ID was shown, which made it difficult to identify which key was used. The key ID is shown in shortened format. For example: `api::01K56PK::DevopsSpaceKey`.
