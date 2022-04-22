# User-Provided Metadata

Occasionally you might want to add additional information to your Runs which isn’t handled on a first-class basis by Spacelift. You can attach this kind of information using the run metadata parameter, which is available through [spacectl](https://github.com/spacelift-io/spacectl) as well as the GraphQL API.

### Usage

Let’s start with a small example. You’ll need a private worker for this.

On the machine where the worker resides, create a simple policy in a file:

```opa
package spacelift
sample { true }
```

And then start the worker with an additional environment variable:

```bash
SPACELIFT_LAUNCHER_RUN_INITIALIZATION_POLICY=/path/to/your/policy.rego
```

This policy will make our launcher sample each [initialization policy](../policy/run-initialization-policy.md) evaluation and print it as a log on stderr.

We’ll also need a [Stack](../stack/) to which [this worker is attached](../worker-pools.md).

We can now trigger a run and provide an arbitrary metadata string:

```bash
~> spacectl stack deploy --id testing-spacelift --run-metadata "deploy-metadata"
You have successfully created a deployment
The live run can be visited at http://cube2222.app.spacelift.tf/stack/testing-spacelift/run/01FEKAGP4AYV0DWP4QDFTANRES
```

And in the private worker logs we should suitably see (formatted for readability):

```json
{
  "caller": "setup.go:201",
  "level": "info",
  "msg": "Sample 0/INITIALIZATION/7YGHCNF7W6VMBQ49XQ42MH4JD1/allow",
  "sample": {
    "body": "package spacelift\nsample { true }\n",
    "input": {
      "docker_image": "",
      "run": {
        "based_on_local_workspace": false,
        "changes": [],
        "commit": {
          "author": "cube2222",
          "branch": "master",
          "created_at": 1628243895000000000,
          "message": "Update main.tf"
        },
        "created_at": 1630588655754344000,
        "id": "01FEKAGP4AYV0DWP4QDFTANRES",
        "state": "PREPARING",
        "triggered_by": "api::01FEGXFB7TWQ2NNF95W7HPRE2E",
        "updated_at": 1630588656197898500,
        "user_provided_metadata": [ // <------------------
          "deploy-metadata".        // <-- the metadata --
        ]                           // <------------------
      },
      "static_run_environment": {
        "account_name": "cube2222",
        "auto_deploy": false,
        "before_apply": null,
        "before_init": null,
        "command": "",
        "commit_branch": "master",
        "commit_sha": "7d629c6c3f3b6da07e28a87727f0586e577d98c1",
        "endpoint_logs": "tcp://169.254.0.3:1983",
        "endpoint_registry": "registry.spacelift.io",
        "environment_variables": {},
        "project_root": "",
        "refresh_state": true,
        "repository_path": "cube2222/testing-spacelift",
        "run_type": "TRACKED",
        "run_ulid": "01FEKAGP4AYV0DWP4QDFTANRES",
        "skip_init": false,
        "stack_labels": null,
        "stack_slug": "testing-spacelift",
        "terraform_version": "0.14.10",
        "vendor_specific_config": {
          "vendor": "terraform",
          "typed_config": {
            "use_terragrunt": false,
            "use_infracost": false
          }
        }
      },
      "worker_version": "development"
    },
    "outcome": "allow",
    "results": {
      "deny": [],
      "sample": true
    },
    "error": ""
  },
  "ts": "2021-09-02T13:17:37.785219048Z"
}
```

Great!

We can now go ahead and confirm this run:

```bash
~> spacectl stack confirm --id testing-spacelift --run-metadata "confirm-metadata" --run 01FEKAGP4AYV0DWP4QDFTANRES
You have successfully confirmed a deployment
The live run can be visited at http://cube2222.app.spacelift.tf/stack/testing-spacelift/run/01FEKAGP4AYV0DWP4QDFTANRES
```

In the policy sample log for the relevant metadata key we’ll see an additional entry, which was added when confirming:

```json
"user_provided_metadata": [
  "deploy-metadata",
  "confirm-metadata"
]
```

And that's basically it! It's a very flexible building block which lets you build various automation and compliance helper tooling.

### Run signatures

A standard use case for this feature would be to sign your runs when you’re creating them.

You'll have to bring the infrastructure for managing keys and signatures yourself - usually you'll already have something like that internally. But in short you can create a cryptographic signature of the parameters for a run you’re about to create - based on the commit SHA, run type, stack, date, etc. - and then you can pass that signature to Spacelift when creating the run.

Later, in the initialization policy you can use the [exec function](../policy/#helper-functions) to run your custom binary for verifying that signature. This way - for your most sensitive stacks - you can verify whether runs you are receiving from the Spacelift backend are legit, intentionally created by an employee of your company.
