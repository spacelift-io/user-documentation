---
name: selfhosted-changelog
description: Add an entry to the Self-Hosted Spacelift changelog under vNext
argument-hint: [description]
---

# Self-Hosted Changelog Update

Add an entry to the Self-Hosted changelog at `docs/installing-spacelift/changelog.md`.

## Instructions

1. Read the changelog file first to understand existing patterns
2. Find or create the `## vNext` section at the top (after frontmatter and `# Changelog` heading)
3. Add the new entry under the appropriate subsection:
   - `### Features` - New functionality
   - `### Fixes` - Bug fixes
   - `### Documentation` - Documentation-only changes
   - `### Infrastructure` - Infrastructure/deployment changes
4. Create the subsection if it doesn't exist

## Entry Format

Basic format:

```markdown
- **Component/Area**: Description of what changed from the user's perspective.
```

Entries can range from one-liners to multi-paragraph with nested content:

- Simple fixes: one sentence
- New features: can include paragraphs, bullet lists, code blocks, links to docs

## Formatting Patterns

**Links to documentation:**

```markdown
See the [feature documentation](../path/to/doc.md) for details.
```

**External links (GitHub, etc.):**

```markdown
[repository name](https://github.com/spacelift-io/repo){: rel="nofollow"}
```

**Nested bullet lists for feature breakdowns (use 4-space indentation):**

```markdown
- **Feature Name**: Description of the feature.
    - Sub-point one
    - Sub-point two
```

**Admonitions when needed:**

```markdown
- **Feature**: Description.

    !!! note
        Additional context or caveats.
```

**Terraform/Helm module version requirements:**

```markdown
You'll need to use:
  - [v2.1.0 or later](https://github.com/spacelift-io/module/releases/tag/v2.1.0) for ECS installations.
```

## Markdown Formatting

- Add blank lines before and after fenced code blocks
- Add blank lines before and after lists
- Use 4-space indentation for nested lists

## Writing Guidelines

- Focus on user-visible changes, not implementation details
- Be clear about what changed and why it matters to users
- For fixes: describe what was broken from the user's perspective
- Include links to relevant documentation when helpful
- For self-hosted specific changes, mention required module/chart versions if applicable
- Match the tone of existing entries - direct and informative
