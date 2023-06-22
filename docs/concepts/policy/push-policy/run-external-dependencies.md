# Run External Dependencies

## Purpose

Run external dependencies is a feature within push policies that allows user to define a set of dependencies, which, while being external to Spacelift, must be completed before a Spacelift run can be executed.
A common use case of this feature is making Spacelift wait for a CI/CD pipeline to complete before executing a run.

## How it works

Using this feature consists of two parts:
- defining dependencies in push policies
- marking dependencies as finished or failed using [spacectl](https://github.com/spacelift-io/spacectl)

### Defining dependencies

To define dependencies, you need to add a `external_dependency` block to your push policy definition.
This way, any run that gets created via this policy, also has the dependency defined.

The following rule adds a dependency to all runs created by a policy.

```rego
external_dependency[sprintf("%s-binary-build", [input.push.hash])] { true }
```

!!! warning
    Make sure to include unique strings such as commit hashes in the dependencies names, as this is the only way to ensure that the dependency is unique for each run.


### Marking dependencies as finished or failed

To mark a dependency as finished or failed, you need to use the [spacectl](https://github.com/spacelift-io/spacectl) command line tool.
You can do so with following commands:

```bash
spacectl run-external-dependency mark-completed --id "<commit-sha>-binary-build" --status finished

spacectl run-external-dependency mark-completed --id "<commit-sha>-binary-build" --status failed
```

!!! info
    Run will be eligible for execution only after all of its dependencies are marked as finished.
    At the same time, if any of the dependencies is marked as failed, the run will be marked as failed as well.

!!! warning
    In order to mark a run dependency as finished or failed, [spacectl](https://github.com/spacelift-io/spacectl) needs to be authenticated and have *write* permission to all the spaces that have runs with given dependency defined.

## Example with GH Actions

The following example shows how to use this feature with GitHub Actions.

The first thing we need to do is to define a push policy with dependencies.
Our policy will look like this:

```rego
package spacelift

track {
    input.push != null
    input.push.branch == input.stack.branch
}

external_dependency[sprintf("%s-binary-build", [input.push.hash])] { true }
external_dependency[sprintf("%s-docker-image-build", [input.push.hash])] { true }
```

We are defining two dependencies. One for a binary build and one for a docker image build.

Next, we need to create a GitHub Action pipeline that will mark the dependencies as finished or failed.
This pipeline will define two jobs, one for each dependency. We will use *sleep* to mock the build process.

```yaml
name: Build

on:
  push:

jobs:
  build-binaries:
    name: Build binaries
    runs-on: ubuntu-latest

    steps:
      - name: Install spacectl
        uses: spacelift-io/setup-spacectl@main
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Check out repository code
        uses: actions/checkout@v3

      - name: Build binaries
        run: |
          sleep 15
          echo "building binaries done"

      - name: Notify Spacelift of build completion (success)
        if: success()
        env:
          SPACELIFT_API_KEY_ENDPOINT: https://<youraccount>.app.spacelift.io
          SPACELIFT_API_KEY_ID: ${{ secrets.SPACELIFT_API_KEY_ID }}
          SPACELIFT_API_KEY_SECRET: ${{ secrets.SPACELIFT_API_KEY_SECRET }}
        run: spacectl run-external-dependency mark-completed --id "${GITHUB_SHA}-binary-build" --status finished

      - name: Notify Spacelift of build completion (failed)
        if: failure()
        env:
          SPACELIFT_API_KEY_ENDPOINT: https://<youraccount>.app.spacelift.io
          SPACELIFT_API_KEY_ID: ${{ secrets.SPACELIFT_API_KEY_ID }}
          SPACELIFT_API_KEY_SECRET: ${{ secrets.SPACELIFT_API_KEY_SECRET }}
        run: spacectl run-external-dependency mark-completed --id "${GITHUB_SHA}-binary-build" --status failed

  build-docker-images:
    name: Build docker images
    runs-on: ubuntu-latest

    steps:
      - name: Install spacectl
        uses: spacelift-io/setup-spacectl@main
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Check out repository code
        uses: actions/checkout@v3

      - name: Build docker images
        run: |
          sleep 30
          echo "building images done"

      - name: Notify Spacelift of build completion (success)
        if: success()
        env:
          SPACELIFT_API_KEY_ENDPOINT: https://<youraccount>.app.spacelift.io
          SPACELIFT_API_KEY_ID: ${{ secrets.SPACELIFT_API_KEY_ID }}
          SPACELIFT_API_KEY_SECRET: ${{ secrets.SPACELIFT_API_KEY_SECRET }}
        run: spacectl run-external-dependency mark-completed --id "${GITHUB_SHA}-docker-image-build" --status finished

      - name: Notify Spacelift of build completion (failed)
        if: failure()
        env:
          SPACELIFT_API_KEY_ENDPOINT: https://<youraccount>.app.spacelift.io
          SPACELIFT_API_KEY_ID: ${{ secrets.SPACELIFT_API_KEY_ID }}
          SPACELIFT_API_KEY_SECRET: ${{ secrets.SPACELIFT_API_KEY_SECRET }}
        run: spacectl run-external-dependency mark-completed --id "${GITHUB_SHA}-docker-image-build" --status failed
```

!!! warning
    Make sure to replace `<youraccount>` with your Spacelift account name and fill in necessary secrets if you decide to use this example.

Let's see what happens when we create a commit in the repository that is tracked by a stack with this push policy attached.

// todo picture of dependencies

After dependency is completed, it is marked as finished in Spacelift.

// todo picture of completed 1/2

Only when all the dependencies are marked as finished, the run is eligible for execution.




