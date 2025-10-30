# HashiCorp Vault

{% if is_saas() %}
!!! hint
    This feature is only available to paid Spacelift accounts. Please check out our [pricing page](https://spacelift.io/pricing){: rel="nofollow"} for more information.
{% endif %}

## Configure Spacelift as an Identity Provider

Set up Spacelift as a valid identity provider for your Vault instance to allow Spacelift runs access to Vault resources. This is done using [Vault's OIDC auth method](https://www.vaultproject.io/docs/auth/jwt){: rel="nofollow"}.

The setup process involves creating a role in Vault that tells Vault which Spacelift runs should be access which Vault secrets. This process can be completed via the Vault CLI or Terraform. For illustrative purposes we will use the Vault CLI.

First, if you haven't enabled the JWT auth method in your Vault instance yet, run the following command:

```bash
vault auth enable jwt
```

### Add Spacelift as an identity provider

1. Run the following command:

    ```bash
    vault write auth/jwt/config \
      bound_issuer="https://demo.app.spacelift.io" \
      oidc_discovery_url="https://demo.app.spacelift.io"
    ```

2. The `bound_issuer` parameter is the URL of your Spacelift account, which is used as the issuer claim in the OIDC token you receive from Spacelift.
3. The `oidc_discovery_url` parameter is the URL of the OIDC discovery endpoint for your Spacelift account, which is (in this case) identical to the `bound_issuer` parameter.
4. Create a policy to determine which Spacelift runs can access which Vault secrets. For example, the following policy allows all Spacelift runs to read any secret in the `secrets/preprod` path:

    ```bash
    vault policy write infra-preprod - <<EOF
    path "secrets/preprod/*" {
      capabilities = ["read"]
    }
    EOF
    ```

### Create role to bind policy to identity provider

1. The following command creates a role called `infra-preprod` that binds the `infra-preprod` policy to the JWT identity provider:

    ```bash
    vault write auth/jwt/role/infra-preprod -<<EOF
    {
      "role_type": "jwt",
      "user_claim": "iss",
      "bound_audiences": "demo.app.spacelift.io",
      "bound_claims": { "spaceId": "preprod" },
      "policies": ["infra-preprod"],
      "ttl": "10m"
    }
    EOF
    ```

2. The `bound_audiences` parameter is the hostname of your Spacelift account, which is used as the audience claim in the OIDC token you receive from Spacelift.
3. The `bound_claims` parameter is a JSON object that contains the claims that the OIDC token must contain in order to be able to access the Vault secrets. How you scope this will very much depend on your use case.

In the above example, only runs belonging to a stack or module in the `spaceId` claim can assume the "infra-preprod" Vault role. You can refer to our documentation to see available [standard](README.md#standard-claims) and [custom claims](README.md#custom-claims) presented by the Spacelift OIDC token.

## Configure the Terraform Provider

Once the Vault setup is complete, you need to configure the [Terraform Vault provider](https://registry.terraform.io/providers/hashicorp/vault/latest){: rel="nofollow"} to use the Spacelift OIDC JWT token to assume a particular role.

1. Provide the [`auth_login_jwt` configuration block](https://registry.terraform.io/providers/hashicorp/vault/latest/docs#jwt){: rel="nofollow"} to the provider.
2. Set the `role` parameter to the name of the role you created in the previous section:

    ```hcl
    provider "vault" {
      # ... other configuration
      skip_child_token = true
      auth_login_jwt {
        role = "infra-preprod"
      }
    }
    ```

3. Set the `TERRAFORM_VAULT_AUTH_JWT` environment variable to `${SPACELIFT_OIDC_TOKEN}`, either directly on your stack, or on one of the attached [contexts](../../../concepts/configuration/context.md).
      - This approach uses [interpolation](../../../concepts/configuration/environment.md#environment-variable-interpolation) to dynamically set the value of the variable the provider is looking for to the value of the environment variable that Spacelift provides.
