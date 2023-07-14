---
description: >-
  Describes how to create a stack from a public Git repository.
---

# Raw Git

Spacelift supports a whole range of version control systems but all of them require setup.

This integration enables you to create stacks right from a publicly accessible Git repository, which also include GitHub gists.

!!! info

    Using Raw Git gives you a one-way connection to the repository. Pushes, PRs, etc. are not supported.

    This provider is best suited for consuming public content.

## Using Raw Git with stacks and modules

The stack or module creation and editing forms will show a dropdown from which you can choose the Raw Git VCS provider. What's different from other VCS providers, you need to specify the repository URL.

![](<../../assets/screenshots/raw-git-stack.png>)

The rest of the process is exactly the same as with [creating a GitHub-backed stack](../../concepts/stack/creating-a-stack.md#integrate-vcs) or module, so we won't go into further details.

## Using GitHub gists

To create a stack backed by a GitHub gist, you enter the gist's URL into the repository URL field.

![](<../../assets/screenshots/raw-git-gist.png>)

## Triggering runs on updates

This provider gives you a one-way connection to the repository. New runs won't get triggered automatically on updates to the repository.

The run can be triggered manually, though.

![](<../../assets/screenshots/raw-git-updates.png>)

1. You can use the Sync button to check for updates,
2. If there are any updates since the last sync or creation of the stack, the tracked commit will change,
3. You can use the Trigger button to invoke a run.
