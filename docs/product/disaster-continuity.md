---
description: >-
  A collection of preparation items and procedures that can be used to assist
  Spacelift Users in their disaster recovery preparation.
---

# Disaster Continuity

## Preparation

The following preparation items are recommended to be followed to ensure that you are able to continue with your infrastructure as code deployments in the event of a Spacelift outage.

### State Management

Here is a list of best practices that should be followed in regards to managing the state of your infrastructure.

- Store your state externally (e.g. Amazon S3 Bucket)
- Enable versioning on your state file to keep a record of changes
- Replicate your state file across regions
- Enable MFA on deletion to prevent accidental loss of your state file

### Deployment Roles

Within your Spacelift configuration, each Spacelift stack utilizes a given Role for deployment purposes. We will be referring to this Role as the **deployment role**.

In the event of a disaster, Spacelift will presumably not be accessible or usable. You should ensure that you have appropriate access to your deployment role, to provide yourself the ability to assume it for deployment purposes, or have plans to use another role for deployment purposes.

- Keep a record of all Roles used by your Spacelift Stacks that are used for deployment purposes
- Ensure that you've done one of the following:
- Provided yourself access to the deployment role that Spacelift is using
- Have a plan to create, or have already created a break-glass role that you can use for disaster purposes

## Terraform Break Glass Example Procedure

### Pre-requisites

- Access to assume your deployment role(s)
- Terraform installed locally
- Managing your state externally (not Spacelift-managed state)

### Assume deployment role locally

Using your favorite cloud provider, generate temporary credentials for your deployment role. With Amazon Web Services for example, this would be done using the following command:

```bash
aws sts assume-role \
  --role-arn <your-deployment-role-arn> \
  --role-session-name local-infra-deployment
```

Using the output from the **assume-role** command, set your credentials in your shell.

```bash
export AWS_ACCESS_KEY_ID=<value for access key id>
export AWS_SECRET_ACCESS_KEY=<value for secret access key>
export AWS_SESSION_TOKEN=<value for session toknen>
```

### Run deployment commands as required

Initialize your code locally:

```bash
terraform init
```

To preview changes to be deployed:

```bash
terraform plan
```

To deploy changes:

```bash
terraform apply
```
