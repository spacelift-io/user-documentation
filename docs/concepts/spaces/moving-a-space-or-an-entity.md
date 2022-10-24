# Moving a Space or any Entity

If after creating multiple Spaces you came to the conclusion that the tree structure could be better, it is entirely possible to restructure the tree completely.
Restructuring the tree can be achieved either by creating new spaces and then moving entities (stacks, policies, etc.) to them, or by moving (re-parenting) spaces including with entities inside them.
Both approaches are completely fine, but there are conditions that must be satisfied for the move operations to succeed.

## Moving a Stack

Stacks can be moved to a different space using the *Name* tab in the Stack's settings.

![](<../../assets/screenshots/spaces-move-stack.png>)

In order for the move operation to succeed, the stack has to maintain access to any attachable resources it uses (worker pools, contexts, cloud integrations, etc.).
In other words, the new space that the stack will be in must either inherit (directly or indirectly via parental chain) from the spaces that the used attachable resources are in or those resources have to be defined in the new space.


## Moving an Attachable Entity (Worker Pool, Context, etc.)



All the attachable entities can be moved to a different space either in the UI or via the API.
The following image shows how to move a context to a different space in the UI.

![](<../../assets/screenshots/spaces-move-context.png>)

Moving entities is possible only if all the stacks that have been using them would still be able to access them after the move in compliance with the inheritance rules.


## Moving a Space

Moving a space is essentially changing its parent space.
This can be done in the UI by choosing a new parent in the space's settings.

![](<../../assets/screenshots/spaces-reparent.png>)

This operation has an effect on the whole subtree, because all the children of the space being moved remain to be its children, so they change their location in the tree as well.
Changing a parent for a space is possible only if after the re-parenting process all the stacks in the whole affected subtree would still be able to access any attachable resources they have attached outside of the affected subtree in compliance with the inheritance rules.

