---
description: Object storage reference documentation.
---

# Object storage

Spacelift requires access to object storage buckets to store certain pieces of data. Currently AWS S3, Google Cloud Storage, Azure Blob Storage and MinIO are supported.

The following table explains each of the buckets that are required. For each bucket, we indicate whether they should have versioning enabled, as well as the retention rules that should be configured. Where the retention is listed as "user configurable", you can adjust the retention to suit your needs. A suggested value is included to give you a reasonable starting point.

| Name                     | Versioning | Retention                   | Description                                                                                      |
| ------------------------ | ---------- | --------------------------- | ------------------------------------------------------------------------------------------------ |
| Deliveries               | No         | User configurable (1 day)   | Used to store the request and response bodies of outbound webhooks.                              |
| Large queue messages     | No         | 2 days                      | Stores inbound webhook payloads that are too large to be posted to a message queue.              |
| Metadata                 | No         | 2 days                      | Stores the metadata required by workers to process runs.                                         |
| Modules                  | Suggested  | Infinite                    | Stores Terraform modules and providers.                                                          |
| Policy inputs            | No         | User configurable (7 days)  | Stores sampled policy evaluations.                                                               |
| Run logs                 | Suggested  | User configurable (60 days) | Stores the content of run logs.                                                                  |
| States                   | Required   | Infinite                    | Stores OpenTofu/Terraform state files when using the built-in Spacelift state server.            |
| Uploads                  | Suggested  | 1 day                       | Used to temporarily upload files from the frontend.                                              |
| User uploaded workspaces | Suggested  | 1 day                       | Used to store workspaces uploaded from user machines as part of the local preview functionality. |
| Workspace                | Suggested  | 7 days                      | Used to temporarily store the workspaces of runs that go into an unconfirmed state.              |

## Configuration

The following environment variables can be used to configure object storage:

| Environment variable                             | Required       | Description                                                                                                                             |
| ------------------------------------------------ | -------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `OBJECT_STORAGE_TYPE`                            | No             | Can be set to `aws` (AWS S3), `gcp` (Google Cloud Storage), `azure` (Azure Blob Storage), `minio` (MinIO). Defaults to `aws`.           |
| `OBJECT_STORAGE_AZURE_ACCOUNT_URL`               | Yes if `azure` | The URL of the Azure storage account e.g. https://{account}.blob.core.windows.net                                                       |
| `OBJECT_STORAGE_MINIO_ENDPOINT`                  | Yes if `minio` | The MinIO server endpoint URL (e.g., minio.example.com:9000).                                                                           |
| `OBJECT_STORAGE_MINIO_ACCESS_KEY_ID`             | Yes if `minio` | The access key ID for MinIO authentication.                                                                                             |
| `OBJECT_STORAGE_MINIO_SECRET_ACCESS_KEY`         | Yes if `minio` | The secret access key for MinIO authentication.                                                                                         |
| `OBJECT_STORAGE_MINIO_USE_SSL`                   | No             | Whether to use SSL/TLS for MinIO connections. Defaults to `false`.                                                                      |
| `OBJECT_STORAGE_MINIO_ALLOW_INSECURE`            | No             | Whether to allow insecure SSL connections to MinIO. Defaults to `false`.                                                                |
| `OBJECT_STORAGE_BUCKET_DELIVERIES`               | Yes            | Bucket where webhook delivery traces are stored.                                                                                        |
| `OBJECT_STORAGE_BUCKET_LARGE_QUEUE_MESSAGES`     | Yes            | Bucket where message payloads too large for storing on message queues are stored.                                                       |
| `OBJECT_STORAGE_BUCKET_METADATA`                 | Yes            | Bucket used to store metadata needed for workers to execute runs.                                                                       |
| `OBJECT_STORAGE_BUCKET_MODULES`                  | Yes            | Bucket where OpenTofu/Terraform module source is stored.                                                                                |
| `OBJECT_STORAGE_BUCKET_POLICY_INPUTS`            | Yes            | Bucket where policy evaluation samples are stored.                                                                                      |
| `OBJECT_STORAGE_BUCKET_RUN_LOGS`                 | Yes            | Bucket where run logs are stored.                                                                                                       |
| `OBJECT_STORAGE_BUCKET_STATES`                   | Yes            | Bucket used to store stack state files.                                                                                                 |
| `OBJECT_STORAGE_BUCKET_UPLOADS`                  | Yes            | Bucket used to temporarily store files uploaded from the frontend.                                                                      |
| `OBJECT_STORAGE_BUCKET_UPLOADS_URL`              | Yes            | The URL of the uploads bucket. This is used to generate a Content Security Policy (CSP) to allow the frontend to upload to this bucket. |
| `OBJECT_STORAGE_BUCKET_USER_UPLOADED_WORKSPACES` | Yes            | Bucket where workspaces uploaded as part of local preview functionality are stored temporarily.                                         |
| `OBJECT_STORAGE_BUCKET_WORKSPACE`                | Yes            | Bucket where run workspaces are stored.                                                                                                 |

