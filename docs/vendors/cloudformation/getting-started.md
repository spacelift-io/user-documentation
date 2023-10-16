---
description: Creating your first AWS CloudFormation Stack with Spacelift, step by step.
---

# Getting Started

## Initial Setup

Start by forking our [AWS CloudFormation example repository](https://github.com/spacelift-io/cloudformation-example){: rel="nofollow"}

Looking at the code, you'll find that it creates two simple Lambda Functions in nested Stacks and a common API Gateway REST API, which provides access to both of them.

In Spacelift, go ahead and click the **Add Stack** button to create a Stack in Spacelift.

In the first screen, you should select the repository you've just forked, as can be seen in the picture.

![Configuring the VCS settings.](<../../assets/screenshots/Screenshot 2021-12-08 at 15.04.17.png>)

In the next screen, you should choose the **CloudFormation** backend. There, fill in the **Region** field with the AWS region you want to create the CloudFormation Stack in. You should also create an Amazon S3 bucket for template storage and provide its name in the **Template Bucket** field. **We won't automatically create this bucket.**

The **Entry Template File** should be set to _main.yaml_ (based on the code in our repository) and the **Stack Name** to a unique CloudFormation Stack name in your AWS account. We'll use _cloudformation-example_ in the pictures.

![Configuring the backend settings.](<../../assets/screenshots/Screenshot 2021-12-08 at 15.09.23.png>)

You can leave the settings on the next page (**Define Behavior)** unchanged. If you have a private worker pool you'd like to use, specify it there instead of the default public one.

Finally, choose a name for your Spacelift Stack on the last page. We'll use _cloudformation-example_ again.

![Naming the Stack.](<../../assets/screenshots/Screenshot 2021-12-08 at 15.13.29 (2).png>)

![Our newly created Stack.](<../../assets/screenshots/Screenshot 2021-12-08 at 15.13.58.png>)

**You'll also have to configure the AWS integration to give Spacelift access to your AWS account.** You can find the details here: [AWS](../../integrations/cloud-providers/aws.md)

## Deploying the Stack

You can now click Trigger to create a new Spacelift Run.

And... oh no! It failed! However, the error message is quite straightforward. We're lacking the relevant [capability](reference.md#cloudformation-stack-capabilities).

![Creating change set failed: Requires capabilities : \[CAPABILITY_IAM\]](<../../assets/screenshots/Screenshot 2021-12-08 at 15.19.52 (4).png>)

We can acknowledge this capability by setting the `CF_CAPABILITY_IAM` environment variable to `1`.

There's a bunch of optional settings for CloudFormation Stacks we expose this way. You can read up on all of them in the [reference](reference.md#special-environment-variables).

![Acknowledging the CAPABILITY_IAM capability by setting the CF_CAPABILITY_IAM environment variable.](<../../assets/screenshots/Screenshot 2021-12-08 at 15.25.59.png>)

Triggering a run again, you should successfully see it get through the planning phase and end up in the unconfirmed state.

In the plan, you can see detailed information about each resource that is supposed to be created.

![Plan details.](<../../assets/screenshots/Screenshot 2021-12-08 at 15.29.45 (1).png>)

You can also click the **ADD +10** tab to see a concise overview of the resources to be created.

![Planned creations overview.](<../../assets/screenshots/Screenshot 2021-12-08 at 15.30.05 (1).png>)

When you're happy with the planned changes, click **Confirm** to apply them.

This will show you a feed of the creation and update events happening in the root Stack and all nested Stacks, which will stop after the creation finishes.

![Resource creation feed](<../../assets/screenshots/Screenshot 2021-12-08 at 15.34.37.png>)

Great! The resources have successfully been created.

You can now switch to the **Outputs** tab and find the **URLBase** output. You can _curl_ that URL with a _hello1_ or _hello2_ suffix to get responses from your Lambda Functions.

![Stack Outputs](<../../assets/screenshots/Screenshot 2021-12-08 at 15.37.51.png>)

![Calling the created Lambda Functions.](<../../assets/screenshots/Screenshot 2021-12-08 at 15.38.49.png>)

You can also switch to the **Resources** tab to explore the resources you've created.

![Exploring the created resources.](<../../assets/screenshots/Screenshot 2021-12-08 at 15.40.32.png>)

## Conclusion

That's it! You can find more details about the available configuration settings in the [reference](reference.md), or you can check out how to use [AWS Serverless Application Model (SAM)](integrating-with-sam.md) or the [Serverless Framework](integrating-with-the-serverless-framework.md) to generate your CloudFormation templates.
