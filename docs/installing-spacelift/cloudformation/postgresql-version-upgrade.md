---
description: Learn how to safely upgrade your PostgreSQL database version in CloudFormation-based Self-Hosted installations.
---

# PostgreSQL Version Upgrades

Starting with Self-Hosted v3.9.0, you can configure the PostgreSQL engine version for CloudFormation-based installations using the `postgres_engine_version` parameter in your configuration file. This guide explains how to safely upgrade your database version and what to expect during the process.

!!! info "CloudFormation installations only"
    This guide is for CloudFormation-based Self-Hosted installations. If you're using Terraform-based installations, follow the [HashiCorp RDS upgrade tutorial](https://developer.hashicorp.com/terraform/tutorials/aws/rds-upgrade#upgrade-rds-instance){: rel="nofollow"} instead.

## Overview

The PostgreSQL version configuration feature allows you to:

- Explicitly control which PostgreSQL version your Self-Hosted installation uses
- Upgrade to newer PostgreSQL versions to benefit from performance improvements and security updates
- Maintain consistency across environments by pinning to specific versions

The installation process automatically creates the appropriate DB parameter groups for your specified PostgreSQL version and validates your configuration before deployment.

## Understanding CloudFormation's Immediate Application Behavior

When you update the `postgres_engine_version` parameter and run the installation script, CloudFormation applies the database version change **immediately** rather than waiting for the next maintenance window. This is an important distinction from how the AWS CLI or Console typically handle RDS modifications.

!!! note "Why CloudFormation applies changes immediately"
    CloudFormation's RDS resources always apply modifications immediately by design rather than deferring to maintenance windows. This ensures stack updates complete predictably and prevents drift detection issues. See [AWS CloudFormation issue #597](https://github.com/aws-cloudformation/cloudformation-coverage-roadmap/issues/597){: rel="nofollow"} for details.

This immediate application means that **upgrading your PostgreSQL version will cause downtime during the installation process**, even if your RDS instance has a maintenance window configured.

## Expected Downtime

PostgreSQL version upgrades require the database to be taken offline while the upgrade is performed. The downtime duration depends on your database instance size, data volume, and the version jump being performed.

!!! info "Real-world timing"
    In our testing, a single `db.t4g.medium` instance took approximately 12 minutes to upgrade. Expect 10-30 minutes depending on your database size and instance type.

## Configuration

Add or update the `database.postgres_engine_version` parameter in your `config.json` file:

```json
{
    "account_name": "your-org",
    "aws_region": "your-region",
    "database": {
        "postgres_engine_version": "14.20"
    },
    ...
}
```

**Default value**: `13.21`

**Supported versions**: Check the [ValidUpgradeTarget](#finding-available-versions) for your current version to see which versions you can upgrade to

!!! tip "Incremental upgrades recommended"
    For production environments, we recommend upgrading one major version at a time (e.g., 13 → 14 → 15) rather than jumping multiple versions. This minimizes risk and makes it easier to identify compatibility issues.

### Finding Available Versions

To check which versions you can upgrade to from your current version:

```bash
aws rds describe-db-engine-versions \
    --engine aurora-postgresql \
    --engine-version "13.21" \
    --query "DBEngineVersions[0].ValidUpgradeTarget"
```

Replace `13.21` with your current PostgreSQL version to see all valid upgrade paths.

## Upgrade Process

Follow these steps to safely upgrade your PostgreSQL version:

!!! tip "Database snapshots"
    CloudFormation automatically creates a snapshot before upgrading your database. However, you can manually create an additional snapshot for extra safety using the AWS CLI or console.

### 1. Stop Spacelift Services

Stop all ECS services to prevent connection attempts during the database upgrade:

```bash
./start-stop-services.sh -e false -c config.json
```

This script gracefully stops the server, scheduler, and drain services.

### 2. Update Configuration and Run Installer

Update the `database.postgres_engine_version` in your `config.json`:

```json
{
    "account_name": "your-org",
    "aws_region": "your-region",
    "database": {
        "postgres_engine_version": "14.20"
    },
    ...
}
```

Run the installation script:

```bash
./install.sh -c config.json
```

The installer will detect the version change and apply the upgrade. This is when the 10-30 minute downtime occurs.

### 3. Restart Spacelift Services

Re-enable all Spacelift services:

```bash
./start-stop-services.sh -e true -c config.json
```

The services will start back up and reconnect to the upgraded database.

!!! note "Cleanup old parameter groups"
    After a successful upgrade, old DB parameter groups are retained and can be manually removed from the RDS console if desired. They are kept for safety to allow rollback if needed.
