---
description: >-
  Describes how to create a stack from a public Git repository.
---

# Raw Git

Spacelift supports a range of [version control systems](./README.md) that all require setup. With the raw Git integration, you can create stacks straight from a publicly accessible Git repository, including GitHub gists, without additional setup.

!!! info

    Using Raw Git with Spacelift gives you a one-way connection to the repository. Pushes, PRs, etc. are not supported.

    This integration is best for _consuming_ public content.

## Use Raw Git with stacks and modules

To get started, click **Create stack** on the _Stacks_ page or **Create module** on the _Terraform registry_ page. When creating a module instead of a stack, you will connect to source code first, then enter module details.

![Create a stack](<../../assets/screenshots/CreateStackGS.png>)

### Stack or module details

Fill in required _stack details_ or _module details_.

![Add stack details](<../../assets/screenshots/getting-started/create-stack/Stack-details.png>)

1. **Name**: Enter a unique, descriptive name for your stack or module.
2. **Space**: Select the [space](../../concepts/stack/README.md) to create the stack or module in.
3. [**Labels**](../../concepts/stack/stack-settings.md#labels) (optional): Add labels to help sort and filter your stacks or modules.
4. **Description** (optional): Enter a (markdown-supported) description of the stack or module and the resources it manages.
5. Click **Continue**.

### Connect to source code

![Create stack with raw Git](<../../assets/screenshots/stack/create-stack-raw-git.png>)

1. **Integration**: Click the Raw Git integration.
2. **URL**: Enter the repository URL you would like to use.
3. **Repository**: Ensure the name of the repository is correct when autofilled from the URL.
4. **Branch**: Select the branch of the repository to manage with this stack.
5. [**Project root**](../../concepts/stack/stack-settings.md#project-root) (optional): If the entrypoint of the stack is different than the root of the repo, enter its path here.
6. [**Project globs**](../../concepts/stack/stack-settings.md#project-globs) (optional): Enter additional files and directories that should be managed by the stack.
7. **Use Git checkout**: Toggle that defines if integration should use git checkout to download source code, otherwise source code will be downloaded as archive through API. This is required for [sparse checkout](../../concepts/stack/stack-settings.md#git-sparse-checkout-paths) to work.
8. Click **Continue**.

The rest of the process is exactly the same as [creating a GitHub-backed stack](../../getting-started/create-stack/README.md#2-connect-to-source-code) or module.

## Use GitHub gists

To create a stack backed by a GitHub gist, enter the gist's URL into the **URL** field.

![Use a GitHub gist](<../../assets/screenshots/stack/create-stack-git-gist.png>)

## Trigger runs on updates

This integration gives you a one-way connection to the repository. New runs aren't automatically triggered on updates to the repository. However, you can trigger runs manually.

![Trigger manual runs](<../../assets/screenshots/raw-git-updates.png>)

1. Click **Sync** to check for updates.
2. If there are any updates since the last sync or creation of the stack, the tracked commit will change.
3. Click **Trigger** to invoke a run.
