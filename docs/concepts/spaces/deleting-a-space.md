# Deleting a Space

Spaces can be deleted from the UI or the API.

![](<../../assets/screenshots/spaces-delete.png>)

The delete operation is only permitted if the space is empty, and it is a leaf of the space tree.
If any of the following conditions is true, the space cannot be deleted:

- The space has any child spaces
- The space contains any stacks or modules
- The space contains any attachable entities such as worker pools, contexts, cloud integrations, etc.


!!! warning
    You cannot delete neither the root nor the legacy space.
