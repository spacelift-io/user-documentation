# Creating a Space

Creating and modifying spaces takes place in the **Spaces** tab in the UI.

![](<../../assets/screenshots/spaces-tab.png>)

## Spaces View

The view shows a tree of all the spaces visible to you in your account. The immutable `root` space is at the top, and from there you can build any tree structure you want.

This view behaves a bit differently for users that are admins of the `root` space.

If you are not an admin of the `root` space, you will only see the spaces that you have access to, additionally, you will see a path from the spaces you have access to, to the `root` space.
Each space card would indicate what access level to that space you have.

If you are an admin of the `root` space you don't see individual access levels, as you are automatically an admin of all spaces.

![](<../../assets/screenshots/spaces_access_propagation.png>)

## Creating a Single Space

If you are an admin of the `root` space you can create a space either by clicking a **Create space** button in the top right corner of the view, or by clicking the blue addition button at the bottom of a space card.

![](<../../assets/screenshots/spaces-create-button.png>)

Clicking either will open a modal where you can enter the name of the space, its parent and optionally a description and labels.

You then can click **Create** to create the space.

![](<../../assets/screenshots/spaces-create-form.png>)

## Editing the Space

An admin of the `root` space has the ability to modify spaces. This can be done by clicking on a space card, which opens up a form similar to the one used for creating a space. After performing any changes you can click **Save** to save them.

![](<../../assets/screenshots/spaces-edit-form.png>)
