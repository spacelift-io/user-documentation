---
description: Find out about the latest changes to the Self-Hosted Spacelift.
---

# Changelog

## Changes between v2.1.0 and v2.2.0

### Features

- Our bulk actions feature has been reworked, making it simpler to perform actions on multiple items at once.
- We've added support for [OIDC Based API Keys](../../integrations/api.md#oidc-based-api-keys) to provide a more secure way of accessing our API without requiring static credentials.
- We've added the ability to add custom headers to your [audit trail webhooks](../../integrations/audit-trail.md), making it easier than ever to integrate with external systems.
- We've added [an option](./install.md#load-balancer) to `config.json` to set `load_balancer.subnet_placement` to either public (default) or private. If the option is omitted, the default remains public.

### Fixes

- We've added a new check that automatically fails the run if a Kubernetes worker pod exits without properly marking the run as finished or failed.

## Changes between v2.0.0 and v2.1.0

!!! warning
    You must upgrade to v2.0.0 **before** installing v2.1.0. If you attempt to upgrade an existing
    installation running a version older than v2.0.0, the installer will report an error and
    exit without making any changes.

    If you are currently on a version older than v2.0.0 and don't have access to the v2.0.0 installer
    anymore, please reach out to our support team for new download links.

### Features

- The stack and module settings have been revamped, making it simpler and more efficient to manage your stacks and modules. One of the standout additions is the new Scheduling and Policies tabs, which have moved from the stack settings to the main stack view. Your schedules and policies are now more easily discoverable, and can also be viewed by team members who don’t have access to stack settings.

### Fixes

- We've fixed an issue with our initial Disaster Recovery support that meant that IoT policies would not be added to your secondary region when resetting an existing worker pool that was created before DR was configured. The impact of this would have been that workers from the affected pools would not be able to connect to your IoT broker after failing over. No user intervention is required to resolve this - the v2.1.0 installation process will fix any affected worker pools.
- We've fixed an issue affecting Bitbucket Data Center that prevented branches being retrieved correctly if the repository contained more than 25 branches that contained your stack's branch name as part of their name (for example if a stack has a tracked branch called `dev`, and other branches exist in the repository like `development`, `dev-1`, `dev-2`, etc). This could prevent the stack settings for an affected stack from being saved.

## Changes between v1.3.0 and v2.0.0

!!! warning
    This release of Self-Hosted involves mandatory downtime during the installation process. We expect that downtime to be between 5 and 10 minutes, but it's important that you do not start the installation at a time you cannot afford Spacelift to be unavailable.

v2.0.0 introduces multi-region failover support to Self-Hosted to help as part of a [disaster recovery](./disaster-recovery.md) process. One of these changes involves converting the single-region KMS key used to encrypt sensitive data like stack and context secrets to a multi-region key. In order to do that, the installation includes a migration to convert the data from one key to another.

The migration is performed inside a transaction, and in the case of any errors the changes will be rolled back to avoid a situation where data is encrypted using both old and new keys.

Although we have safeguards in place to ensure the migration is successful, we recommend taking a snapshot of your RDS cluster before performing the installation in case anything goes wrong.

### Features

