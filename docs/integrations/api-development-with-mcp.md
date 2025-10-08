---
description: Use `spacectl`'s MCP server to build against the Spacelift GraphQL API without learning it.
---

# Spacelift API integration via `spacectl` MCP server

You don't need to learn the Spacelift GraphQL API. We've built GraphQL introspection tooling into `spacectl`'s MCP server that lets your coding assistant discover and use the API automatically.

## How it works

The `spacectl` MCP server includes:

- Complete GraphQL schema introspection.
- Authentication guide with working examples.
- Field and operation search capabilities.
- Live API exploration.

Your coding assistant uses these tools to discover the API structure, understand authentication, and generate working code in any language.

## Setup

### Install `spacectl`

First, install [`spacectl`](https://github.com/spacelift-io/spacectl) following the installation instructions in the repository.

After installation, log in to your Spacelift account:

```bash
spacectl profile login
```

See the [`spacectl` documentation](../concepts/spacectl.md) for more details on authentication and usage.

### Configure your coding assistant

Configure `spacectl` as an MCP server in your coding assistant.

**Claude Code example:**

Add this to your Claude Code MCP configuration:

```json
{
  "mcpServers": {
    "spacectl": {
      "command": "spacectl",
      "args": ["mcp", "server"]
    }
  }
}
```

The server provides tools for API discovery and includes authentication handling.

### Authentication

The MCP server includes a complete authentication guide covering:

- API key setup and token exchange
- GitHub token authentication (for GitHub SSO accounts)
- OIDC-based authentication
- `spacectl` CLI token export

Your coding assistant will automatically retrieve this information when building applications.

## What your coding assistant can discover

### API structure

- All available queries, mutations, and subscriptions
- Field definitions and types
- Required vs optional parameters
- Return types and nested structures

### Operations

- Stack management (create, update, delete, trigger runs)
- Module registry access
- Resource monitoring
- Run execution and monitoring
- Policy management

### Authentication flows

- Token exchange patterns
- Error handling
- Token refresh logic
- Permission requirements

## Development workflow

### Step 1: Tell your assistant what you want to build

- "Build a React dashboard showing stack status"
- "Create a Python script for automated deployments"
- "Make a CLI tool for managing stacks"

### Step 2: Assistant explores the API

- Introspects GraphQL schema
- Finds relevant operations
- Understands data structures

### Step 3: Assistant generates working code

- Handles authentication setup
- Creates properly typed API clients
- Implements error handling
- Follows best practices

## Example applications

Your assistant can build:

- **Dashboards**: Stack monitoring, deployment history, resource visualization
- **Automation**: CI/CD integrations, scheduled deployments, compliance checking
- **Mobile apps**: Deployment approvals, status monitoring, notifications
- **CLI tools**: Developer productivity, batch operations, administrative tasks
- **Integrations**: Slack bots, ticketing systems, monitoring tools

## Language support

The introspection works with any language or framework:

- **Web**: React, Vue, Angular, Next.js, plain Javascript
- **Backend**: Node.js, Python, Go, Java, C#, Ruby
- **Mobile**: React Native, Flutter, native development
- **Desktop**: Electron, native applications
- **Infrastructure**: Terraform providers, Kubernetes operators

## Getting started

1. [Install `spacectl`](https://github.com/spacelift-io/spacectl).
2. [Configure it as an MCP server](#configure-your-coding-assistant) in your coding assistant.
3. Start building. The assistant will handle API discovery, authentication setup, and code generation automatically.

No API documentation reading required.
