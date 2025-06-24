---
description: Contains information about configuration options as well as the commands available for running Spacelift.
---

# General configuration

This page lists the basic configuration options available for running the Spacelift backend services. It contains a command reference, and then separate sections for various configuration options grouped by functionality.

## Command reference

The Spacelift backend services are distributed as a container image. This container image contains a `spacelift` binary that is used to run each of the Spacelift services. The following table lists the services along with the command used to run them:

| Service   | Command                         | Description                                                                         |
| --------- | ------------------------------- | ----------------------------------------------------------------------------------- |
| Server    | `spacelift backend server`      | Runs the HTTP server and (optionally) built-in MQTT broker.                         |
| Drain     | `spacelift backend drain-local` | Runs the asynchronous event processing service.                                     |
| Scheduler | `spacelift scheduler`           | Runs the service responsible for triggering scheduled background tasks (cron jobs). |

## Basic settings

The following basic settings need to be configured:

| Environment variable | Required | Description                                                                                                         |
| -------------------- | -------- | ------------------------------------------------------------------------------------------------------------------- |
| `SERVER_DOMAIN`      | Yes      | This should be set to the domain that users should use to access Spacelift. For example `spacelift.myorg.com`.      |
| `DATABASE_URL`       | Yes      | This should be set to the URL of your Postgres database. For example `postgres://postgres@localhost:5432/postgres`. |

## Admin Login

You can enable an admin login that can be accessed via username and password using the `/admin-login` URL. This can be useful during first time installation, or as a break-glass procedure if you become unable to login via SSO.

To enable this, add the following environment variables to your Spacelift server container:

| Environment variable | Description                         |
| -------------------- | ----------------------------------- |
| `ADMIN_USERNAME`     | The username for the admin account. |
| `ADMIN_PASSWORD`     | The password for the admin account. |

To disable admin logins, either remove the two environment variables or set them to empty strings.

## Licensing

We support two ways of providing a license to your Spacelift instance: via AWS License Manager, or via a license token. The following table lists the license-related configuration options:

| Environment variable | Required  | Description                                             |
| -------------------- | --------- | ------------------------------------------------------- |
| `LICENSE_TYPE`       | No        | Can be set to either `aws` or `jwt`. Defaults to `aws`. |
| `LICENSE_TOKEN`      | For `jwt` | The JWT containing your license details.                |

## Cloud provider authentication

Spacelift requires credentials to your cloud provider to enable certain pieces of functionality, for example access to object storage buckets and role assumption in AWS. The following sections explain how authentication works for the different supported cloud providers.

### AWS

We use the AWS Go SDK for accessing AWS services. The [AWS documentation](https://docs.aws.amazon.com/sdk-for-go/v1/developer-guide/configuring-sdk.html) about configuring the SDK outlines the various options available for authentication. Typically the best approach when running Spacelift in AWS is to create a role for the Spacelift backend services, and then grant the relevant permissions to that role to access the various AWS services required by Spacelift.

When using AWS, please make sure that the following environment variables are set:

| Environment variable   | Required | Description                                                                                                                                    |
| ---------------------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| `AWS_ACCOUNT_ID`       | Yes      | Set to the ID of the account you are deploying Spacelift into.                                                                                 |
| `AWS_PARTITION`        | No       | The [AWS partition](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html) you are deploying Spacelift into. Defaults to `aws`. |
| `AWS_REGION`           | Yes      | The region you are deploying Spacelift into.                                                                                                   |
| `AWS_DEFAULT_REGION`   | Yes      | Set to the same value as `AWS_REGION`.                                                                                                         |
| `AWS_SECONDARY_REGION` | No       | The failover region to use when configuring disaster recovery.                                                                                 |

### Google Cloud

We use the Google Cloud Go SDK for accessing Google Cloud services. You can use [Application Default Credentials](https://cloud.google.com/docs/authentication/client-libraries) to configure access to your account.

When using Google Cloud, please make sure that the following environment variable is set:

| Environment variable | Description                                                                 |
| -------------------- | --------------------------------------------------------------------------- |
| `GCP_PROJECT`        | The GCP project containing your GCP resource (e.g. object storage buckets). |