## Access requirements

None of our buckets need public access - they just need access from the Spacelift backend services. For certain situations where access to buckets is required from outside the backend services, for example when uploading state files from the frontend, or when workers upload run logs, we rely on pre-signed URLs that are only valid for a certain period of time.

## Authentication

=== "AWS S3"

    When using AWS S3, Spacelift uses the default [AWS SDK credential provider chain](https://docs.aws.amazon.com/sdk-for-go/v1/developer-guide/configuring-sdk.html#specifying-credentials){: rel="nofollow"}, which automatically finds credentials in the following order: environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`), shared credential files and IAM roles for compute resources like EC2, ECS and EKS.

=== "Azure Blob Storage"

    When using Azure Blob Storage, Spacelift uses the [DefaultAzureCredential](https://learn.microsoft.com/en-gb/azure/developer/go/sdk/authentication/credential-chains#defaultazurecredential-overview){: rel="nofollow"} authentication chain. This automatically supports multiple authentication methods including environment variables, Workload Identity (recommended for AKS), and Managed Identity.

=== "Google Cloud Storage"

    When using Google Cloud Storage, Spacelift uses [Application Default Credentials (ADC)](https://cloud.google.com/docs/authentication/provide-credentials-adc){: rel="nofollow"}, which automatically finds credentials from multiple sources including: `GOOGLE_APPLICATION_CREDENTIALS` environment variable, [attached service accounts](https://cloud.google.com/docs/authentication/set-up-adc-attached-service-account){: rel="nofollow"} for compute resources, and [Workload Identity Federation](https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity){: rel="nofollow"} for [containerized environments](https://cloud.google.com/docs/authentication/set-up-adc-containerized-environment){: rel="nofollow"} like GKE.

=== "MinIO"

    When using MinIO, Spacelift requires explicit configuration through environment variables: `OBJECT_STORAGE_MINIO_ENDPOINT` for the server endpoint, `OBJECT_STORAGE_MINIO_ACCESS_KEY_ID` for the access key, and `OBJECT_STORAGE_MINIO_SECRET_ACCESS_KEY` for the secret key.

## Uploads bucket CORS configuration

The uploads bucket is used to allow users to upload certain items like Terraform state files from the frontend. To allow this to work, the bucket needs to be configured with the frontend URL as an allowed origin. The following examples show how to configure this using Terraform assuming you were hosting Spacelift at `spacelift.myorg.com`:

=== "AWS S3"
    ```terraform
    resource "aws_s3_bucket_cors_configuration" "spacelift-uploads" {
        bucket = aws_s3_bucket.spacelift-uploads.id

        cors_rule {
            allowed_headers = ["*"]
            allowed_methods = ["PUT", "POST"]
            allowed_origins = ["https://spacelift.myorg.com"]
        }
    }
    ```

=== "Google Cloud Storage"
    ```terraform
    resource "google_storage_bucket" "spacelift-uploads" {
        name = # bucket name
        location = # location

        public_access_prevention = "enforced"

        cors {
            origin = ["https://spacelift.myorg.com"]
            method = ["PUT", "POST"]
            response_header = ["*"]
            max_age_seconds = 3600
        }

        ... # more configuration options
    }
    ```
=== "Azure Blob Storage"
    ```terraform
    resource "azurerm_storage_account" "spacelift_storage_account" {
      # Some of the configuration options are omitted for brevity.
      blob_properties {
        versioning_enabled = true
        cors_rule {
          allowed_headers    = ["*"]
          allowed_methods    = ["PUT", "POST"]
          allowed_origins    = ["https://spacelift.myorg.com"]
          exposed_headers    = ["*"]
          max_age_in_seconds = 3600
        }
      }
    }
    ```

Note that the platform-specific Terraform modules ([terraform-azure-spacelift-selfhosted](https://github.com/spacelift-io/terraform-azure-spacelift-selfhosted){: rel="nofollow"}, [terraform-google-spacelift-selfhosted](https://github.com/spacelift-io/terraform-google-spacelift-selfhosted){: rel="nofollow"}, [terraform-aws-spacelift-selfhosted](https://github.com/spacelift-io/terraform-aws-spacelift-selfhosted){: rel="nofollow"}) take care of the CORS configuration.
