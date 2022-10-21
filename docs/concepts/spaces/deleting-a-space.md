# Deleting a Space

Spaces can be deleted from the UI or the API.

![](<../../assets/screenshots/spaces-delete.png>)

Delete operation is only permitted if the space is empty and it is a leaf in the space tree.
If any of the following conditions is true, space cannot be deleted:

- Space has any child spaces
- Space contains any stacks or modules
- Space contains any attachable entities such as worker pools, contexts, cloud integrations, etc.


!!! warning
    You cannot delete neither the root nor the legacy space.
