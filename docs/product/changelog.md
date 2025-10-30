---
description: Find out about the latest changes to Spacelift.
---

# Changelog

## 2025-11-03

### Features

- **Authorization & RBAC**: Stacks can now assume roles for elevated permissions through stack role attachments, replacing the legacy administrative flag. This new approach provides three key advantages:
    - **Cross-space access**: Attach roles for sibling spaces, not just the stack's own space and subspaces
    - **Fine-grained permissions**: Use custom roles with specific actions instead of full Space Admin permissions
    - **Enhanced audit trail**: Role information is included in webhook payloads for better visibility

    The administrative flag is deprecated for stacks and will be automatically disabled on **June 1st, 2026**. Spacelift will backfill affected stacks with Space Admin roles (100% backward compatible), but manual migration is recommended to access advanced features.

    Note: [Modules](../vendors/terraform/module-registry.md) are not affected by this change. The administrative flag for modules remains unchanged.

    See the [Stack Role Attachments documentation](../concepts/authorization/assigning-roles-stacks.md) for migration guides and detailed examples.

## 2025-10-27

### Features

- **Account default runner images** - Added support for account default runner images. See the [runtime security](../integrations/docker.md#account-default-runner-images) for more information.

## 2025-10-17

### Features

- **Dashboard**: The Dashboard is now accessible to all users, not just admins. Non-admin users can view most dashboard widgets, with the Launch Pad and User Activity widgets remaining admin-only.
- **Integrations**: Migrated the slack integration management screen to the integrations page. The legacy UI has been removed, and all the legacy URLs now redirect to the new screen in the Integrations page.

- **Module Registry**: Modules can now be shared with specific spaces within your account, providing fine-grained control over which teams can discover and use your modules.

    ![](../assets/screenshots/terraform/modules/module_sharing.png)

    The module list includes an availability filter to help you find modules shared with your spaces.

    Space-level sharing is now the recommended approach for most organizations, with cross-account sharing remaining available for backwards compatibility.

    See the [module sharing documentation](../vendors/terraform/module-registry.md#sharing-modules) for more details.

## 2025-10-15

### Features

- **Filters**: Enhanced filtering interface with improved selection states, dropdown functionality, and visual styling for better user experience
- Added SSO SAML attribute mapping support. See the [custom attribute mapping documentation](../integrations/single-sign-on/README.md#custom-attribute-mapping) for more information.

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

## 2025-10-01

### Features

- Run log retention period can now be configured at the organization level. This allows you to set how long run logs are retained before being automatically deleted. More details can be found in the [run log retention documentation](../concepts/run/README.md#logs-retention).

## 2025-09-30

### Features

- Detailed policy schema can now be retrieved from a public URL served by the Spacelift API. Each policy type has a detailed JSON schema definition which can be used for validation or provided to LLMs to generate policies. The schema can be found at [.well-known/policy-contract.json](https://app.spacelift.io/.well-known/policy-contract.json).

## 2025-09-16

### Features

- Run details now display both the API key ID and name when triggered by an API key. Previously only the key ID was shown, which made it difficult to identify which key was used. The key ID is shown in shortened format. For example: `api::01K56PK::DevopsSpaceKey`.
