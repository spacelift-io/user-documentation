# HashiCorp Vault

## Configuring Spacelift as an Identity Provider

In order to enable Spacelift runs to access Vault, you need to set up Spacelift as a valid identity provider for your Vault instance. This is done using [Vault's OIDC auth method](https://www.vaultproject.io/docs/auth/jwt){: rel="nofollow"}. The set up process involves creating a role in Vault that tells Vault which Spacelift runs should be able to access which Vault secrets. This process can be completed via the Vault CLI or Terraform. For illustrative purposes we will use the Vault CLI.

If you haven't enabled the JWT auth method in your Vault instance, you need to do so first. To do this, run the following command:

```bash
vault auth enable jwt
```

In the next step, we need to add configuration for your Spacelift account as an identity provider. To do this, run the following command:

```bash
vault write auth/jwt/config \
  bound_issuer="https://demo.app.spacelift.io" \
  oidc_discovery_url="https://demo.app.spacelift.io"
```

The `bound_issuer` parameter is the URL of your Spacelift account which is used as the issuer claim in the OIDC token you receive from Spacelift. The `oidc_discovery_url` parameter is the URL of the OIDC discovery endpoint for your Spacelift account, which is in this case identical to the `bound_issuer` parameter.

Next, you will need to create a policy that will be used to determine which Spacelift runs can access which Vault secrets. For example, the following policy allows all Spacelift runs to read any secret in the `secrets/preprod` path:

```bash
vault policy write infra-preprod - <<EOF
path "secrets/preprod/*" {
  capabilities = ["read"]
}
EOF
```

Last but not least, you will need to create a role that binds the policy to the identity provider. The following command creates a role called `infra-preprod` that binds the `infra-preprod` policy to the JWT identity provider:

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

The `bound_audiences` parameter is the hostname of your Spacelift account, which is used as the audience claim in the OIDC token you receive from Spacelift. The `bound_claims` parameter is a JSON object that contains the claims that the OIDC token must contain in order to be able to access the Vault secrets. How you scope this will very much depend on your use case. In the above example, only runs belonging to a stack or module in the `spaceId` claim can assume "infra-preprod" Vault role. You can refer to this document to see the available [standard](README.md#standard-claims) and [custom claims](README.md#custom-claims) presented by the Spacelift OIDC token.

## Configuring the Terraform Provider

Once the Vault setup is complete, you need to configure the [Terraform Vault provider](https://registry.terraform.io/providers/hashicorp/vault/latest){: rel="nofollow"} to use the Spacelift OIDC JWT token to assume a particular role. To do this, you will provide the [`auth_login_jwt` configuration block](https://registry.terraform.io/providers/hashicorp/vault/latest/docs#jwt){: rel="nofollow"} to the provider, and set the `role` parameter to the name of the role you created in the previous section:

```hcl
provider "vault" {
  # ... other configuration
  skip_child_token = true
  auth_login_jwt {
    role = "infra-preprod"
  }
}
```

Next, set the `TERRAFORM_VAULT_AUTH_JWT` environment variable to `${SPACELIFT_OIDC_TOKEN}`, either directly on your stack, or on one of the attached [contexts](../../../concepts/configuration/context.md). This approach uses [interpolation](../../../concepts/configuration/environment.md#environment-variable-interpolation) to dynamically set the value of the variable the provider is looking for to the value of the environment variable that Spacelift provides.
