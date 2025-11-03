# Moving a space or any entity

If you need to move or rearrange your spaces after they're created, you can restructure your spaces tree by:

1. Creating new spaces and then moving entities (stacks, policies, etc.) to them.
2. Moving spaces to a different parent space (which also moves the entities they contain).

By default, only `root` admin users can move spaces. This can be changed in [account settings](./allowing-non-root-admins-to-manage-spaces.md).

## Moving a space

Moving a space means, essentially, changing its parent space. You can only change a space's parent if affected stacks (in the entire affected subtree) would still be able to access entities that are attached outside of the subtree, in compliance with the inheritance rules.

Choose a new parent in the space's settings:

1. Click the space card you want to edit.
2. In the _Parent space_ section, choose the new parent space to use.
3. Click **Save**.

![Move a space by changing its parent](<../../assets/screenshots/spaces/change_parent_space.png>)

Moving a space will affect the whole subtree, and any other spaces attached to the moved space will move as well.

## Moving a stack

Stacks can be moved to a different space. You can only change a stack's space if it retains access to its attachable resources, such as worker pools and cloud integrations. The new space must either inherit (directly or indirectly via parental chain) from the spaces containing the attachable resources used by the stack, or those resources must be defined in the new space to ensure the stack retains access.

1. Navigate to _Ship Infra_ > _Stacks_ and locate the stack you want to move.
2. Click the **three dots** beside the name of the stack, then click **Settings**.
3. In _Stack details_, select the new space to use.
4. Click **Save**.

![Move a stack to a different space](<../../assets/screenshots/stack/settings/stack-details_spaces-ipunt.png>)

## Moving an attachable entity

All attachable entities (worker pools, contexts, etc.) can be moved to a different space. You can only move an entity if the stacks using it will still be able to access it in the new space.

In general, you will:

1. Click the **three dots** beside the entity in the Spacelift UI to edit it.
2. Select the new space from the dropdown.
3. **Save** your changes.

![Move a context to a different space](<../../assets/screenshots/spaces/edit_context.png>)
