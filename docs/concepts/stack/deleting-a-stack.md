# Deleting a Stack

When you are ready to delete your stack, you can do so by navigating to your stack settings and clicking on the delete button. You will get a warning first to let you know that deleting this stack does not delete any of the resources that this stack manages.

![](<../../assets/screenshots/delete-a-stack.png>)

## Deleting Resources Managed by a Stack

Depending on the backend of your stack, there are different ways you can delete the resources managed by your stack.

## Terraform

To delete the resources managed by a stack with a terraform backend, you can run `terraform destroy -auto-approve` as a [task](../run/task.md) before you delete the stack.

## Cloudformation

To delete the resources managed by a stack with a cloudformation backend, you can run `aws cloudformation delete-stack --stack-name <cloudformation-stack-name>` as a [task](../run/task.md) before you delete the stack.

## Pulumi

To delete the resources managed by a stack with a pulumi backend, you can run `destroy --non-interactive --yes` as a [task](../run/task.md) before you delete the stack.

## Kubernetes

To delete the resources managed by a stack with a kubernetes backend, you can run `kubectl delete --ignore-not-found -l spacelift-stack=<stack-slug> $(kubectl api-resources --verbs=list,create -o name | paste -s -d, -)` as a [task](../run/task.md) before you delete the stack.

!!! info
    You can also run a task through our cli tool [spacectl](../../vendors/terraform/provider-registry.md#use-our-cli-tool-called-spacectl)

## Scheduled Delete

If you would like to schedule to delete a stack, please see our documentation on [Scheduling](../stack/scheduling.md).

## Using the API

If you would like to delete a stack using our API, please see our documentation on GraphQL [API](../../integrations/api.md).
