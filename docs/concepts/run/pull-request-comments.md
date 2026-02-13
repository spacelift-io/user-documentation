---
description: >-
  Describes Spacelift's support for commenting on pull requests, as well as for
  taking action due to comments on pull requests
---
# Pull request comments

## Pull request plan commenting

### Via notification policy

We have a nice example in our [Notification policy](../policy/notification-policy.md#adding-a-comment-to-a-pr-about-changed-resources) documentation that shows how to add a comment to a pull request about changed resources. It is fully customizable, so you can change the message to your liking.

### Via stack label

To enable this feature, add the label `feature:add_plan_pr_comment` to the stacks you wish to enable plan commenting for on pull requests.

![Add PR comment stack label](<../../assets/screenshots/Screen Shot 2022-06-27 at 4.35.36 PM.png>)

Once enabled, on any future pull request activity, the result of the plan will be commented onto the pull request.

![Comments on future PRs](<../../assets/screenshots/Screen Shot 2022-06-27 at 4.34.46 PM.png>)

## Pull request comment-driven actions

To enable support for pull request comment events in Spacelift, enable the following permissions within your VCS app integration. If your VCS integration was created using the Spacelift VCS setup wizard, then these permissions have already been set up automatically, and no action is needed.

- Read access to `issues` repository.
- Subscribe to `issues:comments` event.

Once permissions are configured, you can access pull request comment event data from within your push policy and build customizable workflows using this data.

!!! warning
    Spacelift will only evaluate comments that begin with `/spacelift` to prevent users from unintended actions against their resources managed by Spacelift. Furthermore, Spacelift only processes event data for **new** comments, and will not receive event data for edited or deleted comments.

Here's an example [push policy](../policy/push-policy/README.md) to **trigger a tracked run from a pull request comment** event:

```opa
package spacelift

track {
    input.pull_request.action == "commented"
    input.pull_request.comment == concat(" ", ["/spacelift", "deploy", input.stack.id])
}
```

Using a push policy like the example above, a user could trigger a tracked run on their Spacelift stack by commenting something such as:

```text
/spacelift deploy my-stack-id
```

Events triggered by comments are subject to the same deduplication logic as other VCS events. If the commit data remains unchanged, a new run will not be created.

However, there is an exception for pull request comment events: if push policy results in a proposed decision and the comment starts with the `/spacelift` command, deduplication rules do not apply and the run will be created regardless. This allows you to trigger an unlimited number of proposed runs from a single commit, for example:

```opa
package spacelift

propose {
    input.pull_request.action == "commented"
    input.pull_request.comment == concat(" ", ["/spacelift", "propose", input.stack.id])
}
```
