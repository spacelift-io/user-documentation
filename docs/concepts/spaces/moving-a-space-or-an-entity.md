# Moving a Space or any Entity

If after creating multiple Spaces you conclude that the tree structure could be better, it is possible to restructure the tree completely.

Restructuring the tree can be achieved either by creating new spaces and then moving entities (stacks, policies, etc.) to them or by moving (re-parenting) spaces (which includes the entities they contain).

Both approaches are valid, but some conditions must be satisfied for the move operations to succeed.

## Moving a Stack

Stacks can be moved to a different space using the **Stack Details** tab in the Stack's settings.

![](<../../assets/screenshots/stack/settings/stack-details_spaces-ipunt.png>)

For the move operation to succeed, the stack has to maintain access to any attachable resources it uses (worker pools, contexts, cloud integrations, etc.).

In other words, the new space the stack will be in must either inherit (directly or indirectly via parental chain) from the spaces that the used attachable resources are in or those resources have to be defined in the new space.

## Moving an Attachable Entity (Worker Pool, Context, etc.)

All the attachable entities can be moved to a different space either:

![](<../../assets/screenshots/spaces-move-context.png>)

Moving entities is possible only if all the stacks that have been using them would still be able to access them after the move in compliance with the inheritance rules.

## Moving a Space

Moving a space is essentially changing its parent space.

This can be done by choosing a new parent in the space's settings:

![](<../../assets/screenshots/spaces-reparent.png>)

This operation affects the whole subtree, because all the children of the space being moved remain its children, so they change their location in the tree as well.

Changing a parent for a space is possible only if after the re-parenting process all the stacks in the whole affected subtree would still be able to access any entities that are attached outside of the subtree, in compliance with the inheritance rules.
