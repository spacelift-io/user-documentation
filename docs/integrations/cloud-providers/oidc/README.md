# OpenID Connect (OIDC)

{% if is_saas() %}
!!! hint
    This feature is only available to paid Spacelift accounts. Please check out our [pricing page](https://spacelift.io/pricing){: rel="nofollow"} for more information.
{% endif %}

OpenID Connect is a federated identity technology that allows you to exchange short-lived Spacelift credentials for temporary credentials valid for external service providers like AWS, GCP, Azure, HashiCorp Vault etc. This allows you to use Spacelift to manage your infrastructure on these cloud providers without the need of using static credentials.

{% if is_saas() %}
OIDC is also an attractive alternative to our native [AWS](aws-oidc.md), [Azure](azure-oidc.md) and [GCP](gcp-oidc.md) integrations in that it implements a common protocol, requires no additional configuration on the Spacelift side, supports a wider range of external service providers and empowers the user to construct more sophisticated access policies based on JWT claims.
{% else %}
OIDC is also an attractive alternative to our native [AWS](aws-oidc.md) integration in that it implements a common protocol, requires no additional configuration on the Spacelift side, supports a wider range of external service providers and empowers the user to construct more sophisticated access policies based on JWT claims.
{% endif %}

It is not the purpose of this document to explain the details of the OpenID Connect protocol. If you are not familiar with it, we recommend you read the [OpenID Connect specification](https://openid.net/specs/openid-connect-core-1_0.html){: rel="nofollow"} or GitHub's excellent introduction to [security hardening with OpenID Connect](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect){: rel="nofollow"}.

{% if is_self_hosted() %}

## Considerations when Self-Hosting

For this feature to work, the service you are integrating with needs to be able to verify that tokens issued by Spacelift are valid. To do this it needs to be able to access the JWKs used by Spacelift.

The simplest option is to allow the service you are integrating with to access your Spacelift server directly. In this case it will access the `/.well-known/openid-configuration` and `/.well-known/jwks` endpoints on your Spacelift server during the token exchange.

Another option is to manually upload the JWKs (that you can get from the `/.well-known/jwks` endpoint on your Spacelift server) to the service you are integrating with if they support doing so.

{% endif %}

## About the Spacelift OIDC token

The Spacelift OIDC token is a [JSON Web Token](https://jwt.io/){: rel="nofollow"} that is signed by Spacelift and contains a set of claims that can be used to construct a set of temporary credentials for the external service provider. The token is valid for an hour and is available to every run in any paid Spacelift account. The token is available in the `SPACELIFT_OIDC_TOKEN` environment variable and in the `/mnt/workspace/spacelift.oidc` file.

### Standard claims

The token contains the following standard claims:

- `iss` - the issuer of the token - the URL of your Spacelift account, for example `https://demo.app.spacelift.io`. This is unique for each Spacelift account;
- `sub` - the subject of the token - some information about the Spacelift run that generated this token. The subject claim is constructed as follows: `space:<space_id>:(stack|module):<stack_id|module_id>:run_type:<run_type>:scope:<read|write>`. For example, `space:legacy:stack:infra:run_type:TRACKED:scope:write`. Individual values are also available as separate custom claims - see [below](#custom-claims);
- `aud` - the audience of the token - the hostname of your Spacelift account. For example, `demo.app.spacelift.io`. This is unique for each Spacelift account;
- `exp` - the expiration time of the token - the time at which the token will expire, in seconds since the Unix epoch. The token is valid for one hour;
- `iat` - the time at which the token was issued, in seconds since the Unix epoch;
- `jti` - the unique identifier of the token;
- `nbf` - the time before which the token is not valid, in seconds since the Unix epoch. This is always set to the same value as `iat`;

### Custom claims

The token also contains the following custom claims:

- `spaceId` - the ID of the space in which the run that owns the token was executed;
- `callerType` - the type of the caller, ie. the entity that owns the run - either [`stack`](../../../concepts/stack/README.md) or [`module`](../../../vendors/terraform/module-registry.md);
- `callerId` - the ID of the caller, ie. the [stack](../../../concepts/stack/README.md) or [module](../../../vendors/terraform/module-registry.md) that generated the run;
- `runType` - the type of the run ([`PROPOSED`](../../../concepts/run/proposed.md), [`TRACKED`](../../../concepts/run/tracked.md), [`TASK`](../../../concepts/run/task.md), [`TESTING`](../../../concepts/run/test-case.md) or [`DESTROY`](../../../concepts/run/test-case.md);
- `runId` - the ID of the run that owns the token;
- `scope` - the scope of the token - either `read` or `write`.

### About scopes

Whether the token is given `read` or `write` scope depends on the type of the run that generated the token. [Proposed](../../../concepts/run/proposed.md) runs get a `read` scope, while [tracked](../../../concepts/run/tracked.md), [testing](../../../concepts/run/test-case.md) and [destroy](../../../concepts/run/test-case.md) runs as well as [tasks](../../../concepts/run/task.md) get a `write` scope. The only exception to that rule are tracked runs whose stack is not set to [autodeploy](../../../concepts/run/tracked.md#approval-flow). In that case, the token will have a `read` scope during the planning phase, and a `write` scope during the apply phase. This is because we know in advance that the tracked run requiring a manual approval should not perform write operations before human confirmation.

Note that the scope claim, as well as other claims presented by the Spacelift token are merely advisory. It depends on you whether you want to control access to your external service provider based on the scope of the token or on some other claim like space, caller or run type. In other words, Spacelift just gives you the data and it's up to you to decide whether and how to use it.

## Using the Spacelift OIDC token

You can follow guidelines under this section to see how to use the Spacelift OIDC token to authenticate with [AWS](aws-oidc.md), [GCP](gcp-oidc.md), [Azure](azure-oidc.md), and [HashiCorp Vault](vault-oidc.md). In particular, we will focus on setting up the integration and using it from these services' respective OpenTofu/Terraform providers
