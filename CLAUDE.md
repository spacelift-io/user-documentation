# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Documentation Build System

This is the Spacelift user documentation repository using MkDocs with Material theme. The live documentation is at https://docs.spacelift.io/.

## Common Commands

### Development

- `make run` - Run the documentation site locally via Docker Compose (http://localhost:8000)
- `mkdocs serve` - Run locally with MkDocs directly
- `mkdocs serve -a '0.0.0.0:8000'` - Run with external access

### Testing and Linting

- `make lint` - Run all linting checks (markdown + image optimization)
- `pre-commit` - Run pre-commit hooks manually
- `pre-commit install` - Install git hooks for automatic validation

### Self-Hosted Documentation

- `mike serve --branch self-hosted-releases-prod` - Preview self-hosted docs
- Requires fetching: `git fetch origin self-hosted-releases-prod`

## Architecture

### Dual Documentation System

The repository maintains two versions of documentation:

- **SaaS version**: Standard documentation for cloud users
- **Self-hosted version**: Documentation for on-premises installations

This is managed through:

- Two navigation files: `nav.yaml` (SaaS) and `nav.self-hosted.yaml` (self-hosted)
- Conditional content using Jinja macros: `is_saas()` and `is_self_hosted()`
- Environment variable `SPACELIFT_DISTRIBUTION` controls which version is built

### Key Files and Structure

- `docs/` - All Markdown documentation content
- `mkdocs.yaml` - Main MkDocs configuration (uses `nav.yaml` by default)
- `nav.yaml` / `nav.self-hosted.yaml` - Navigation structure for each version
- `main.py` - Custom Jinja macros for conditional content
- `hooks/` - MkDocs build hooks for banner fetching and URL processing
- `overrides/` - Custom theme templates and components
- `docs/assets/` - Static assets (CSS, images, screenshots)

### Content Organization

Documentation is organized into main sections:

- **Getting Started** - Initial setup and onboarding
- **Main Concepts** - Core concepts like Stack, Blueprint, Configuration, Run, Policy, Resources
- **Vendors** - Tool-specific guides (Terraform, Ansible, Kubernetes, etc.)
- **Integrations** - Third-party integrations and cloud providers
- **Product** - Product-specific features and administration

### Screenshots and Assets

- Screenshots go in `docs/assets/screenshots/`
- Images are automatically optimized with oxipng during pre-commit
- Use descriptive filenames for screenshots

### Conditional Content Patterns

```markdown
{% if is_saas() %}
SaaS-only content here
{% endif %}

{% if is_self_hosted() %}
Self-hosted-only content here
{% endif %}
```

Use `{% raw %}` blocks when Jinja interferes with code examples containing template syntax.

## Development Workflow

### Making Changes

1. Edit Markdown files in `docs/` directory
2. Add new pages to appropriate navigation file(s)
3. Test locally with `make run`
4. Validate with pre-commit hooks
5. Both SaaS and self-hosted versions are automatically built on PR

### Adding New Pages

- Add to `nav.yaml` for SaaS-only pages
- Add to `nav.self-hosted.yaml` for self-hosted-only pages
- Add to both files for pages that appear in both versions

### Pre-commit Validation

The repository uses pre-commit hooks for:

- Large file detection
- YAML validation
- Markdown linting (markdownlint)
- Link checking (markdown-link-check)
- PNG optimization (oxipng)
