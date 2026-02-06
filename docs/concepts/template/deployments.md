# Template Deployments

The Templates list offers a simplified, form-based experience designed for application developers and end users who may not have deep infrastructure-as-code or Spacelift knowledge.

## Overview

Templates are designed for:

- **Application developers** who need infrastructure without IaC expertise
- **End users** who want to deploy pre-approved infrastructure patterns
- **Teams** who benefit from standardized, self-service infrastructure

The deployment experience prioritizes simplicity, validation, and guardrails to ensure successful infrastructure provisioning.

## Templates List

The Templates List is a user-friendly interface where users can browse and deploy from available templates.

![Templates Marketplace](<../../assets/screenshots/templates/templates-marketplace.png>)

## Deploying from the Marketplace

### Step 1: Select a Template

1. Browse or search for the template you need
2. Click **Deploy** to open the deployment form:

![Marketplace Deploy Form](<../../assets/screenshots/templates/marketplace-deploy-form.png>)

### Step 2: Create the Deployment

1. Review all input values
2. Click **Deploy**
3. Deployment is created and infrastructure provisioning begins
4. You're redirected to the deployment details page

## Viewing Your Deployments

After deploying, you can view and manage your deployments in the template deployments list.

### Deployment Details

![Deployment Details](<../../assets/screenshots/templates/deployment-details.png>)

**Overview Information:**

- Deployment name and description
- Current state (InProgress, Finished, Failure, etc.)
- Template and version used
- Creation date
- List of deployment outputs

### Deployment States

Your deployment will go through various states:

| State | Description | What You Can Do |
|-------|-------------|-----------------|
| **None** | Initial state | Wait for processing |
| **In Progress** | Being created | Monitor progress |
| **Finished** | Completed successfully | View outputs, use infrastructure |
| **Failure** | Creation failed | Review errors, contact template creator |
| **Unconfirmed** | Awaiting confirmation | Needs to be confirm by template creator |
| **Destroying** | Resources being destroyed | Wait for completion |
| **Destroying Failed** | Destruction failed | Contact template creator |

### Understanding Deployment States

**In Progress:**

- Infrastructure is being provisioned
- Check back periodically for updates
- Cannot make changes while in progress

**Finished:**

- Infrastructure is ready to use
- Outputs are available
- You can update or delete the deployment

**Failure:**

- Something went wrong during provisioning
- Review error messages
- Contact template creator for assistance
- You may be able to retry or delete

**Unconfirmed:**

- Deployment requires manual confirmation
- Contact template creator
- Wait for template creator confirmation

### Updating a Deployment

If you need to change anything in your deployment you can update it on deployment list.

**Update Process:**

1. Navigate to the deployment details
2. Choose **Update deployment** from actions dropdown
3. Update whatever inputs you need
4. Confirm the update

After that deployment process starts again and you will see the progress on the deploy detail page or deployments list.

!!! warning
    You cannot update a deployment that is in `InProgress`, `Unconfirmed`, or `Destroying` state. Wait for the current operation to complete.

### Deleting a Deployment

When you no longer need the infrastructure:

1. Navigate to your deployment details
2. Click **Delete**
3. Confirm the deletion

!!! warning
    - Deleting and destroying resources is permanent and cannot be undone
    - Make sure you have backups of any important data
    - You cannot delete a deployment that is in `InProgress`, `Unconfirmed`, or `Destroying` state

## Getting Help

If you encounter issues or need assistance:

1. **Check deployment errors**: Review error messages for clues
2. **Contact template creator**: They created the templates and can help
3. **Review documentation**: Check deployment instructions in the template
4. **Provide details**: Share deployment name, template version, and error messages

## Permissions

Your ability to work with template deployments depends on your permissions:

| Action | Required Permission |
|--------|---------------------|
| View templates list | Space Read access |
| Browse templates | Space Read access for template's space |
| Create deployment | `CreateBlueprintDeployment` or Space Write access |
| View your deployments | Space Read access |
| Delete deployment | `DeleteBlueprintDeployment` or deployment owner |

!!! note
    Permissions are managed by template creator through [spaces](../spaces/README.md). Contact them if you need additional access.

## Related Resources

- [Template Overview](README.md) - General information about templates
- [Templates Workbench](workbench.md) - Template creator interface for managing templates
- [Template Configuration](configuration.md) - Understanding template structure (for advanced users)
- [Stacks](../stack/README.md) - Understanding the stacks created by deployments
