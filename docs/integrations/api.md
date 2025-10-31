---
description: Describes how to authenticate and use the Spacelift GraphQL API.
---

# GraphQL API

## GraphQL

GraphQL is a query language for APIs and a runtime for fulfilling those queries with your existing data. GraphQL:

- Provides a complete and understandable description of the data in your API.
- Gives clients the power to ask for exactly what they need and nothing more.
- Makes it easier to evolve APIs over time.
- Enables powerful developer tools.

Spacelift provides a [GraphQL API](https://graphql.org/){: rel="nofollow"} for you to control your Spacelift account programmatically and/or through an API Client if you choose to do so. A smaller subset of this API is also used by the Spacelift [Terraform provider](../vendors/terraform/terraform-provider.md), as well as the Spacelift CLI ([spacectl](https://github.com/spacelift-io/spacectl){: rel="nofollow"}). The API can be accessed at the `/graphql` endpoint of your account using `POST` HTTPS method.

!!! tip "Quick start with AI coding assistants"
    The fastest way to build applications against our API is using a coding assistant with our MCP server. You don't need to learn the GraphQL API because the assistant discovers it automatically. See [API development with MCP](api-development-with-mcp.md) for setup instructions.

### Example request and response

```curl
$ curl --request POST \
  --url https://<account-name>.app.spacelift.io/graphql \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{"query":"{ stacks { id name, createdAt, description }}"}'
```

The request body looks like this when formatted a bit nicer:

```graphql
{
  stacks
  {
    id
    name,
    createdAt,
    description
  }
}
```

And the response looks like this:

```json
{
  "data": {
    "stacks": [
      {
        "id": "my-stack-1",
        "name": "My Stack 1",
        "createdAt": 1672916942,
        "description": "The is my first stack"
      },
      {
        "id": "my-stack-2",
        "name": "My Stack 2",
        "createdAt": 1674218834,
        "description": "The is my second stack"
      }
    ]
  }
}
```

### What tool should I use to authenticate?

Our recommendation is to use the [Spacelift API Key](api.md#spacelift-api-key) to authenticate with the GraphQL API.

Our tool of choice is [Insomnia](https://insomnia.rest/download){: rel="nofollow"}, a free, open-source tool that allows you to easily create and manage API requests. You can also use [Postman](https://www.postman.com/downloads/){: rel="nofollow"}, but the walkthrough in this guide will be based on Insomnia.

## View the GraphQL schema

Our GraphQL schema is self-documenting. The best way to view the latest documentation is using a dedicated GraphQL client like [Insomnia](https://insomnia.rest/){: rel="nofollow"} or [GraphiQL](https://github.com/skevy/graphiql-app){: rel="nofollow"}. You can also view the documentation using a static documentation website generator like [GraphDoc](https://graphdoc.io/preview/?endpoint=https://demo.app.spacelift.io/graphql){: rel="nofollow"}.

Make sure to provide a valid JWT bearer token as described in [Authenticating with the GraphQL API](api.md#authenticating-with-the-graphql-api).

!!! note

    The latest version of Postman does not currently support viewing GraphQL Schemas from a URL, but does support autocompletion.

### Insomnia

1. Enter the GraphQL Endpoint for _your_ Spacelift account.
2. Click **Schema**, then **Show Documentation**.
  ![Example viewing GraphQL documentation using Insomnia.](<../assets/screenshots/Spacelift_–_GraphQL.png>)

### GraphiQL

1. Enter the GraphQL Endpoint for _your_ Spacelift Account, then click **Docs**.
    ![Click docs](<../assets/screenshots/1-graphiql.png>)
2. Use the Documentation Explorer within GraphiQL.
    ![Explore docs](<../assets/screenshots/2-graphiql-view-docs.png>)

## Example usage

In this example, we'll generate your Spacelift token with spacectl and use it to communicate with Spacelift.

!!! tip "Prerequisites:"

      - [Insomnia](https://insomnia.rest/download){: rel="nofollow"} downloaded and installed.
      - Spacelift account with admin access (for ability to create API Keys).

<!-- markdownlint-disable-next-line MD033 -->
<div style="position: relative; padding-bottom: 56.25%; height: 0;"><iframe src="https://www.loom.com/embed/1cefc584b1bc41d7bc75d767afaf3916" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>

## Authenticating with the GraphQL API

If your Spacelift account were called `example`, you could access your GraphQL by sending **POST** requests to: `https://example.app.spacelift.io/graphql`.

All requests need to be authenticated using a [JWT](https://jwt.io/){: rel="nofollow"} bearer token. There are currently three ways of obtaining this token:

1. [Spacelift API Key](api.md#spacelift-api-key): For long-term use (**recommended**).
2. [SpaceCTL CLI](api.md#spacectl-cli): For temporary use.
3. [Personal GitHub Token](api.md#personal-github-token)

### Spacelift API key

You can generate the JWT token with a Spacelift API key, ideal for long-term use. Spacelift supports creating and managing machine users with programmatic access to the Spacelift GraphQL API. These "machine users" are called API Keys and can be created by Spacelift admins through the _Settings_ panel.

There are two types of API keys: more traditional, secret-based keys, and keys based on OIDC identity federation.

!!! tip "API key billing"
    API keys are **virtual users** and are billed like regular users, too. Thus, **each API key used** (exchanged for a token) during any given billing cycle counts against the total number of users.

#### Secret-based API keys

Secret-based keys exchange an API key ID and secret for a JWT token, identical to how IAM user keys work. They're more flexible, but less secure because they involve static credentials. Here is how to create a secret-based API key in the Spacelift UI:

1. In the lower right hand corner menu, click your account name and select **Organization settings**.
    ![Click organization settings](<../assets/screenshots/organization-settings.png>)
2. In the _Access_ section, click **API keys**, then **Create API key**.
    ![Create API key](<../assets/screenshots/create-api-key-button.png>)
3. Fill in the details for your API key:
    ![Fill in API key details](<../assets/screenshots/create-api-key-drawer.png>)
      - **Name**: An arbitrary key name. We recommend you choose something memorable, ideally reflecting the purpose of the key.
      - **Type**: Select **Secret**.
      - **Space**: Select the [spaces](../concepts/spaces/README.md) the key should have access to, along with access level (reader vs writer). If you are using [login policies](../concepts/policy/login-policy.md), you will need to define the API key in the policy for non-admin keys.
      - **Groups**: Enter the group(s) the key should belong to. Groups give the API key a virtual group membership for scenarios where you'd prefer to control access to resources on group/team level rather than individual level.
4. Click **Create**. The API key will be generated in a file and automatically downloaded to your device.

    ![Download the file](<../assets/screenshots/api-key-creation-04.png>)

      - The file contains the API token in two forms: one to be used with our API, and the other as a `.terraformrc` snippet to access your [private modules](../vendors/terraform/module-registry.md) outside of Spacelift.

!!! note
    Giving "admin" permissions on the "root" space makes the key **administrative**.

The config file looks something like this:

```text
# Spacelift API Key Configuration

[credentials]
api_key_id     = ID_VALUEW2EWGQ9F7AVF41CG1
api_key_secret = SECRET_VALUE40ffc46887297384892384789239

# Usage Options:
#
# - Programmatic Access:
#   Use the api_key_secret above in your API calls
#
# - UI Login:
#   Visit /apikeytoken and enter the credentials above

# Terraform Module Access:
# Add this snippet to your .terraformrc file to access 
# Spacelift-hosted Terraform modules outside of Spacelift:

credentials "spacelift.io" {
  token = "TOKEN_VALUEQwZmZjNDY4ODdiMjI2ZWE4NDhjMWQwNWZiMWE5MGU4NWMwZTFlY2Q4NDAxMGI2ZjA2NzkwMmI1YmVlMWNmMGE"
}
```

!!! warning
    Make sure you save this data somewhere on your end. Spacelift doesn't store the token, and it cannot be retrieved or recreated afterwards.

For programmatic access, exchange the key ID and secret pair for an API token using a GraphQL mutation:

```graphql
mutation GetSpaceliftToken($id: ID!, $secret: String!) {
  apiKeyUser(id: $id, secret: $secret) {
    jwt
  }
}
```

Once you obtain the token, you can use it to authenticate your requests to the Spacelift API.

#### OIDC-based API keys

{% if is_saas() %}
!!! Info
    This feature is only available on our Enterprise plan. Please check out our [pricing page](https://spacelift.io/pricing){: rel="nofollow"} for more information.
{% endif %}

OIDC-based API keys are a more secure alternative to secret-based API keys. They're based on the OpenID Connect protocol and are more secure because they don't involve static credentials. They're also more flexible because they can be used to authenticate with Spacelift using any OIDC identity provider.

1. In the lower right hand corner menu, click your account name and select **Organization settings**.
    ![Click organization settings](<../assets/screenshots/organization-settings.png>)
2. In the _Access_ section, click **API keys**, then **Create API key**.
    ![Create API key](<../assets/screenshots/create-api-key-button.png>)
3. Fill in the details for your API key:
    ![Fill in API key details](<../assets/screenshots/create-oidc-api-key.png>)
      - **Name**: An arbitrary key name. We recommend you choose something memorable, ideally reflecting the purpose of the key.
      - **Type**: Select **OIDC**.
      - **Issuer**: The URL your OIDC provider reports as the token issuer in the `iss` claim of your JWT token. For GitHub Actions, this is `https://token.actions.githubusercontent.com`.
      - **Client ID (audience)**: The client ID of the OIDC application you created in the identity provider, in the `aud` claim of your JWT token. Some identity providers allow this to be customized.
      - **Subject Expression**: A regular expression that needs to match the `sub` claim of your JWT token. Use this to restrict API key access to a specific source.
      - **Space**: Select the [spaces](../concepts/spaces/README.md) the key should have access to, along with access level (reader vs writer). If you are using [login policies](../concepts/policy/login-policy.md), you will need to define the API key in the policy for non-admin keys.
      - **Groups**: Enter the group(s) the key should belong to. Groups give the API key a virtual group membership for scenarios where you'd prefer to control access to resources on group/team level rather than individual level.
4. Click **Create**. The API key will be generated in a file and automatically downloaded to your device.

!!! warning
    Make sure you save the data in your API key file somewhere on your end. Spacelift doesn't store the token, and it cannot be retrieved or recreated afterwards.

Here is a sample workflow using the key we just created and [spacectl](../concepts/spacectl.md) in GitHub Actions, without the need for any static credentials:

{% raw %}

```yaml
name: List Spacelift stacks

on: [push]

jobs:
  test:
    name: List Spacelift stacks
    runs-on: ubuntu-latest
    permissions:
      contents: 'read'
      id-token: 'write'

    steps:
      - name: Generate token
        run: |
          OIDC_TOKEN=$(curl -H "Authorization: bearer $ACTIONS_ID_TOKEN_REQUEST_TOKEN" "$ACTIONS_ID_TOKEN_REQUEST_URL&audience=myorg.app.spacelift.io" | jq --raw-output '.value')
          echo "OIDC_TOKEN=$OIDC_TOKEN" >> $GITHUB_ENV

      - name: Install spacectl
        uses: spacelift-io/setup-spacectl@main

      - name: List stacks
        env:
          # You will want to replace this endpoint (and the audience) with your
          # own Spacelift account's endpoint.
          SPACELIFT_API_KEY_ENDPOINT: https://myorg.app.spacelift.io
          SPACELIFT_API_KEY_ID: ${{ env.SPACELIFT_KEY_ID }}
          SPACELIFT_API_KEY_SECRET: ${{ env.OIDC_TOKEN }}
        run: |
          spacectl whoami
          spacectl stack list
```

{% endraw %}

For programmatic access, exchange the key ID and secret pair for an API token using a GraphQL mutation:

```graphql
mutation GetSpaceliftToken($id: ID!, $secret: String!) {
  apiKeyUser(id: $id, secret: $OIDC_TOKEN) {
    jwt
  }
}
```

Once you obtain the token, you can use it to authenticate your requests to the Spacelift API.

!!! note
    OIDC-based API keys do not provide special access to OpenTofu/Terraform modules. They are only used to authenticate with the Spacelift API.

### SpaceCTL CLI

You can generate the JWT token using the Spacelift [spacectl](https://github.com/spacelift-io/spacectl) CLI. We consider this the easiest method, as the heavy lifting to obtain the token is done for you.

1. Follow the instructions on the `spacectl` [GitHub repository](https://github.com/spacelift-io/spacectl){: rel="nofollow"} to install the CLI on your machine.
2. Authenticate to your Spacelift account using `spacectl profile login`.
3. Once authenticated, run `spacectl profile export-token` to receive the bearer token needed for future GraphQL queries/mutations.

### Personal GitHub token

!!! info
    This option is only available to accounts using GitHub as their identity provider. If you have enabled any other [Single Sign-On methods](single-sign-on/README.md) on your account, this method will not work and you will need to use the [Spacelift API Key](api.md#spacelift-api-key) method instead.

1. Using a GitHub Account that has access to your Spacelift account, [create a GitHub Personal Access Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token){: rel="nofollow"}.
2. Copy the value of the token to a secure location.
3. Using your favorite API Client (e.g. [Insomnia](https://insomnia.rest/){: rel="nofollow"} or [GraphiQL](https://github.com/skevy/graphiql-app){: rel="nofollow"}), make a GraphQL POST request to your account's GraphQL endpoint (example below).

#### Request details

**POST** to `https://example.app.spacelift.io/graphql`. Replace "example" with your Spacelift account name.

##### Query

Pass in **token** as a query variable for this example. When making a GraphQL query with your favorite API Client, you should see a section called GraphQL variables where you can pass in an input.

```graphql
mutation GetSpaceliftToken($token: String!) {
  oauthUser(token: $token) {
    jwt
  }
}
```

##### GraphQL variables input

```graphql
{
    "token": "PASTE-TOKEN-VALUE-HERE"
}
```

This query should return your JWT bearer token, which you can use to authenticate other queries by using it as the bearer token in your requests. If you want to automatically access the API reliably, we suggest the [Spacelift API Key](api.md#spacelift-api-key) approach, as Spacelift tokens expire after 1 hour.

## Insomnia setup

You can create request libraries in Insomnia to make it easier to work with the Spacelift API. You can also automate the JWT token generation process using the [Environment Variables](https://docs.insomnia.rest/insomnia/environment-variables){: rel="nofollow"} feature.

### Copy the schema

Copy the following JSON to your clipboard:

??? note "Click here to expand"

{% raw %}

    ```json
    {
        "_type": "export",
        "__export_format": 4,
        "__export_date": "2023-01-23T19:49:05.605Z",
        "__export_source": "insomnia.desktop.app:v2022.7.0",
        "resources": [
      {
              "_id": "req_d7fb83c13cc945da9e21cd9b94722d3d",
              "parentId": "wrk_3b73a2a7403445a48acdc8396803c4e8",
              "modified": 1674497188638,
              "created": 1656577781496,
              "url": "{{ _.BASE_URL }}/graphql",
              "name": "Authentication - Get JWT",
              "description": "",
              "method": "POST",
              "body": {
                  "mimeType": "application/graphql",
                  "text": "{\"query\":\"mutation GetSpaceliftToken($keyId: ID!, $keySecret: String!) {\\n  apiKeyUser(id: $keyId, secret: $keySecret) {\\n    id\\n\\t\\tjwt\\n  }\\n}\",\"variables\":{\"keyId\":\"{{ _.API_KEY_ID }}\",\"keySecret\":\"{{ _.API_KEY_SECRET }}\"},\"operationName\":\"GetSpaceliftToken\"}"
              },
              "parameters": [],
              "headers": [
                  {
                      "name": "Content-Type",
                      "value": "application/json",
                      "id": "pair_85e4a9afc2e6491ca59b52f77d94e81f"
                  }
              ],
              "authentication": {},
              "metaSortKey": -1656577781496,
              "isPrivate": false,
              "settingStoreCookies": true,
              "settingSendCookies": true,
              "settingDisableRenderRequestBody": false,
              "settingEncodeUrl": true,
              "settingRebuildPath": true,
              "settingFollowRedirects": "global",
              "_type": "request"
          },
          {
              "_id": "wrk_3b73a2a7403445a48acdc8396803c4e8",
              "parentId": null,
              "modified": 1656576979763,
              "created": 1656576979763,
              "name": "Spacelift",
              "description": "",
              "scope": "collection",
              "_type": "workspace"
          },
          {
              "_id": "req_83de84158a16459fa4bfce6042859df6",
              "parentId": "wrk_3b73a2a7403445a48acdc8396803c4e8",
              "modified": 1674497166036,
              "created": 1656577541263,
              "url": "{{ _.BASE_URL }}/graphql",
              "name": "Get Stacks",
              "description": "",
              "method": "POST",
              "body": {
                  "mimeType": "application/graphql",
                  "text": "{\"query\":\"{ \\n\\tstacks\\n\\t{\\n\\t\\tid\\n\\t\\tname,\\n\\t\\tcreatedAt,\\n\\t\\tdescription\\n\\t}\\n}\"}"
              },
              "parameters": [],
              "headers": [
                  {
                      "name": "Content-Type",
                      "value": "application/json",
                      "id": "pair_80893dda7c0f4266b48bd09d0eaa3222"
                  }
              ],
              "authentication": {
                  "type": "bearer",
                  "token": "{{ _.API_TOKEN }}"
              },
              "metaSortKey": -1656577721437.75,
              "isPrivate": false,
              "settingStoreCookies": true,
              "settingSendCookies": true,
              "settingDisableRenderRequestBody": false,
              "settingEncodeUrl": true,
              "settingRebuildPath": true,
              "settingFollowRedirects": "global",
              "_type": "request"
          },
          {
              "_id": "env_36e5a9fc63b6443ed4d0a656800d202bcd1f5286",
              "parentId": "wrk_3b73a2a7403445a48acdc8396803c4e8",
              "modified": 1660646140956,
              "created": 1656576979773,
              "name": "Base Environment",
              "data": {},
              "dataPropertyOrder": {},
              "color": null,
              "isPrivate": false,
              "metaSortKey": 1656576979773,
              "_type": "environment"
          },
          {
              "_id": "jar_36e5a9fc63b6443ed4d0a656800d202bcd1f5286",
              "parentId": "wrk_3b73a2a7403445a48acdc8396803c4e8",
              "modified": 1656576979775,
              "created": 1656576979775,
              "name": "Default Jar",
              "cookies": [],
              "_type": "cookie_jar"
          },
          {
              "_id": "spc_dbcf993f70b44bb18eee1b2362bb5bdc",
              "parentId": "wrk_3b73a2a7403445a48acdc8396803c4e8",
              "modified": 1656576979770,
              "created": 1656576979770,
              "fileName": "Spacelift",
              "contents": "",
              "contentType": "yaml",
              "_type": "api_spec"
          },
          {
              "_id": "env_ea5c30c23af449f792c71d160678eff5",
              "parentId": "env_36e5a9fc63b6443ed4d0a656800d202bcd1f5286",
              "modified": 1669716444669,
              "created": 1669716373608,
              "name": "Spacelift",
              "data": {
                  "BASE_URL": "https://ACCOUNT_NAME.app.spacelift.io",
                  "API_KEY_ID": "insert-your-real-api-key-here",
                  "API_KEY_SECRET": "insert-your-real-api-secret-here",
                  "API_TOKEN": "{% response 'body', 'req_d7fb83c13cc945da9e21cd9b94722d3d', 'b64::JC5kYXRhLmFwaUtleVVzZXIuand0::46b', 'never', 60 %}"
              },
              "dataPropertyOrder": {
                  "&": [
                      "BASE_URL",
                      "API_KEY_ID",
                      "API_KEY_SECRET",
                      "API_TOKEN"
                  ]
              },
              "color": "#6b84ff",
              "isPrivate": false,
              "metaSortKey": 828288489886.5,
              "_type": "environment"
            }
        ]
    }
    ```

{% endraw %}

### Paste the schema into Insomnia

1. On Insomnia's home screen, click **Import From**, then **Clipboard**.
    ![Import from clipboard](<../assets/screenshots/graphql-insomnia-01-import.png>)
2. Click on the _Spacelift_ collection when it appears.
3. In the top left corner, click **Spacelift**, then **Manage Environments**.
    ![Manage environments](<../assets/screenshots/graphql-insomnia-02-manage-envs.png>)
4. Fill in the first three variables:
    ![Fill in variables](<../assets/screenshots/graphql-insomnia-fill-vars.png>)
      - `BASE_URL`: The URL of your Spacelift account. For example, `https://my-account.app.spacelift.io`.
      - `API_KEY_ID`: The ID of the [API key you created](#authenticating-with-the-graphql-api), a 26-character [ULID](https://github.com/ulid/spec){: rel="nofollow"}.
      - `API_KEY_SECRET`: Found in the file that was downloaded when you created the API key.
      - `API_TOKEN`: Leave this field as it is.

That's it! Now you can send an `Authentication - Get JWT` request, which populates the `API_TOKEN` environment variable. Then you can send the `Get Stacks` request to see the list of stacks in your account.

If you want to create another request, just right-click on `Get Stacks` and duplicate it. Then, change the query to whatever you want.

!!! hint
    Don't forget that the JWT expires after 10 hours. Run the authentication request again to get a new one.
