# Amazon Web Services (AWS)

{% if is_saas() %}
!!! hint
    This feature is only available to paid Spacelift accounts. Please check out our [pricing page](https://spacelift.io/pricing){: rel="nofollow"} for more information.
{% endif %}

!!! warning
    Until Terraform and OpenTofu versions 1.6.0, the [AWS S3 state backend](https://developer.hashicorp.com/terraform/language/settings/backends/s3){: rel="nofollow"} did not support authenticating with OIDC.

    If you need to use the AWS S3 state backend with older versions, you can use the following workaround:

    - Add the following command as a [`before_init` hook](../../../concepts/stack/stack-settings.md#customizing-workflow) (make sure to replace `<ROLE ARN>` with your IAM role ARN).

    ```shell
    export $(printf "AWS_ACCESS_KEY_ID=%s AWS_SECRET_ACCESS_KEY=%s AWS_SESSION_TOKEN=%s" $(aws sts assume-role-with-web-identity --web-identity-token "$(cat /mnt/workspace/spacelift.oidc)" --role-arn <ROLE ARN> --role-session-name spacelift-run-${TF_VAR_spacelift_run_id} --query "Credentials.[AccessKeyId,SecretAccessKey,SessionToken]" --output text))
    ```

    - Comment out the `role_arn` argument in the `backend` block.
    - Comment out the `assume_role_with_web_identity` section in the AWS provider block.

    Alternatively, you can use the dedicated [AWS Cloud Integration](../aws.md) that uses AWS STS to obtain temporary credentials.

## Configure Spacelift as an identity provider

You need to set up Spacelift as a valid identity provider for your AWS account. This is done by creating an [OpenID Connect identity provider](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html){: rel="nofollow"}. You can do it declaratively using any of the IaC providers, programmatically using the [AWS CLI](https://aws.amazon.com/cli/){: rel="nofollow"}, or with the console.

For illustrative purposes, we will use the console:

1. Go to the [AWS console](https://console.aws.amazon.com/iam/home#/home){: rel="nofollow"} and select the IAM service.
2. Click **Identity providers** in the left-hand menu.
3. Click **Add provider** in the top bar.
    ![Add provider](<../../../assets/screenshots/oidc/aws-iam-add-provider.png>)
4. Select **OpenID Connect** as the provider type.
    ![Configure provider](<../../../assets/screenshots/oidc/aws-iam-configure-provider.png>)
5. Click **Get thumbprint**. This is required by AWS and protects you from a certain class of MitM attacks.

!!! hint
    Add [iss](README.md#standard-claims) to _Provider URL_ and you will need to add [aud](README.md#standard-claims) to _Audience_.

    Replace `demo.app.spacelift.io` with the hostname of your Spacelift account.

Once created, the identity provider will be listed in the "Identity providers" table.

### Add Spacelift OIDC as the role provider

You can click on the provider name to see the details. From here, you will also be able to assign an IAM role to this new identity provider:

![Provider details](<../../../assets/screenshots/oidc/aws-iam-provider-details.png>)

1. Click **Assign role**, and choose to create a new role.
2. Click **Web identity** and select the new Spacelift OIDC provider as the trusted entity.
3. Select the audience from the dropdown (there should only be one option).
    ![Choosing role provider](<../../../assets/screenshots/oidc/aws-iam-choosing-role-provider.png>)
4. The rest of the process is the same as for any other role creation. Select the policies you want to attach to the role, and add tags and a description.
5. Once you're done, click **Create role**.

If you go to your new role's details page, in the _Trust relationships_ section you will notice that it is now associated with the Spacelift OIDC provider:

![Trust relationship](<../../../assets/screenshots/oidc/aws-iam-trust-relationship.png>)

This trust relationship is very relaxed and will allow any stack or module in the `demo` Spacelift account to assume this role. If you want to be more restrictive, you will want to add more conditions. For example, we can restrict the role to be only assumable by stacks in the `production` space (with space ID `production-01HND497T9JKR76MR3KA2CDJHP`) by adding the following condition:

```json
"StringLike": {
  "demo.app.spacelift.io:sub": "space:production-01HND497T9JKR76MR3KA2CDJHP:*"
}
```

!!! hint
    You will need to replace `demo.app.spacelift.io` with the hostname of your Spacelift account.

You can also restrict the role so only a specific stack can assume it, using the stack ID:

```json
"StringLike": {
  "demo.app.spacelift.io:sub": "*:stack:oidc-is-awesome:*"
}
```

You can mix and match these to get the exact constraints you need. You can learn more about the intricacies of AWS IAM conditions in the [official docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition.html){: rel="nofollow"}. Remember that AWS does not seem to support custom claims, so you will need to use the standard ones to do the matching (primarily `sub`, as shown above).

The full `sub` is constructed as follows:

* Format: `space:<space_id>:(stack|module):<stack_id|module_id>:run_type:<run_type>:scope:<read|write>`
* For example: `space:legacy-01KJMM56VS4W3AL9YZWVCXBX8D:stack:infra:run_type:TRACKED:scope:write`

## Configure the Terraform provider

Once the Spacelift-AWS OIDC integration is set up, the Terraform provider can be configured without the need for any static credentials. The `aws_role_arn` variable should be set to the ARN of the role that you want to assume:

```hcl
provider "aws" {
  assume_role_with_web_identity {
    role_arn = var.aws_role_arn
    web_identity_token_file = "/mnt/workspace/spacelift.oidc"
  }
}
```
