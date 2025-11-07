# Creating a space

You can create and modify spaces on the _Enforce Guardrails_ > _Spaces_ tab in the Spacelift UI.

## Spaces diagram view

The spaces diagram view shows a tree of all the spaces visible to you in your account. The immutable `root` space is at the top, and from there you can build any tree structure you want.

If you are not an admin of the `root` space, you will only see the spaces that you have access to, additionally, you will see a path from the spaces you have access to, to the `root` space. Each space card indicates what access level you have to that space.

If you are an admin of the `root` space you don't see individual access levels, as you are automatically an admin of all spaces.

![Spaces diagram view](<../../assets/screenshots/spaces_access_propagation.png>)

By default, only `root` admin users can create or delete spaces. This can be changed in [account settings](./allowing-non-root-admins-to-manage-spaces.md).

## Creating a single space

You can create a space either by clicking a **Create space** button in the top right corner of the view, or by clicking the blue addition button at the bottom of a space card.

1. Click **Create space** in the top-right or the **blue plus sign** at the bottom of a space card in the diagram.
2. Fill in the details for the space:
      - **Name**: Enter a unique, descriptive name for your space.
      - **Description** (optional): Enter a (markdown-supported) description of the space and the resources it manages.
      - **Labels** (optional): Add labels to help sort and filter your spaces.
      - **Parent space**: Select the parent space for the new space. If you clicked the blue plus sign, this will be automatically filled in.
      - **Enable inheritance**: Check the box to enable, and uncheck to disable. Inheritance is enabled by default.
3. Click **Create**.

![Create a new space](<../../assets/screenshots/spaces/create_space.png>)

## Editing a space

Space admins can edit the space(s) they are assigned to, and `root` space admins can modify any space.

1. Click the space card you want to edit.
2. Make your desired changes.
3. Click **Save**.

![Edit a space](<../../assets/screenshots/spaces/edit_space.png>)

## Deleting a space

You can delete any space besides `root` and `legacy` if it is empty. Empty spaces do not have any child spaces, stacks, modules, or other attachable entities like worker pools and integrations.

1. Click the space card you want to delete.
2. Click **Delete space**.
3. Click **Delete** in the pop-up to confirm.

![Delete a space](<../../assets/screenshots/spaces/delete_space.png>)
