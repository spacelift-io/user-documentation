---
description: >-
  From this article you can learn how to setup a Pulumi JavaScript Stack in
  Spacelift
---

# Python

In order to follow along with this article, you'll need an AWS account.

Start with forking the [Pulumi examples repo](https://github.com/pulumi/examples), we'll be setting up an example directory from there, namely [aws-py-webserver](https://github.com/pulumi/examples/tree/master/aws-py-webserver).

In the root of the repository (not the aws-py-webserver directory), add a new file:

```yaml title=".spacelift/config.yml"
version: "1"

stack_defaults:
  before_apply:
    - pip install -r requirements.txt
```

`before_apply` is not yet exposed through the interface like `before_init`, so you have to set it through the config file.

Now let's open Spacelift and create a new Stack, choose the examples repo you just forked. In the second step you'll have to change multiple default values:

* Set the project root to `aws-py-webserver`, as we want to run Pulumi in this subdirectory only.
* Add one before init script: `pip install -r requirements.txt`, which will install all necessary dependencies, before initializing Pulumi itself. This will need to run both when [initializing](../../../concepts/run/#initializing) and before [applying](../../../concepts/run/#applying).
* Set the runner image to `public.ecr.aws/spacelift/runner-pulumi-python:latest`
  * Pinning to a specific Pulumi version is possible too, using a tag like `v2.15.4` - you can see the available versions here.

![Define behavior.](<../../../assets/screenshots/image (44).png>)

In the third step, choose Pulumi as your Infrastructure as Code vendor. You'll have to choose:

* A state backend, aka login URL. This can be a cloud storage bucket, like `s3://pulumi-state-bucket`, but it can also be a Pulumi Service endpoint.
* A stack name, which is how the state for this stack will be namespaced in the state backend. Best to write something close to your stack name, like `my-python-pulumi-spacelift-stack`.

![Configure backend.](<../../../assets/screenshots/image (34).png>)

!!! info
    You can use `https://api.pulumi.com` as the Login URL to use the official Pulumi state backend. You'll also need to provide your Pulumi access token through the `PULUMI_ACCESS_TOKEN` environment variable.

You'll now have to set up the AWS integration for the Stack, as is described in [AWS](../../../integrations/cloud-providers/aws.md#setting-up-aws-integration).

Go into the [Environment](../../../concepts/configuration/environment.md) tab in your screen, add an **AWS\_REGION** environment variable and set it to your region of choice, i.e. `eu-central-1`.

![Configure enviornment.](<../../../assets/screenshots/image (24).png>)

You can now trigger the Run manually in the Stack view, after the planning phase is over, you can check the log to see the planned changes.

![Pending confirmation.](<../../../assets/screenshots/image (13).png>)

Confirm the run to let it apply the changes, after applying it should look like this:

![Applied](<../../../assets/screenshots/image (14).png>)

We can see the public\_dns stack output. If we try to curl it, lo and behold:

```bash
~> curl ec2-3-125-48-55.eu-central-1.compute.amazonaws.com
Hello, World!
```

In order to clean up, open the [Tasks](../../../concepts/run/task.md) tab, and perform `pulumi destroy --non-interactive --yes` there.

![Performing cleanup task.](<../../../assets/screenshots/image (5).png>)

Which will destroy all created resources.

![Destruction complete.](<../../../assets/screenshots/image (15).png>)

