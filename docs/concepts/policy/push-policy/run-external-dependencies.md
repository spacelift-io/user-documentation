# External dependencies

External dependencies in push policies allow a user to define a set of dependencies that, while being external to Spacelift, **must be completed before a Spacelift run can start**.

A common use case of this feature is making Spacelift wait for a CI/CD pipeline to complete before executing a run.

## How it works

To use this feature, you must:

- Define dependencies in push policies.
- Mark dependencies as finished or failed using [spacectl](https://github.com/spacelift-io/spacectl){: rel="nofollow"}.

### Define dependencies

To define dependencies, you need to add a `external_dependency` rule to your push policy definition. This way, any run that gets created via this policy also has the dependency defined.

The following rule adds a dependency to all runs created by a policy.

```rego
external_dependency[sprintf("%s-binary-build", [input.push.hash])] { true }
```

You can have more complex rules that decide on the set of external dependencies based on data such as the current stack's labels.

!!! warning
    Include unique strings (such as commit hashes) in the dependencies names, as this is the only way to ensure that the dependency is unique for each source control event.

### Mark dependencies as finished or failed

To mark a dependency as `finished`, `failed`, or `skipped`, use the [spacectl](https://github.com/spacelift-io/spacectl){: rel="nofollow"} command line tool with following commands:

```bash
spacectl run-external-dependency mark-completed --id "<commit-sha>-binary-build" --status finished

spacectl run-external-dependency mark-completed --id "<commit-sha>-binary-build" --status failed

spacectl run-external-dependency mark-completed --id "<commit-sha>-binary-build" --status skipped 
```

The run will be eligible for execution only **after all of its dependencies are marked** as finished or skipped. If any of the dependencies has failed, the run will be marked as failed as well.

!!! warning
    To mark a run dependency as finished or failed, [spacectl](https://github.com/spacelift-io/spacectl){: rel="nofollow"} needs to be authenticated and have _write_ access to all the spaces that have runs with the given dependency defined.

## Example with GitHub Actions

The following example shows how to use external dependencies with GitHub Actions. First, define a push policy with dependencies. This example defines two dependencies: one for a binary build and one for a Docker image build.

```rego
package spacelift

track {
    input.push != null
    input.push.branch == input.stack.branch
}

external_dependency[sprintf("%s-binary-build", [input.push.hash])] { true }
external_dependency[sprintf("%s-docker-image-build", [input.push.hash])] { true }
```

Next, create a GitHub Action pipeline that will mark the dependencies as `finished` or `failed`. This pipeline will define two jobs, one for each dependency. We will use `sleep` to mock the build process.

{% raw %}

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

      - name: Check out repository code
        uses: actions/checkout@v5

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

      - name: Check out repository code
        uses: actions/checkout@v5

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

{% endraw %}

!!! warning
    Replace `<youraccount>` with your Spacelift account name and fill in necessary secrets if you decide to use this example.

### Testing example

With the policy and the pipeline defined, we can test it. Creating a new commit in the repository will trigger the pipeline.

1. A run was created in Spacelift, but it's in queued state. The run will not start until all the dependencies are marked as finished or skipped.
    ![Run in queued state for dependencies](<../../../assets/screenshots/run-external-dependency-queued.png>)
2. After the `docker-image-build` dependency has been marked as skipped the run is still queued, as the `binary-build` dependency is still not resolved.
    ![One dependency resolved, one unresolved](<../../../assets/screenshots/run-external-dependency-completed-1.png>)
3. The run starts only after all the dependencies reach a terminal state.
    ![All dependencies resolved](<../../../assets/screenshots/run-external-dependency-completed-2.png>)

We can also test what happens if a step in the pipeline fails by changing the `build-binaries` job in the pipeline from:

```yaml
      - name: Build binaries
        run: |
          sleep 15
          echo "building binaries done"
```

to:

```yaml
      - name: Build binaries
        run: |
          sleep 15
          echo "building binaries failed"
          exit 1
```

Now, when we push a commit to the repo, the new run will be marked as failed with a note explaining that one of the dependencies is marked as failed.

![External dependency failed](<../../../assets/screenshots/run-external-dependency-failed.png>)
