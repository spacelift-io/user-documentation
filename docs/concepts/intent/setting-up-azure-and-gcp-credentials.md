# Setting up Azure and GCP credentials for Spacelift Intent

## Azure credentials

1. Get your tenant id.

    ```jsx
        $ az account show --query 'tenantId'`
        "<YOUR-TENANT-ID>"
    ```

2. Get your subscription id.

    ```jsx
      $ az account subscription list --query '[].{name:displayName,id:id}'
        [ ... , { "id": "<YOUR-SUBSCRIPTION-ID>", "name": "..." }, ... ]
    ```

3. Optionally, create a role (role.json).

    ```jsx
        {
          "Name": "example-role”,
          "IsCustom": true,
          "Description": "example-role",
          "Actions": [
            "Microsoft.Resources/subscriptions/<ACTIONS…>"
          ],
          "NotActions": [],
          "DataActions": [],
          "NotDataActions": [],
          "AssignableScopes": [
            "/subscriptions/<YOUR-SUBSCRIPTION-ID>"
          ]
        }

        $ az role definition create --role-definition role.json
    ```

4. Create a service principal.

    ```jsx
        $ az ad sp create-for-rbac --name "example-name" --role "example-role" --scopes "/subscriptions/<YOUR-SUBSCRIPTION-ID>"
        {
        "appId": "<YOUR-CLIENT-ID>",
        "displayName": "example-name",
        "password": "<YOUR-CLIENT-PASSWORD>",
        "tenant": "<YOUR-TENANT-ID>"
        }
    ```

5. Get client id and client password from above and setup env vars.

    ```jsx
      ARM_CLIENT_ID="<YOUR-CLIENT-ID>"
      ARM_CLIENT_SECRET="<YOUR-CLIENT-PASSWORD>"
      ARM_TENANT_ID="<YOUR-TENANT-ID>"
      ARM_SUBSCRIPTION_ID="<YOUR-SUBSCRIPTION-ID>"
    ```

![Azure environment setup](<../../assets/screenshots/spacelift-intent/setting-up-azure-and-gpc/Screenshot_2025-10-22_at_13.48.03.png>)

## Google credentials

Configuring Google credentials for Intent follows the same steps as [setting up GCP](../../getting-started/integrate-cloud/GCP.md) for Spacelift, with only a slight change to the file paths for `spacelift.oidc` and `gcp.json`.

![Spacelift docs on GCP](<../../assets/screenshots/spacelift-intent/setting-up-azure-and-gpc/Screenshot_2025-10-22_at_13.55.08.png>)

1. When setting up the OIDC file location, use `/app/spacelift.oidc` instead of `/mnt/workspace/spacelift.oidc`.

    ![Spacelift docs on GCP](<../../assets/screenshots/spacelift-intent/setting-up-azure-and-gpc/Screenshot_2025-10-22_at_13.50.34.png>)

2. When setting up the JSON configuration, use `/app/spacelift.oidc` as well.

    ![Spacelift docs on GCP](<../../assets/screenshots/spacelift-intent/setting-up-azure-and-gpc/Screenshot_2025-10-22_at_13.52.29.png>)

3. At the end we need:

      - `GOOGLE_APPLICATION_CREDENTIALS=<pointing-to-JSON-configuration-file>`.
      - `GOOGLE_PROJECT=<project name>` (optional).
      - `gcp.json` (JSON configuration file).
      - `spacelift.oidc` will be automatically mounted.

![GCP env configuration](<../../assets/screenshots/spacelift-intent/setting-up-azure-and-gpc/Screenshot_2025-10-22_at_14.02.56.png>)
