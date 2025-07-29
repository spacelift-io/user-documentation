# Integrate Spacelift with Amazon Web Services (AWS)

The AWS integration allows Spacelift [runs](../../concepts/run/README.md) or [tasks](../../concepts/run/task.md) to automatically [assume an IAM role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use.html){: rel="nofollow"} in your AWS account, and in the process, generate a set of _temporary credentials_. These credentials are then exposed as [computed environment variables](../../concepts/configuration/environment.md#computed-values) during the run/task that takes place on the Spacelift stack where the integration is attached.

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_SECURITY_TOKEN`
- `AWS_SESSION_TOKEN`

These temporary credentials are enough for both the [AWS Terraform provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#environment-variables){: rel="nofollow"} and the [Amazon S3 state backend](https://www.terraform.io/docs/backends/types/s3.html){: rel="nofollow"} to generate a fully authenticated AWS session without further configuration.

To use the AWS integration, you need to set it up and attach it to any stacks that need it.

## Set up the AWS IAM role

!!! info "Prerequisites"

    To set up the AWS integration, you need:

      - The ability to create IAM roles for your AWS account.
      - Administrator access to your Spacelift account.

### Step 1: Create a role in AWS

Before creating the Spacelift AWS integration, you need an [AWS IAM Role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html){: rel="nofollow"} within your AWS account.

!!! hint "Multiple AWS accounts"
    You can extend this role to have cross-account permissions to the target accounts to allow Spacelift to access multiple AWS accounts. See [AWS documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/tutorial_cross-account-with-roles.html){: rel="nofollow"} for more details.

1. Within your AWS account, navigate to _AWS IAM_.
2. Select the _Roles_ section and click **Create role**.

    ![Within AWS IAM, click Create role](<../../assets/screenshots/getting-started/cloud-provider/AWS-create-role.png>)

### Step 2: Configure trust policy

You will need to configure a custom [trust policy](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-custom.html){: rel="nofollow"} for the IAM role in AWS to allow Spacelift to assume the role and generate temporary credentials. When completing the role assumption, Spacelift will pass extra information in the `ExternalId` attribute, allowing you to add additional layers of security to your role.

**External ID Format:** `<spacelift-account-name>@<integration-id>@<stack-slug>@<read|write>`

- `<spacelift-account-name>`: The name of the Spacelift account, found in the lower left-hand side of the Spacelift platform UI.
- `<integration-id>`: The ID of the AWS Cloud Integration.
- `<stack-slug>`: The slug of the stack that the AWS Cloud Integration is attached to.
- `<read|write>`: Set to either `read` or `write` based upon the event that initiated the role assumption. The [Planning phase](../../concepts/run/proposed.md#planning) uses `read` while the [Applying phase](../../concepts/run/tracked.md#applying) uses `write`.

Given the format of the External ID passed by Spacelift, you can further secure your IAM Role trust policies for more granular security. For example, you may wish to lock down an IAM Role so that it can only be used by a specific stack.

#### Example trust policies

=== "Any stack can use role"

    Here's an example trust policy statement that allows any stack within your Spacelift account to use the IAM Role.

    {% if is_saas() %}
    Make sure to replace: 
    
      - `yourSpaceliftAccountName` with your actual Spacelift account name.
      - `<principal>` based on your environment:
        - for [spacelift.io](https://spacelift.io), use `324880187172`.
        - for [us.spacelift.io](https://us.spacelift.io), use `577638371743`.
    {% endif %}

    ```json
    {
    "Version": "2012-10-17",
    "Statement": [
            {
                "Action": "sts:AssumeRole",
                "Condition": {
                "StringLike": {
                    "sts:ExternalId": "yourSpaceliftAccountName@*"
                }
                },
                "Effect": "Allow",
                "Principal": {
                "AWS": "<principal>"
                }
            }
    ]
    }
    ```

=== "Specific stack can use role"

    Here's an example trust policy that locks down an IAM Role so it can only be used by the stack `stack-a`.

    {% if is_saas() %}
    Make sure to replace: 
    
      - `yourSpaceliftAccountName` with your actual Spacelift account name.
      - `<principal>` based on your environment:
        - for [spacelift.io](https://spacelift.io), use `324880187172`.
        - for [us.spacelift.io](https://us.spacelift.io), use `577638371743`.
    {% endif %}

    ```json
    {
    "Version": "2012-10-17",
    "Statement": [
            {
                "Action": "sts:AssumeRole",
                "Condition": {
                "StringLike": {
                    "sts:ExternalId": "yourSpaceliftAccountName@*@stack-a@*"
                }
                },
                "Effect": "Allow",
                "Principal": {
                "AWS": "<principal>"
                }
            }
    ]
    }
    ```

1. In AWS' Create Role wizard, select _Custom trust policy_.
2. Paste the configured trust policy, then click **Next**.

### Step 3: Configure role permissions

1. Check the boxes to attach at least one permissions policy to your IAM role.
     - Ensure it has sufficient permissions to deploy any resources your IaC code defines.
2. Click **Next**.

!!! info "Info for Terraform users"
    For Terraform users managing their own state file, give your role sufficient permissions to access your state. Terraform documents the [permissions required for S3-managed state](https://www.terraform.io/language/settings/backends/s3#s3-bucket-permissions){: rel="nofollow"} and for [DynamoDB state locking](https://www.terraform.io/language/settings/backends/s3#dynamodb-table-permissions){: rel="nofollow"}.

### Step 4: Create IAM role

1. Enter a **role name** and **description**, then review your configuration.
2. Click **Create role**.
3. Once the role is created, click **View role** or its name in the list.
4. Copy the IAM role _ARN_ to set up the integration in Spacelift.

    ![Copy the listed ARN](<../../assets/screenshots/getting-started/cloud-provider/AWS-ARN.png>)

## Create the cloud integration in Spacelift

1. On the _Cloud integrations_ tab, click **Set up integration**, then choose **AWS** on the dropdown.

    ![Click AWS to access integration settings](<../../assets/screenshots/integrations/cloud-providers/aws/setup-integration-step-2.png>)

2. Fill in the integration details:
      1. **Name**: Enter a name for the cloud integration.
      2. **Space**: Select the space that can access the integration.
      3. **Role ARN**: Paste the ARN copied from the IAM role you created in AWS.
      4. **Assume role on worker**: If enabled, role assumption will be performed on your private worker rather than on Spacelift's end. You can also specify a custom External ID to use during role assumption.
      5. **Duration** (optional): Select how long the role session will last, from 15 minutes to 1 hour (default).
      6. **Region** (optional): Set the AWS regional endpoint to use (such as us-east-2).
      7. **Labels** (optional): Enter a label or labels to help sort your integrations if needed.
3. Click **Set up**.

!!! warning
    If you receive an error message when trying to set up the integration in Spacelift, see [Troubleshooting Trust Relationship Issues](../../integrations/cloud-providers/aws.md#troubleshooting-trust-relationship-issues).

✅ Step 2 of the LaunchPad is complete! Now you can [create your first stack](../create-stack/README.md).

![](<../../assets/screenshots/getting-started/cloud-provider/Launchpad-step-2-complete.png>)