- Added the ability to provide a [custom database connection string](./install.md#self-managed-database) during install/upgrade. This allows you to take full control over the database used by Spacelift.
- Added [multi-region disaster recovery](./disaster-recovery.md) support.
- Added support for OpenTofu 1.8.0.
- Various other small features and improvements.

### Fixes

- Fixed a misconfiguration that was causing the server logs to be filled with messages containing `failed to record HTTP transaction`.

## Changes between v1.2.1 and v1.3.0

### Features

- Added ability to view spaces as a list view, you can now switch between Diagram and List view using the toggle in the page header
- Added Account details drawer (under user menu) with self hosted version, license information and identity provider data.
- Updated documentation links to use the currently used self hosted version immediately
- Added list view customization
- Added stack settings scheduling and policies tabs
- Added module list and form redesign

### Fixes

- Fix: Raw Git does not work with terraform modules

## Changes between v1.2.0 and v1.2.1

### Fixes

- Fix for an issue where a commit to Bitbucket Datacenter could trigger more stacks than necessary
- Fix for an issue where crashed workers left runs in a hanging state
- If custom certificates are defined, Spacelift's internal HTTP client will use those for AWS-related requests as well

## Changes between v1.1.0-hotfix.1 and v1.2.0

### Features

- [Added OpenTofu support for Terragrunt](../../vendors/terragrunt/terragrunt-tool.md)
    - **Important note**: in order to use this new feature, you need to recycle your worker pools. This is because new launcher versions are downloaded during the instance startup, and the old launchers do not support this new feature. Note: we recommend recycling the worker pools after each release anyway. The [native Kubernetes workers](../../concepts/worker-pools/kubernetes-workers.md) are an exception to this rule since each run starts a new container running the latest launcher image for your Self-Hosted instance.
- [Added `Trigger always` flag to Stack Dependencies](../../concepts/stack/stack-dependencies.md)
- Disabled the rate limiting for [policy sampling](../../concepts/policy/README.md#sampling-policy-inputs)
- Added LaunchPad, a dashboard for new Spacelift users that provides a guided tour of the platform
- Added support for [OPA v0.64](https://github.com/open-policy-agent/opa/releases/tag/v0.64.0)
- Support for [moved](https://developer.hashicorp.com/terraform/language/modules/develop/refactoring) and [imported](https://developer.hashicorp.com/terraform/language/import) Terraform resources
- Installation script:
    - [We added support for defining custom retention periods for all of the S3 buckets.](./install.md#s3-config) If you don't specify it, they remain untouched.

### Fixes

- Fixed a bug where some of the runs weren't scheduled because we attempted to checkout the same license from License Manager at the same time in parallel. Now license checkouts are serialized to avoid this issue.

## Changes between v1.1.0 and v1.1.0-hotfix.1

### Fixes

- Fixed an issue where license check-out could fail when multiple runs were scheduled at the same time

## Changes between v1.0.0 and v1.1.0

### Features

- [Beta Terragrunt support](../../vendors/terragrunt/README.md)
- [Enhanced VCS integrations](https://spacelift.io/changelog/en/enhanced-vcs-integrations)
- [OpenTofu v1.6.2 support](../../concepts/stack/creating-a-stack.md#opentofu)
- [New run history view](https://spacelift.io/changelog/en/introducing-the-new-run-history-view)
- [Redesigned stack creation view](https://spacelift.io/changelog/en/stack-creation-v2)

### Fixes

- Various backend and frontend fixes and improvements

## Changes between v0.0.12 and v1.0.0

### Features

- [User Management](../../concepts/user-management/README.md)
- [Terraform Provider Registry](../../vendors/terraform/provider-registry.md)
- The settings page is now split into Organization and Personal settings
- [OpenTofu v1.6.1 support](../../concepts/stack/creating-a-stack.md#opentofu)
- [PR stack locking](../../concepts/policy/push-policy/README.md#stack-locking)
- [Support for deploying workers via the Kubernetes operator](../../concepts/worker-pools/kubernetes-workers.md)

### Fixes

- Improved license check-out logic
- Fix stale logs display for [targeted replans](../../concepts/run/tracked.md#targeted-replan)
- Allow to persist roles and collections installed during run initialization for [Ansible stacks](../../vendors/ansible/README.md) automatically
- Various other backend and frontend fixes and improvements

## Changes between v0.0.11 and v0.0.12

### Features

- [OpenTofu v1.6.0 support](../../concepts/stack/creating-a-stack.md#opentofu)
- [PRs as notification targets](../../concepts/policy/notification-policy.md#pull-request-notifications)
- [Run prioritization through Push Policy](../../concepts/policy/push-policy/README.md#prioritization) (`prioritize` keyword)
- Add state size (in bytes) to `ManagedStateVersion` type in GraphQL

### Fixes

- Various backend and frontend fixes and improvements

## Changes between v0.0.10 and v0.0.11

### Features

- [New stack creation view](../../concepts/stack/creating-a-stack.md)
- [Auto Attaching Contexts](../../concepts/configuration/context.md#auto-attachments)
- [Context Hooks](../../concepts/configuration/context.md#editing-hooks)
- Additional [project globs](../../concepts/stack/stack-settings.md#project-globs)
- [Pull request default behaviour change](https://spacelift.io/changelog/en/upcoming-pull-request-default-behaviour-change)
    - Spacelift will start handling pull request events and creating proposed runs if no push policy is set as the default behaviour

### Fixes

- Various backend and frontend fixes and improvements

## Changes between v0.0.9 and v0.0.10

### Features

- Stack Dependencies with [output/input references](../../concepts/stack/stack-dependencies.md#defining-references-between-stacks).
- [Ready run state](../../concepts/run/README.md#ready).
- [Targeted replan support](../../concepts/run/tracked.md#targeted-replan).
- New detailed terraform changes view.
- [Worker Pool Management views](../../concepts/worker-pools#worker-pool-management-views).
- [Add OpenTofu and custom workflows support for terraform](../../vendors/terraform/workflow-tool.md).

### Fixes

- Do not re-create SAML certificate during each install

## Changes between v0.0.8 and v0.0.9

### Features

- Increase worker default disk size to 40GB.
- Adding support for Terraform versions up to v1.5.7.
- Update frontend and backend to the latest versions.

### Fixes

- Enforce bucket policy to prevent objects getting fetched not using HTTPS.
- Updated no account ID message to indicate that it is caused by missing AWS credentials in the install script.

## Changes between v0.0.7 and v0.0.8

### Features

- Update CloudFormation worker pool template to allow [a custom instance role to be provided](../../concepts/worker-pools/docker-based-workers.md#using-a-custom-iam-role).
- Update CloudFormation worker pool template to allow poweroff on crash to be disabled to aid debugging.
- Update CloudFormation worker pool template to [allow custom user data to be provided](../../concepts/worker-pools/docker-based-workers.md#injecting-custom-commands-during-instance-startup).
- Update frontend and backend to the latest versions.
- Adding support for Terraform versions up to v1.5.4 and kubectl up to v1.27.4.
- Added support for [External Dependencies](../../concepts/policy/push-policy/run-external-dependencies.md).
- Added support for [Raw Git](../../integrations/source-control/raw-git.md) source code provider.

### Removals

- Remove the unused `ecs-state-handler` Lambda.

### Fixes

- Improve warning message during installation when changeset contains no changes.
- Fix role assumption and automatic ECR login in GovCloud regions.
- Don't incorrectly attempt to report errors to Bugsnag in Self-Hosting (errors were never reported, but this could cause some misleading log entries).
- Fix crash on run startup if the runner image was missing the `ps` command.
- Increase default worker pool size to `t3.medium`.
- Increase minimum drain instances to 3 to provide more resilience.
