# Structuring your spaces tree

When planning your [space structure](./creating-a-space.md#spaces-diagram-view), consider the following:

- **Who needs access?:** Spaces control access to resources. Who needs access to production stacks? Who should be able to approve IAM changes?
- **How do you want to organize your spaces?:** Spaces organize your resources. Do you want to organize by team, environment, project, or some other way?
- **How do you want to share resources?:** Spaces can share resources. Through space inheritance, you can share policies, worker pools, and other attachable resources from parent to child spaces.

## Structure recommendations

Your first intuition might be to structure your spaces team-first or service-first, like this:

![Team first space tree example](<../../assets/screenshots/spaces_tree_structure_1.png>)

However, you will probably want to reuse some Spacelift resources across all development environment services, not across all environments for a single service. For example, resources like [worker pools](../worker-pools/README.md) are usually shared across security domains, not logical domains.

We recommend a spaces tree structure more like this:

![Better space tree structure](<../../assets/screenshots/spaces_tree_structure_2.png>)

This way you can create your worker pools, contexts, and policies in the `dev`, `preprod`, and `prod` spaces, and then reuse them in all spaces below those.

!!! info
    Enable [inheritance](./access-control.md#inheritance) in the space settings if you plan to have, for example, your VCS in a separate space above your stack.

## Rearranging spaces and other resources

If you need to move or rearrange your spaces after they're created, you can restructure your spaces tree by:

1. Creating new spaces and then moving entities (stacks, policies, etc.) to them.
2. Moving spaces to a different parent space (which also moves the entities they contain).

By default, only `root` admin users can move spaces. This can be changed in [account settings](./allowing-non-root-admins-to-manage-spaces.md).

### Moving a space

Moving a space means, essentially, changing its parent space. You can only change a space's parent if affected stacks (in the entire subtree) would still be able to access entities that are attached outside of the subtree, in compliance with the inheritance rules.

Choose a new parent in the space's settings:

1. Click the space card you want to edit.
2. In the _Parent space_ section, choose the new parent space to use.
3. Click **Save**.

![Move a space by changing its parent](<../../assets/screenshots/spaces/change_parent_space.png>)

Moving a space will affect the whole subtree, and any other spaces attached to the moved space will move as well.

### Moving a stack

Stacks can be moved to a different space. You can only change a stack's space if it retains access to its attachable resources, such as worker pools and cloud integrations. The new space must either inherit (directly or indirectly via parental chain) from the spaces containing the attachable resources used by the stack, or those resources must be defined in the new space to ensure the stack retains access.

1. Navigate to _Ship Infra_ > _Stacks_ and locate the stack you want to move.
2. Click the **three dots** beside the name of the stack, then click **Settings**.
3. In _Stack details_, select the new space to use.
4. Click **Save**.

![Move a stack to a different space](<../../assets/screenshots/stack/settings/stack-details_spaces-ipunt.png>)

### Moving an attachable resource

All attachable resources (worker pools, contexts, etc.) can be moved to a different space. You can only move a resource if the stacks using it will still be able to access it in the new space.

In general, you will:

1. Click the **three dots** beside the resource in the Spacelift UI to edit it.
2. Select the new space from the dropdown.
3. **Save** your changes.

![Move a context to a different space](<../../assets/screenshots/spaces/edit_context.png>)
