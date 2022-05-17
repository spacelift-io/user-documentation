---
description: From this article you can learn how to setup a Pulumi Go Stack in Spacelift
---

# Go

In order to follow along with this article, you'll need an AWS account.

Start with forking the [Pulumi examples repo](https://github.com/pulumi/examples), we'll be setting up an example directory from there, namely [aws-go-s3-folder](https://github.com/pulumi/examples/tree/master/aws-go-s3-folder).

Now let's open Spacelift and create a new Stack, choose the examples repo you just forked. In the second step you'll have to change multiple default values:

* Set the project root to `aws-go-s3-folder`, as we want to run Pulumi in this subdirectory only.
* Set the runner image to `public.ecr.aws/spacelift/runner-pulumi-golang:latest`
  * Pinning to a specific Pulumi version is possible too, using a tag like `v2.15.4` - you can see the available versions [here](https://gallery.ecr.aws/spacelift/runner-pulumi-golang).

![Define behavior.](<../../../assets/screenshots/image (42).png>)

In the third step, choose Pulumi as your Infrastructure as Code vendor. You'll have to choose:

* A state backend, aka login URL. This can be a cloud storage bucket, like `s3://pulumi-state-bucket`, but it can also be a Pulumi Service endpoint.
* A stack name, which is how the state for this stack will be namespaced in the state backend. Best to write something close to your stack name, like `my-golang-pulumi-spacelift-stack`.

![Configure backend.](<../../../assets/screenshots/image (37).png>)

!!! info
    You can use `https://api.pulumi.com` as the Login URL to use the official Pulumi state backend. You'll also need to provide your Pulumi access token through the `PULUMI_ACCESS_TOKEN` environment variable.

You'll now have to set up the AWS integration for the Stack, as is described in [AWS](../../../integrations/cloud-providers/aws.md#setting-up-aws-integration).

Go into the [Environment](../../../concepts/configuration/environment.md) tab in your screen, add an `AWS_REGION` environment variable and set it to your region of choice, i.e. `eu-central-1`.

![Configure environment.](<../../../assets/screenshots/image (23).png>)

You can now trigger the Run manually in the Stack view, after the planning phase is over, you can check the log to see the planned changes.

![Pending confirmation.](<../../../assets/screenshots/image (8).png>)

Confirm the run to let it apply the changes, after applying it should look like this:

![Applied](<../../../assets/screenshots/image (9).png>)

We can see the websiteUrl stack output. If we try to curl it, lo and behold:

```bash
~> curl s3-website-bucket-b47a23a.s3-website.eu-central-1.amazonaws.com
<html><head>
    <title>Hello S3</title><meta charset="UTF-8">
    <link rel="shortcut icon" href="/favicon.png" type="image/png">
</head>
<body><p>Hello, world!</p><p>Made with ❤️ with <a href="https://pulumi.com">Pulumi</a></p>
</body></html>
```

In order to clean up, open the [Tasks](../../../concepts/run/task.md) tab, and perform `pulumi destroy --non-interactive --yes` there.

![Performing cleanup task.](<../../../assets/screenshots/image (5).png>)

Which will destroy all created resources.

![Destruction complete.](<../../../assets/screenshots/image (11).png>)
