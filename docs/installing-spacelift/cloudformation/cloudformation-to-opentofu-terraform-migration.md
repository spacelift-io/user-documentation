---
description: Moving from Cloudformation-based installation to the reference architecture
---

# CloudFormation to OpenTofu/Terraform migration

If you seek to migrate from the Cloudformation-based installation to the reference architecture, we developed [a small migration toolkit to help you with the process](https://github.com/spacelift-io/self-hosted-v2-to-v3-kit){: rel="nofollow"}.

The end result will be similar to the [ECS guide](../reference-architecture/guides/deploying-to-ecs.md) with the following differences:

- the message queue will remain SQS as opposed to Postgres
- the MQTT server will remain IoT Core as opposed to the built-in server

The migration process **does not require any downtime**. It pulls up a new application (ECS) environment in parallel to the existing one so that you can test it before switching over.

!!! note
    The most important resources are the persistence layer: the S3 buckets and the RDS cluster. Both of those resources are protected by default. S3 buckets cannot be removed as long as they have objects in them and the RDS cluster has deletion protection enabled by default.

In short, the migration process looks like this:

- the script ensures the prerequisites are met (you're at least on Self-Hosted v2.6.0 version)
- the Python script will read your Cloudformation stacks and generate an equivalent Terraform project, which will include various of import statements to import your Cloudformation-managed infrastructure into Terraform
- the Terraform code will also create a brand new load balancer and an ECS cluster which will connect to the exact same AWS resources as the old one
- once you have confirmed the new ECS cluster's services are looking good, you can point your website's DNS to the new load balancer
- you can manually scale down the services' desired count to 0 in the old ECS cluster
- ideally, you should test this new environment for a few days before deleting the old one
- once you are happy with the new environment, you can delete the old one by running the `delete_cf_stacks.py` Python script which will make sure to retain the required resources and delete the rest
- there are a few leftover resources that you can delete manually
  
!!! warning
    Be extra careful when applying the Terraform changes. Look out for resource deletion and replacements. Note that we have some minor differences in the new Terraform modules compared to the old Cloudformation templates (different wording in the ECR lifecycle policy, slightly different S3 retention policy, different tags for the gateways etc.) but those are completely safe. On the other hand, you definitely don't want to see RDS instance or subnet replacements.
  
## CloudFormation stack deletion approach

One of the reasons the Cloudformation stack deletion requires such a complex Python script is a Cloudformation quirk. Cloudformation can retain resources when deleting a stack, **but only if the stack is in the `DELETE_FAILED` state**. We're using [a workaround](https://gist.github.com/magnetikonline/51bbb3de48dc4a10e11f38f9d911ac08){: rel="nofollow"} to achieve this: first, attempt to delete the stack with a "weak" IAM role that doesn't have permissions to delete the resources. This will put the stack in the `DELETE_FAILED` state. Afterwards, we can delete the stack with an administrator IAM role that has permissions to delete the resources. At this point, we can specify the retained resources. The script will delete both temporary IAM roles (weak, admin) after it is done.

The exact steps can be found in the [README of the repository](https://github.com/spacelift-io/self-hosted-v2-to-v3-kit){: rel="nofollow"}.
