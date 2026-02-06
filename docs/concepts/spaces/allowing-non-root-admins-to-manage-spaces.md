# Managing child spaces

By default, only `root` admins can manage the spaces tree because we also grant `root` admins the ability to enforce best practices organization-wide by [autoattaching policies](https://docs.spacelift.io/concepts/policy.html#automatically).

However, if your organization needs to allow other users to [alter the spaces tree structure](./structuring-your-spaces-tree.md), `root` admins can adjust it in account settings.

1. Click your name in the bottom-left of the screen, then **Organization settings**.
2. In the _Access control center_ section, click **Spaces**.
3. Click the toggle to **enable** or **disable** allowing space admins to create and edit spaces.
      - If enabled, non-root admins can create, manage, and delete the spaces they manage and those spaces' children.
      - If disabled, non-root admins cannot modify spaces.

![Allow non-admins to edit spaces](<../../assets/screenshots/spaces/allow_nonroot_space_management.png>)

## Non-root admin limitations

A subspace created by a non-root admin has **inheritance enabled by default**, and non-root admins cannot disable inheritance.

Only `root` admins can:

- Create child spaces that have disabled inheritance.
- Disable inheritance in a space.
- Enable/disable non-root admins to manage sub-spaces.
