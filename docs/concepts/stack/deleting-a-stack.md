# Deleting a Stack

When you are ready to delete your stack, you can do so by navigating to your stack settings and clicking on the delete button. You will get a warning first to let you know that deleting this stack does not delete any of the resources that this stack manages.

![](<../../assets/screenshots/delete-a-stack.png>)

## Deleting Resources Managed by a Stack

Depending on the backend of your stack, there are different commands you can run as a [task](../run/task.md) before deleting the stack.

| Backend           | Command                                        |
| -------------- | ------------------------------------------------------------ |
| **Terraform**       | `terraform destroy -auto-approve`           |
| **Cloudformation**      | `aws cloudformation delete-stack --stack-name <cloudformation-stack-name>` |
| **Pulumi** | `pulumi destroy --non-interactive --yes` |
| **Kubernetes** | `kubectl delete --ignore-not-found -l spacelift-stack=<stack-slug> $(kubectl api-resources --verbs=list,create -o name &#124; paste -s -d, -)` |

!!! tip
    For Terraform, you can also run a task through our CLI tool [spacectl](../../vendors/terraform/provider-registry.md#use-our-cli-tool-called-spacectl).

## Scheduled Delete

If you would like to schedule to delete a stack, please see our documentation on [Scheduling](../stack/scheduling.md).

## Using the API

If you would like to delete a stack using our API, please see our documentation on GraphQL [API](../../integrations/api.md).
