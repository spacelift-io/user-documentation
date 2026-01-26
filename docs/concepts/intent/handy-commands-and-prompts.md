# Handy commands & prompts

## Add MCP server (CLI)

```bash
claude mcp add intent-mcp -t http https://<account-name>.app.spacelift.io/intent/mcp
```

## Auth & status

- `/mcp` → select **intent-mcp** → log in → verify **connected**

## Project management (via prompts)

```text
Create a project called "my-project".
Use the project "my-project".
List my projects and their lock status.
Unlock the current project.
```

## Resources (via prompts)

```text
Create two resources — one very long random string and a cute pet.
Create an S3 bucket named "dev-attachments-123" with SSE enabled.
Create a t3.micro EC2 instance in us-east-1.  # expect policy denial with example policy
List resources in this project.
Delete the random resources we created earlier.
```

## Import (via prompts)

```text
List SSM parameters in my account and import them into the project.
```

_Use concise, explicit prompts; include environment/region and compliance requirements in your wording to help the agent make safer defaults._
