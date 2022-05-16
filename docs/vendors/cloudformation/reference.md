---
description: Details about all available CloudFormation-specific configuration options.
---

# Reference

## Stack Settings

* **Region** - AWS region in which to create and execute the CloudFormation Stack.
* **Stack Name** - The name for the CloudFormation Stack controlled by this Spacelift Stack.
* **Entry Template File** - The path to the JSON or YAML file describing your root CloudFormation Stack. If you're generating CloudFormation code using a tool like SAM, point this to the file containing the generated template.
* **Template Bucket** - S3 bucket to store CloudFormation templates in. Each created object will be prefixed by the current run ID like this: `<run id>/artifact_name`

## Special Environment Variables

### CloudFormation Stack Parameters

Use this if your CloudFormation template requires parameters to be specified.

Each environment variable of the form **CF\_PARAM\_xyz** will be interpreted as the value for the parameter _xyz_.

For example, with this template snippet:

```yaml
Parameters:
  InstanceTypeParameter:
    Type: String
    AllowedValues:
      - t2.micro
      - t2.small
    Description: Enter t2.micro or t2.small.
```

In order to specify the InstanceTypeParameter add an environment variable to your Stack **CF\_PARAM\_InstanceTypeParameter** and set its value to i.e. _t2.micro_

### CloudFormation Stack Capabilities

Some functionalities available to CloudFormation Stacks need to be explicitly acknowledged using [capabilities](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities). You can configure capabilities in Spacelift using environment variables of the form **`CF_CAPABILITY_xyz`** and set them to 1.

As of the time of writing this page, available capabilities are `CF_CAPABILITY_IAM`, `CF_CAPABILITY_NAMED_IAM,` and `CF_CAPABILITY_AUTO_EXPAND`. Detailed descriptions can be found in the [AWS API documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/APIReference/API_CreateChangeSet.html).

## Available Computed Environment Variables

To ease writing reusable scripts and hooks for your CloudFormation Stacks, the following environment variables are computed for each run: `CF_METADATA_REGION`, `CF_METADATA_STACK_NAME`, `CF_METADATA_ENTRY_TEMPLATE_FILE`, `CF_METADATA_TEMPLATE_BUCKET`.

Their values are set to the respective [Stack settings](reference.md#stack-settings).

## Permissions

You need to provide Spacelift with access to your AWS account. You can either do this using the [AWS Integration](../../integrations/cloud-providers/aws.md), provide ambient credentials on private workers, or pass environment variables directly.
