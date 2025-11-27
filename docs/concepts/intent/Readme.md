# Spacelift Intent

## What Is Spacelift Intent?

**Spacelift Intent** lets you provision and manage infrastructure by describing what you need in natural language. Instead of writing Terraform/OpenTofu code, your MCP client (e.g. Claude Code) calls Spacelift Intent, which directly interacts with provider schemas under Spacelift’s guardrails (policies, audit trail, state, permissions).

### **Key concepts**

- **Natural language**: Describe your infrastructure needs in natural language; Intent translates it directly into the infrastructure you want.
- **Policies**: Spacelift enforces governance (OPA/Rego policies) before execution to deny unsafe operations and allow compliant ones.
- **State & audit built-in**: Centralize state management and view the complete operation history without manual backend configuration.
- **Separate policy writing & resource changes:** With [Spaces](../spaces/README.md) and our [access control features](../authorization/rbac-system.md), you can assign precise roles and permissions so authors and operators stay clearly separated.

### **Architecture (high level)**

Spacelift Intent connects your AI client to your cloud infrastructure through a secure, policy-governed pipeline:

1. **MCP Client (Claude Code, ChatGPT, VS Code, etc.):** You describe infrastructure in natural language.
2. **Intent MCP Serve**r: Translates requests into provider operations, discovers Terraform providers from OpenTofu registry, learns resource schemas.
3. **Spacelift Control Plane:** Enforces policies (OPA/Rego), manages state, records audit history, handles cloud authentication, provides resource visibility.
4. **Cloud Providers (AWS, etc.):** Executes approved operations via cloud integrations with scoped permissions.
💡

**Key flow:** You send a natural language prompt describing infrastructure changes. Intent interprets the request, discovers relevant Terraform providers from the OpenTofu registry, and learns their schemas to plan operations. Attached policies then evaluate the plan against governance rules—allowing or denying based on resource types, operations, or attributes.

If approved, Intent executes changes via cloud integrations with scoped credentials. State updates automatically and full operation history is recorded for audit and rollback.

![High-level architecture of Spacelift Intent](../../assets/screenshots/spacelift-intent/intent.png)

---

## Supported clients & endpoint

