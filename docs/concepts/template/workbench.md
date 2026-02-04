# Templates Workbench

The Templates Workbench is the platform team interface for creating, managing, and maintaining reusable infrastructure templates. It provides comprehensive tools for template authoring, version management, and deployment oversight.

## Overview

The Templates Workbench is designed for:

- **Platform engineers** who create and maintain infrastructure templates
- **Template authors** who design self-service infrastructure offerings
- **Operations teams** who need visibility into all deployments

![Templates Workbench](<../../assets/screenshots/templates/templates-workbench.png>)

## Creating a Template

To create a new template:

1. Navigate to **Templates Workbench**
2. Click **Create template**
3. Fill in the template details:
   - **Name**: Unique identifier within the space
   - **Space**: The space where the template will be created
   - **Description**: Optional description of the template's purpose
   - **Labels**: Optional metadata tags for organization
   - **Initial Version**: Version number (e.g., "1.0.0"), we don't force to use any versioning convention.
   - **Deployment Instructions**: Optional Markdown instructions for users, which can be use to show more detailed explanation of deployment configuration

![Create Template](<../../assets/screenshots/templates/create-template.png>)

## Managing Template Versions

Each template can have multiple versions, allowing you to evolve your infrastructure configuration over time while maintaining backwards compatibility.

![Template Versions](<../../assets/screenshots/templates/template-versions.png>)

### Template Version States

- **Draft**: The version is under development and can be edited. Deployments cannot be created from draft versions.
- **Published**: The version is finalized and read-only. Deployments can be created from published versions.

!!! warning
    Publishing a template version is a one-way operation. Once published, a version cannot be reverted to draft state. You must create a new version for further changes.

### Creating a New Version

1. Open your template from the Templates Workbench
2. Navigate to the **Versions** tab
3. Click **Create version**
4. Optionally clone from an existing version
5. Enter a version number
6. Add deployment instructions (optional, Markdown supported)

**Cloning a Version:**

- Start with an existing version's configuration
- Useful for incremental updates
- Preserves template body, inputs, and configuration
- You can then modify as needed

### Editing the Template Body

The template body is a YAML configuration that defines the infrastructure to be provisioned and the inputs users can provide.

![Template Body Editor](<../../assets/screenshots/templates/template-body-editor.png>)

The template body uses YAML format and supports the same configuration as Blueprints. Here's a minimal example:

{% raw %}

```yaml
inputs:
  - id: environment
    name: Target environment
stacks:
  - key: main
    name: ${{ context.deployment.name }}-stack
    vcs:
      reference:
        type: branch
        value: main
      repository: my-terraform-repo
      provider: GITHUB
    vendor:
      terraform:
        manage_state: true
    environment:
      variables:
        - name: TF_VAR_environment
          value: ${{ inputs.environment }}
```

{% endraw %}

For detailed template body syntax and configuration options, see the [Template Configuration](configuration.md) section.

### Publishing a Version

Once your template version is ready:

1. Click **Publish** in the template body editor
2. Review the parsed template configuration
3. Confirm the action in the modal
4. The version becomes read-only and available for deployments

!!! tip
    Test your template thoroughly in draft state before publishing, as published versions cannot be edited.

**What Happens When Publishing:**

- Version state changes from Draft to Published
- Version is pinned to the current VCS commit (deterministic)
- Template becomes available in the marketplace
- Users can create deployments from this version
- Version becomes immutable (cannot be edited)

### Deleting a Version

You can delete a template version if:

- It has no deployments
- You have delete permission in the template's space

To delete a version:

1. Navigate to the version in the versions list
2. Click **Delete**
3. Confirm the deletion

!!! warning
    Versions with existing deployments cannot be deleted. You must delete all deployments first.

## Managing Deployments

The Templates Workbench provides visibility into all deployments created from your templates.

![Template Deployments](<../../assets/screenshots/templates/template-deployments.png>)

!!! tip
    You can also see all deployments for specific template version on version view.

### Deployment States

| State | Description | Actions Available |
|-------|-------------|-------------------|
| **None** | Initial state | View, Update, Delete |
| **InProgress** | Being created | View only |
| **Finished** | Completed successfully | View, Update, Delete |
| **Failure** | Creation failed | View, Update, Delete |
| **Unconfirmed** | Awaiting confirmation | View only |
| **Destroying** | Resources being destroyed | View only |
| **DestroyingFailed** | Destruction failed | View, Update, Delete |
| **Discarded** | Deployment discarded | View, Update, Delete |

### Updating a Deployment version

Platform teams can update deployments to use different template versions:

1. Navigate to the deployment details
2. Click **Update version**
3. Select a different published version
4. Confirm the update

**Update Behavior:**

- Deployment switches to the new version
- Stacks are updated (not recreated)
- New version's configuration is applied
- New tracked run is triggered

### Updating a Deployment

There is also a possibility to update deployment inputs:

1. Navigate to the deployment details
2. Click **Update deployment**
3. Update inputs
4. Confirm the update

**Update Behavior:**

- Stacks are updated (not recreated) with new configuration
- New tracked run is triggered

### Deleting a Deployment

To remove a deployment:

1. Navigate to the deployment details or list
2. Click **Delete**
3. Confirm the deletion

## Deployment Details

When viewing a specific deployment, you can access:

### Stacks Tab

View all stacks created by the deployment

![Deployment Stacks](<../../assets/screenshots/templates/deployment-stacks.png>)

!!! warning
    Stacks created by template deployments are immutable and can't be edited like regular stacks, even by admins. The only way to modify them is by updating the deployment version or creating a new template version.

### Outputs Tab

On this view you can find all outputs from all stacks that were created with specific deployment.

![Deployment Outputs](<../../assets/screenshots/templates/deployment-outputs.png>)

## Permissions in the Workbench

Actions available depend on your permissions:

| Action | Required Permission |
|--------|---------------------|
| View templates | Space Read access |
| Create template | `CreateBlueprintsVersionedGroup` or Space Admin |
| Edit template | `UpdateBlueprintsVersionedGroup` or Space Admin (in template's space) |
| Delete template | `DeleteBlueprintsVersionedGroup` or Space Admin (no versions) |
| Create version | `UpdateBlueprintsVersionedGroup` or Space Admin |
| Publish version | `UpdateBlueprintsVersionedGroup` or Space Admin |
| Delete version | `DeleteBlueprintVersion` or Space Admin (no deployments) |
| View deployments | Space Read access |
| Update deployment | `UpdateBlueprintDeployment` or Space Admin |
| Delete deployment | `DeleteBlueprintDeployment` or Space Admin |

## Related Resources

- [Template Overview](README.md) - General information about templates
- [Template Deployments](deployments.md) - End user deployment interface
- [Template Configuration](configuration.md) - Complete YAML configuration reference
- [Blueprints](../blueprint/README.md) - Programmatic stack creation alternative
