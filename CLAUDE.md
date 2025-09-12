# Claude Instructions for Spacelift User Documentation

For detailed contribution workflow, setup instructions, and validation requirements, see @CONTRIBUTING.md.

## Repository Overview

This repository contains the official documentation for Spacelift (<https://docs.spacelift.io>), an infrastructure management platform that enhances Infrastructure-as-Code workflows. The documentation is built with MkDocs and Material theme, supporting both SaaS and Self-hosted versions.

## Spacelift Product Context

**What is Spacelift?**

- Infrastructure management platform for IaC workflows
- Supports multi-cloud (AWS, Azure, GCP) and multi-tool (Terraform, Kubernetes, Ansible, Pulumi, etc.)
- GitOps-focused with VCS integration and pull request previews
- Policy-driven governance using Open Policy Agent (OPA)

**Core Concepts to Understand:**

- **Stacks**: Main infrastructure units combining source code, state, and configuration
- **Policies**: Code-based governance rules using Rego language (9 types: login, access, approval, initialization, notification, plan, push, task, trigger)
- **Worker Pools**: Custom execution environments for enhanced security/compliance
- **Runs**: Infrastructure change executions (plan, apply, etc.)
- **Spaces**: Organizational units for grouping stacks
- **spacectl**: Official CLI tool wrapping GraphQL API

## Documentation Structure

```text
/docs/
  /concepts/          # Core Spacelift concepts (stack, policy, spaces, worker-pools, etc.)
  /getting-started/   # New user onboarding (create-stack, integrate-source-code, etc.)
  /integrations/      # Third-party integrations and APIs
  /product/           # Product feature documentation
  /vendors/           # Infrastructure provider docs (terraform, kubernetes, etc.)
  /assets/
    /css/             # Custom styling
    /images/          # Site logos and graphics
    /screenshots/     # UI screenshots for documentation
```

## Content Guidelines

### Quirks and Patterns

- When adding links to external websites, always add `{: rel="nofollow"}` to the link. For example: [Spacelift](https://spacelift.io){: rel="nofollow"}

### Dual Distribution Support

The documentation supports both SaaS and Self-hosted distributions:

**Navigation Files:**

- `nav.yaml` - SaaS navigation structure
- `nav.self-hosted.yaml` - Self-hosted navigation structure
- Generally update both unless content is distribution-specific

**Conditional Content:**
Use Jinja templating for distribution-specific sections:

```markdown
{% if is_saas() %}
SaaS-specific content here
{% endif %}

{% if is_self_hosted() %}
Self-hosted-specific content here
{% endif %}
```

**Raw Blocks:**
Wrap code containing template-like syntax:

```markdown
{% raw %}
```yaml
# Code with {{ template.syntax }} here
```
{% endraw %}
```

### Screenshot Guidelines

- Store in `/docs/assets/screenshots/`
- Use descriptive, hierarchical filenames
- Images are automatically optimized by pre-commit hooks (oxipng)
- Follow UI screenshot patterns from existing docs

### Content Patterns

- **Step-by-step guides**: Numbered workflows (see getting-started examples)
- **Cross-references**: Heavy linking between related concepts
- **Feature gates**: Mark paid/tier-specific features appropriately
- **Code examples**: Include practical examples with proper syntax highlighting

## Best Practices

### When Adding Content

1. Check existing structure and follow established patterns
2. Add to appropriate navigation files
3. Include cross-references to related concepts

### When Editing Existing Content

1. Preserve conditional content blocks
2. Update both navigation files if needed
3. Check for broken internal links
4. Consider impact on both documentation distributions

### Content Quality

- Use clear, actionable language
- Include practical examples
- Follow established screenshot and formatting patterns
- Link to related concepts and external resources appropriately
- Consider the user journey and onboarding experience
