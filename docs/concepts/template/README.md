# Templates

{% if is_saas() %}
!!! Info
    This feature is only available on the Business plan and above. Please check out our [pricing page](https://spacelift.io/pricing){: rel="nofollow"} for more information.
{% endif %}

Templates provide a self-service approach to infrastructure provisioning, making it easier for application developers to deploy infrastructure without deep IaC or Spacelift knowledge. Templates focus on enabling end users to deploy infrastructure through a simplified, form-based interface.

## What is a Template?

A Template is a reusable infrastructure-as-code configuration that can be deployed multiple times with different inputs. Templates consist of:

- **Template metadata**: Name, description, labels, and space assignment
- **Template versions**: One or more versions of the template configuration
- **Template body**: YAML configuration defining infrastructure resources and inputs
- **Inputs**: User-provided values that customize each deployment

## Templates vs Blueprints

While both features enable infrastructure provisioning, they have fundamentally different approaches and serve different use cases:

### Key Architectural Differences

**Blueprints** are a **creation tool** that generates stacks which then live independently:

- Creates stacks that become regular, fully editable Spacelift stacks
- Once created, stacks can be modified manually like any other stack
- No ongoing relationship between the blueprint and the created stacks
- Stacks continue to evolve independently after creation
- Blueprint changes don't affect previously created stacks

**Templates** are a **lifecycle management tool** that maintains control over deployed infrastructure:

- Creates stacks through deployments that are fully managed by the template
- Stacks created from templates are **immutable** - cannot be edited manually, even by admins
- The only way to modify infrastructure is by:
    1. Updating the template deployment to use a different version
    2. Creating a new template version with changes and update deployment to use it
    3. Modifying deployment inputs
- Deployments maintain a permanent link to the template version
- Templates ensure consistency across all deployments

### Determinism and Reproducibility

**Templates are deterministic by design:**

- Each published template version is pinned to a specific VCS commit
- Same template version + same inputs = identical infrastructure every time (if you don't use any random inputs or random resources in terraform)
- Guarantees reproducibility across deployments
- Eliminates configuration drift between environments
- Ensures predictable outcomes

**Blueprints offer flexibility:**

- Use the latest code from the VCS branch
- Stacks can diverge from the original blueprint configuration
- Allows for manual adjustments and customizations
- More suitable for one-time stack creation scenarios

## Two Interfaces for Different Users

Templates are accessed through two distinct interfaces designed for different user personas:

### Templates Workbench

The **Templates Workbench** is designed for platform teams and template authors:

- Create and manage template definitions
- Author and edit template versions
- Configure template body (YAML configuration)
- Publish template versions
- View all deployments across the organization
- Manage template lifecycle

See [Templates Workbench](workbench.md) for detailed documentation.

### Templates List

The **Templates List** is designed for application developers and end users:

- Browse available published templates
- Deploy infrastructure using simple forms
- View their own deployments
- Update deployments
- Simplified, self-service experience

See [Template Deployments](deployments.md) for detailed documentation.

## Related Features

- [Templates Workbench](workbench.md) - Platform team interface for creating and managing templates
- [Template Deployments](deployments.md) - End user interface for deploying infrastructure
- [Blueprints](../blueprint/README.md) - Programmatic stack creation
- [Stacks](../stack/README.md) - Infrastructure-as-code project management
- [Spaces](../spaces/README.md) - Multi-tenancy and access control
- [Policies](../policy/README.md) - Governance and compliance rules
- [Contexts](../configuration/context.md) - Shared configuration

## Summary

Templates provide a powerful self-service approach to infrastructure provisioning:

- ✅ **User-Friendly**: Form-based interface for non-experts
- ✅ **Reusable**: Create once, deploy many times with different inputs
- ✅ **Versioned**: Built-in version management for evolution
- ✅ **Deterministic**: Same version + inputs = identical infrastructure
- ✅ **Immutable**: Deployed stacks cannot be modified manually
- ✅ **Validated**: Input validation prevents misconfigurations
- ✅ **Controlled**: Permission-based access control
