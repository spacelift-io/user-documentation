# Stack bulk actions

Spacelift allows you to perform bulk actions on stacks. This is useful when you need to perform the same action on multiple stacks at once. To initiate bulk actions, navigate to the "Stacks" page and select the stacks you want to perform the action on. When you make the selection you can choose the intended action from the following options:

- Confirm - Allows to confirm the blocking run for the selected stacks that are in the `Unconfirmed` state.
- Discard - Allows to discard the blocking run for the selected stacks that are in the `Unconfirmed` state.
- Trigger - Allows to [manually trigger a tracked run](../run/tracked.md#triggering-manually) for the selected stacks.
- Sync commit - Allows to sync the tracked stack commit. It pulls the latest HEAD commit of the tracked branch and updates the tracked commit field.
- Lock - Allows to lock the selected stacks for exclusive use.
- Unlock - Allows to unlock the selected locked stacks.
- Enable - Allows to enable the selected disabled stacks.
- Disable - Allows to disable the selected stacks, so they will not trigger any runs.
- Approve - Allows to add a run review approval for the selected stacks that require reviews according to your [approval policy](../policy/approval-policy.md).
- Reject - Allows to add a run review approval for the selected stacks that require reviews according to your [approval policy](../policy/approval-policy.md).
- Run task - Allows to [manually trigger a run](../run/task.md) with a custom command.

!!! info
    The UI will only show the actions that can be performed on the selected stacks filtering out the unavailable ones for your convenience.

## How to use bulk actions

When you select stacks on the "Stacks" page a floating action bar will appear at the bottom of the screen. This bar will show the number of selected stacks and the available actions.

![](../../assets/screenshots/stack/bulk-actions/stack-bulk-actions_floating-bar.png)

Actions that are not available for all the selected stacks will be marked with an icon. You can hover over the icon to see how many stacks are going to be affected.
![](../../assets/screenshots/stack/bulk-actions/stack-bulk-actions_partial-action-floating-bar.png)

If you need a more detailed view of the selected stacks, click the "See details" button, that will open the bulk actions drawer. From the drawer you can also dismiss any stacks you deem unnecessary. Use floating bar for quick actions and use the drawer when you need to be more careful with your selection.
![](../../assets/screenshots/stack/bulk-actions/stack-bulk-actions_drawer.png)

On the drawer you will see a fine-grained details on which actions are available for each of the selected stacks.
![](../../assets/screenshots/stack/bulk-actions/stack-bulk-actions_partial-action-drawer.png)

Once you select action, you will be presented with the confirmation step, that allows you to add additional details (like a note for the Lock action) and confirm the action itself.
![](../../assets/screenshots/stack/bulk-actions/stack-bulk-actions_confirm-action-floating-bar.png)

The same view is also available on the drawer, where you can review the applicable and not applicable items again.
![](../../assets/screenshots/stack/bulk-actions/stack-bulk-actions_confirm-action-drawer.png)

Once you confirm the action you'll be presented with the action results drawer, where you can review the status of each item. Please stay on this view until all actions are done otherwise you will stop the execution of the actions on all the selected items. When the action execution is finished, you can use the "New action" button to perform another action on the same selection or a subset of it (from the completed or the failed results).
![](../../assets/screenshots/stack/bulk-actions/stack-bulk-actions_result-drawer.png)

Note: It is possible to stop the queued actions if you make a mistake by clicking on either "Stop all" or the "Stop" button available for all queued items.
![](../../assets/screenshots/stack/bulk-actions/stack-bulk-actions_pending-actions.png)
