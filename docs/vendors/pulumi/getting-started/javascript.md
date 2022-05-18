---
description: >-
  From this article you can learn how to setup a Pulumi JavaScript Stack in
  Spacelift
---

# Javascript

In order to follow along with this article, you'll need an AWS account.

Start with forking the [Pulumi examples repo](https://github.com/pulumi/examples){: rel="nofollow"}, we'll be setting up an example directory from there, namely [aws-js-webserver](https://github.com/pulumi/examples/tree/master/aws-js-webserver){: rel="nofollow"}.

Now let's open Spacelift and create a new Stack, choose the examples repo you just forked. In the second step you'll have to change multiple default values:

- Set the project root to `aws-js-webserver`, as we want to run Pulumi in this subdirectory only.
- Add one before init script: `npm install`, which will install all necessary dependencies, before initializing Pulumi itself. The outputs will be persisted in the workspace and be there for the [Planning](../../../concepts/run/#planning) and [Applying](../../../concepts/run/#applying) phases.
- Set the runner image to `public.ecr.aws/spacelift/runner-pulumi-javascript:latest`
- Pinning to a specific Pulumi version is possible too, using a tag like `v2.15.4` - you can see the available versions [here](https://gallery.ecr.aws/spacelift/runner-pulumi-javascript){: rel="nofollow"}.

![Define behavior.](<../../../assets/screenshots/image (43).png>)

In the third step, choose Pulumi as your Infrastructure as Code vendor. You'll have to choose:

- A state backend, aka login URL. This can be a cloud storage bucket, like `s3://pulumi-state-bucket`, but it can also be a Pulumi Service endpoint.
- A stack name, which is how the state for this stack will be namespaced in the state backend. Best to write something close to your stack name, like `my-javascript-pulumi-spacelift-stack`.

![Configure backend.](<../../../assets/screenshots/image (36).png>)

!!! info
    You can use `https://api.pulumi.com` as the Login URL to use the official Pulumi state backend. You'll also need to provide your Pulumi access token through the `PULUMI_ACCESS_TOKEN` environment variable.

You'll now have to set up the AWS integration for the Stack, as is described in [AWS](../../../integrations/cloud-providers/aws.md#setting-up-aws-integration).

Go into the [Environment](../../../concepts/configuration/environment.md) tab in your screen, add an `AWS_REGION` environment variable and set it to your region of choice, i.e. `eu-central-1`.

![Configure environment.](<../../../assets/screenshots/image (22).png>)

You can now trigger the Run manually in the Stack view, after the planning phase is over, you can check the log to see the planned changes.

![Pending confirmation.](<../../../assets/screenshots/image (3).png>)

Confirm the run to let it apply the changes, after applying it should look like this:

![Applied](<../../../assets/screenshots/image (4).png>)

We can see the publicHostName stack output. If we try to curl it, lo and behold:

```bash
~> curl ec2-18-184-240-9.eu-central-1.compute.amazonaws.com
Hello, World!
```

In order to clean up, open the [Tasks](../../../concepts/run/task.md) tab, and perform `pulumi destroy --non-interactive --yes` there.

![Performing cleanup task.](<../../../assets/screenshots/image (5).png>)

Which will destroy all created resources.

![Destruction complete.](<../../../assets/screenshots/image (6).png>)