- **MCP server URL:** `https://<account-name>.app.spacelift.io/intent/mcp`
- **Tested clients:** Claude Code, Claude Desktop (custom connectors), [claude.ai](http://claude.ai)
- **Coming soon:** VS Code, Cursor

---

## Prerequisites

- **Claude Code**
- **Spacelift account** with access to Intent
    - for Early Access, we require `root` space admin access
- _(Optional for AWS tests)_ An **AWS account**
- [**AWS integration** configured in Spacelift](../../getting-started/integrate-cloud/AWS.md) if you plan to create AWS resources

---

## Set up Spacelift Intent

📽️ Quick demo of Spacelift Intent with Claude Code below.

[![Intent demo](https://img.youtube.com/vi/UvF-_gbW9Gk/0.jpg)](https://www.youtube.com/watch?v=UvF-_gbW9Gk)

### Step 1. Add Intent MCP server to Claude Code

You can add the MCP server via command-line interface (CLI) _or_ by editing your config file.

**CLI:**

```bash
claude mcp add intent-mcp -t http https://<account-name>.app.spacelift.io/intent/mcp
```

**Config file (`.mcp.json` at repo root):**

```json
{
  "mcpServers": {
    "intent-mcp": {
      "type": "http",
      "url": "https://<account-name>.app.spacelift.io/intent/mcp"
    }
  }
}
```

---

### Step 2. Authenticate via MCP

1. Open **Claude Code**.
2. Run the `/mcp` command.
3. Select **`intent-mcp`** and press **Enter** to log in (status shows _disconnected – Enter to login_).
4. Complete the browser-based OAuth flow → “Authorization successful”.
5. Back in Claude Code, run `/mcp` again to confirm status is **connected**.

![Claude Code: Spacelift Intent server prior to authentication](../../assets/screenshots/spacelift-intent/01-claude-code-intent-disconnected.png)

Claude Code: Spacelift Intent server prior to authentication

![Claude Code: Authenticating Spacelift Intent MCP Server](../../assets/screenshots/spacelift-intent/02-claude-code-intent-auth.png)

Claude Code: Authenticating Spacelift Intent MCP Server

![Claude Code: Opening the browser for authentication](../../assets/screenshots/spacelift-intent/03-claude-code-intent-auth-url.png)

Claude Code: Opening the browser for authentication

![Claude Code: Browser authorization request](../../assets/screenshots/spacelift-intent/04-claude-code-intent-approve-step.png)

Claude Code: Browser authorization request

![Claude Code: Successful authentication callback](../../assets/screenshots/spacelift-intent/2025-10-07_21-58.png)

Claude Code: Successful authentication callback

![Claude Code: Spacelift Intent MCP Server successfully connected](../../assets/screenshots/spacelift-intent/2025-10-07_21-58_1.png)

Claude Code: Spacelift Intent MCP Server successfully connected

### Step 3. Create & use an Intent project

Projects scope your work and policy. You can create and lock a project entirely through natural language.

**Create a project** (via chat prompt):

```text
Create a project called "my-project".
```

Claude Code will call `project-create` for you.

![Claude Code: Creating a project using Spacelift Intent](../../assets/screenshots/spacelift-intent/2025-10-07_22-04.png)

Claude Code: Creating a project using Spacelift Intent

Then **lock** the project for exclusive access:

```text
Use the project "my-project".
```

This calls `project-use` and locks the project to your user. Locks expire after a short period of inactivity; you can unlock via UI or API.

![Claude Code: Locking a project using Spacelift Intent](../../assets/screenshots/spacelift-intent/2025-10-07_22-05_1.png)

Claude Code: Locking a project using Spacelift Intent

!!! note
    💡 Creating a project via MCP currently places it in the root Space. To create it in a different Space, [use the Spacelift UI](https://docs.spacelift.io/concepts/spaces).

---

### Step 4. Create resources (random provider)

Try something safe first using the **random** provider:

```text
Create two resources — one very long random string and a cute pet.
```

Intent discovers the provider schema, proposes the operations, and applies them under policy. You’ll get a short summary in chat once the resources are created.

![Claude Code: Creating two random provider resources - discovering resources](../../assets/screenshots/spacelift-intent/2025-10-07_22-12.png)

Claude Code: Creating two random provider resources - discovering resources

![Claude Code: Creating resources](../../assets/screenshots/spacelift-intent/2025-10-07_22-13.png)

Claude Code: Creating resources

![Claude Code: Resources successfully created](../../assets/screenshots/spacelift-intent/2025-10-07_22-14.png)

Claude Code: Resources successfully created

---

## Use Spacelift Intent

### 1. Explore the Spacelift Intent UI

!!! warning
    ❗ Please note that we've made some updates to the navigation — you can now find **Intent Projects** under **"Try New Features" → "Intent Projects."**

Open **Spacelift → Intent Projects → my-project**. You'll see:

- **Resources:** Current resources in project.
- **History:** Timeline of operations (create, update, delete, import).
- **Policies:** Attach Intent [policies to govern operations](https://docs.spacelift.io/concepts/policy.html).
- **Integrations:** Attach [cloud accounts](https://docs.spacelift.io/integrations/cloud-providers.html) (AWS supported today).
- **Environments:** [Environment variables](https://docs.spacelift.io/concepts/configuration/environment.html) for the project.

You will also see if the project is locked and who locked it.

![Spacelift UI: Intent Projects, locking projects and resources list](../../assets/screenshots/spacelift-intent/2025-10-07_22-19.png)

Spacelift UI: Intent Projects, locking projects and resources list

---

### 2. Create & attach Intent policy

Policies are your guardrails. Create a policy in **Policies** and attach it to your project. A simple example:

```rego
package spacelift

import rego.v1

sample = true

# Deny any resource that isn't an S3 bucket
deny contains message if {
  input.resource.resource_type != "aws_s3_bucket"
  message := sprintf(
    "Only aws_s3_bucket resources are allowed. Resource type %q is not permitted",
    [input.resource.resource_type],
  )
}

# Allow all operations on S3 buckets
allow contains message if {
  input.resource.resource_type == "aws_s3_bucket"
  message := sprintf(
    "Operation %q on aws_s3_bucket is allowed",
    [input.resource.operation],
  )
}
```

![Spacelift UI: Creating your first Intent policy](../../assets/screenshots/spacelift-intent/2025-10-07_23-20.png)

Spacelift UI: Creating your first Intent policy

![Spacelift UI: Intent policy payload](../../assets/screenshots/spacelift-intent/2025-10-08_01-52.png)

Spacelift UI: Intent policy payload

Once the policy is created, attach it to your project. Use the `Policies` tab in your Intent Project view.

![Spacelift UI: Attaching policy to the project](../../assets/screenshots/spacelift-intent/2025-10-07_23-25.png)

Spacelift UI: Attaching policy to the project

![Spacelift UI: Finding the right policy](../../assets/screenshots/spacelift-intent/2025-10-07_23-25_1.png)

Spacelift UI: Finding the right policy

![Spacelift UI: Intent policy attached](../../assets/screenshots/spacelift-intent/2025-10-07_23-26.png)

Spacelift UI: Intent policy attached

---

### 3. Attach AWS integration

Follow [AWS integration setup](https://docs.spacelift.io/getting-started/integrate-cloud/AWS), then attach the integration to your Intent project:

- Choose an **AWS region** for tests
- Grant **Read + Write**

![Spacelift UI: Attaching AWS integration to the project](../../assets/screenshots/spacelift-intent/2025-10-07_23-49.png)

Spacelift UI: Attaching AWS integration to the project

![Spacelift UI: AWS integration attached](../../assets/screenshots/spacelift-intent/2025-10-07_23-50.png)

Spacelift UI: AWS integration attached

---

### 4. Provision AWS resources (S3, EC2)

With the policy above:

- Creating an **S3 bucket** should **succeed**.
- Creating an **EC2 instance** should **fail** with a policy denial.

**Create an S3 bucket** (via chat):

```text
Create an S3 bucket named "dev-attachments-123" with SSE enabled.
```

![2025-10-07_23-56.png](../../assets/screenshots/spacelift-intent/2025-10-07_23-56.png)

**Update the S3 bucket:**

You can continue the conversation to modify existing resources:

```text
Add tags to the dev-attachments-123 bucket: Environment=dev, Owner=platform-team.
```

Intent updates the resource configuration and applies the changes. You’ll see the updated values in both your AWS account and the Spacelift UI (Resources view shows current config; History tab records the update operation).

![2025-10-07_23-59.png](../../assets/screenshots/spacelift-intent/2025-10-07_23-59.png)

**Verify in Spacelift UI & AWS:**

Confirm the resource lifecycle in both systems.

1. **In the Spacelift UI**, **n**avigate to your Intent project.
    - **Resources tab:** Shows the S3 bucket with current configuration including the tags you just added.

    ![2025-10-08_00-01_1.png](../../assets/screenshots/spacelift-intent/2025-10-08_00-01_1.png)

    - **History tab:** Lists all operations (create, update) with timestamps, operation details, and who/what triggered them.

    ![2025-10-08_00-02.png](../../assets/screenshots/spacelift-intent/2025-10-08_00-02.png)

2. In the **AWS Console**, go to S3:
    - Find your bucket (e.g., `dev-attachments-123`).
    - Verify it exists with the correct configuration.
    - Check the Tags section to confirm `Environment=dev` and `Owner=platform-team` are present.

    ![2025-10-08_00-01.png](../../assets/screenshots/spacelift-intent/2025-10-08_00-01.png)

As we've seen, Intent creates resources directly in your cloud, while Spacelift provides access control, policy governance, state management, and full auditability.

**Try an EC2 instance** (to see policy denial):

```text
Create a t3.micro EC2 instance in us-east-1.
```

![2025-10-08_00-05.png](../../assets/screenshots/spacelift-intent/2025-10-08_00-05.png)

!!! note
    💡 Iterate on the policy to allow additional resource types when ready (e.g., allow aws_instance for non-prod).

---

### 5. Import existing resources

You can **discover** and **import** pre-existing resources into Intent state, then manage them going forward.

**Example (SSM Parameters):**

```text
List SSM parameters in my account and import them into the project.
```

- Review the discovery result.

![2025-10-08_00-12.png](../../assets/screenshots/spacelift-intent/2025-10-08_00-12.png)

- Select items to **import** into Intent state.

![2025-10-08_00-17.png](../../assets/screenshots/spacelift-intent/2025-10-08_00-17.png)

- Manage them via natural language and policy from now on.

**Check Spacelift UI after import:**

Once resources are imported, verify them in the Spacelift UI.

- **Resources tab:** Shows newly imported SSM parameters alongside your existing S3 bucket.

![2025-10-08_00-19.png](../../assets/screenshots/spacelift-intent/2025-10-08_00-19.png)

- **History tab:** Records the import operation with full details of what was imported and when.

![2025-10-08_00-19_1.png](../../assets/screenshots/spacelift-intent/2025-10-08_00-19_1.png)

---

### 6. Delete resources safely

When deleting, Intent evaluates **dependencies**, requests **confirmation**, and enforces **policy**.

**Example:**

```text
Delete the random resources we created earlier.
```

Typical flow:

1. Tool computes dependency order.
2. Client asks for **explicit confirmation** (by default).
3. Apply proceeds or is **blocked by policy**.

![2025-10-08_00-23.png](../../assets/screenshots/spacelift-intent/2025-10-08_00-23.png)

If policy prevents deletion, update the policy to allow the `random` resources. You can do this using Spacelift Intent, but make sure to review the next section: Session Locks, Permissions & Safety.

![2025-10-08_00-29.png](../../assets/screenshots/spacelift-intent/2025-10-08_00-29.png)

![2025-10-08_00-33.png](../../assets/screenshots/spacelift-intent/2025-10-08_00-33.png)

![2025-10-08_00-34.png](../../assets/screenshots/spacelift-intent/2025-10-08_00-34.png)

**Auditability:** Even after deletion, the **History** tab shows attempted and successful deletions, with full receipts.

![2025-10-08_00-35.png](../../assets/screenshots/spacelift-intent/2025-10-08_00-35.png)

---

### 7. Session locks, permissions, & safety

- **Project lock:** Only one active session can operate on a project at a time (prevents conflicting changes). Locks auto-expire after inactivity.
- **Client controls:** You can configure your MCP client to always ask before invoking tools.
- **Role separation** (coming soon; unavailable in early access): For safety, split who writes policies from who operates resources. Combining both lets an agent relax guardrails to push through blocked changes. Use Spaces/RBAC to enforce when this feature becomes available.

---

## Troubleshooting

- **I don't see `intent-mcp` in `/mcp`.**

    - Re-run the add command; confirm the URL and account name.
    - Verify `.mcp.json` path and JSON validity.

- **OAuth window didn't open.**

    - Check pop-up blockers. Try re-auth via `/mcp` → select server again.

- **`project-use` fails / lock busy.**

    - Another session may hold the lock. Wait for timeout, or unlock via UI/API.

- **Policy denies everything.**

    - Start with allow-list for one resource type and expand.
    - Use a separate test project/Space while iterating.
    - Enable policy sampling by adding `sample = true` to your policy to capture evaluation events and debug in the Policy Workbench (UI → Policies → select policy → Show simulation panel).

- **AWS creation fails.**

    - Verify integration is attached **to the project**, region matches prompts, and access is **Read+Write**.

---

## FAQ

- **Can I use a client other than Claude Code?**

    Yes—Claude Desktop (custom connector), VS Code, Cursor. Any MCP-capable client should work with the same URL.

- **Where are the Terraform files?**

    Intent works at a higher abstraction—your agent calls provider operations under Spacelift governance. No IaC files are required for day‑1 usage.

- **Can I export to Terraform/OpenTofu later?**

    Export/migration is on the roadmap; for now, use Intent for discovery/management and codify stable architectures in your IaC repos over time.

- **How do I keep things safe in production?**

    For this early access beta, we do not recommend to run things in production.

---

## Appendix 1: Handy Commands & Prompts

**Add MCP server (CLI):**

```bash
claude mcp add intent-mcp -t http https://<account-name>.app.spacelift.io/intent/mcp
```

**Edit `.mcp.json`:** See [Set Up Claude Code](about:blank#set-up-claude-code).

**Auth & status:**

- `/mcp` → select **intent-mcp** → log in → verify **connected**

**Project management (via prompts):**

```text
Create a project called "my-project".
Use the project "my-project".
List my projects and their lock status.
Unlock the current project.
```

**Resources (via prompts):**

```text
Create two resources — one very long random string and a cute pet.
Create an S3 bucket named "dev-attachments-123" with SSE enabled.
Create a t3.micro EC2 instance in us-east-1.  # expect policy denial with example policy
List resources in this project.
Delete the random resources we created earlier.
```

**Import (via prompts):**

```text
List SSM parameters in my account and import them into the project.
```

_Use concise, explicit prompts; include environment/region and compliance requirements in your wording to help the agent make safer defaults._

## Appendix 2: Setting up Azure and GCP credentials

[Setting up Azure and GCP credentials for Spacelift Intent](https://www.notion.so/Setting-up-Azure-and-GCP-credentials-for-Spacelift-Intent-294251e5616a805196a8e360fcfcd5ea?pvs=21)
