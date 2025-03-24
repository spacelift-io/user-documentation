# Managing child spaces

By default, only `root` admins can manage the spaces' tree topology.

This limitation stems from the fact that we also grant the `root` admins the ability to enforce a set of best practices across the whole organization by [autoattaching policies](https://docs.spacelift.io/concepts/policy.html#automatically).

However, if this limitation doesn't align with your organization's needs, you can adjust it in the account settings.

## Toggling the setting

The feature is controlled by a toggle found in the account settings. Only `root` admins can toggle the setting.
![](<../../assets/screenshots/spaces/subspaces-toggle.png>)

After enabling this setting, non-root admins will be able to create, manage, and delete child spaces that are children of the spaces they administrate.
After disabling the setting, non-root admins will no longer have the ability to modify spaces.

## Limitations

A subspace created by a non-root admin has inheritance enabled by default.

Non-root admins cannot create a subspace with disabled inheritance or update the subspace to disable inheritance.

Only `root` admins can create child spaces that have disabled inheritance.

Only `root` admins are eligible to disable inheritance in a space.

Only `root` admins can enable/disable non-root admins to manage sub-spaces.
