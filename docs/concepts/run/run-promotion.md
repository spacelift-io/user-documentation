---
 description: >-
   Describes the process of promoting proposed runs into tracked runs on
   Spacelift.
---

# Run promotion

[proposed](proposed.md) runs only display changes to be made, while [tracked](tracked.md) runs apply (deploy) the proposed changes.

Promoting a proposed run is triggering a tracked run for the same Git commit.

## Prerequisites

1. For a run to be promote-able, the proposed run **must point to a commit that is newer than the stack's current commit**.
2. To promote a run, you first need to ensure that you have `Allow run promotion` enabled in the stack settings of your stack(s) in which you'd like to promote runs.
3. You should have a write permission to promote a run.

## Enabling run promotion

1. Navigate to **Ship Infra** > **Stacks**.
2. Click the **three dots** beside the stack and select **Settings**.
3. Click **Behavior**.
4. Enable the _Allow run promotion_ slider.

![Enable the Allow run promotion feature in stack settings](<../../assets/screenshots/stack/settings/stack-behavior_run-promotion.png>)

### Promote from proposed run view

Assuming all prerequisites are met, you will see a **Promote** button on a proposed run. Click it to promote the proposed run into a tracked run.

![Promote a proposed run using the Promote button](<../../assets/screenshots/run/promote-proposed-run.png>)

### Promote from a pull request

For Spacelift users using GitHub, a similar feature is available directly from the GitHub pull request. Assuming the prerequisites are met, you will see a **Deploy** button within the _Checks_ tab of the pull request. This button will promote your proposed run into a tracked run.

![Promote a run from a GitHub pull request using the Deploy button](<../../assets/screenshots/run/deploy-proposed-run.png>)
