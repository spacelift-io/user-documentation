# Drift detection

## **Drift happens**

In _infrastructure-as-code_, the concept of _drift_ represents the difference between the desired and the actual state of the infrastructure managed by your tool of choice - [Terraform](https://www.terraform.io), [Pulumi](https://www.pulumi.com), [CloudFormation](https://aws.amazon.com/cloudformation/), etc. In practice, there are two sources of _drift_.

The first source covers changes directly introduced by external actors - either humans or machines (scripts). If an on-call SRE changes your database parameters otherwise controlled by Terraform, you've introduced _drift_. If an external script updates your Kubernetes cluster in a way that conflicts with its Pulumi definition, it's _drift_ as well.

The other source of drift comes from the dependency of your resources on external data sources. For example, if your load balancer only expects to receive traffic from [Cloudflare](https://www.cloudflare.com/en-gb/), you may want to restrict ingress to a predefined range of IPs. However, that range may be dynamic, and your IaC tool queries it every time it runs. If there's any change to the external data source, it's showing up as drift, too.

In the first scenario, drift is an unwanted by-product of emergencies or broken processes. In the latter, it's both desired and inevitable - it's proof that your otherwise declarative system responds to external changes. In other words - drift happens, so deal with it. 😎

## How Spacelift helps

Spacelift comes with a built-in mechanism to detect and - optionally - reconcile drift. We do it by periodically executing [proposed runs](../run/proposed.md) on your stable infrastructure (in Spacelift, we generally represent it by the [FINISHED stack state](./#stack-state)) and checking for any changes.

To get started, create a drift detection configuration from the Integrations section of your stack settings. You will be able to add multiple cron rules to define when your reconciliation jobs should be scheduled, as well as decide whether you want your jobs to trigger [tracked runs](../run/tracked.md) ([reconciliation](drift-detection.md#to-reconcile-or-not-to-reconcile) jobs) in response to detected drift**:**

![](../../assets/screenshots/Edit\_stack\_·\_Test\_github\_packages\_tf.png)

!!! info
    Note that, at least currently, drift detection only works on private workers.

### To reconcile, or not to reconcile

We generally suggest turning reconciliation "on" as it ensures that you get the most out of drift detection. Reconciliation jobs are equivalent to manually triggering [tracked runs](../run/tracked.md) and obey the same rules and constraints. In particular, they respect their stacks' auto-deploy setting and trigger plan policies - see [this section](drift-detection.md#policy-input) for more details.

However, if you choose not to reconcile changes, you can still get value out of drift detection - in this case, drifted resources can be seen in the Resources view, both on the stack and account level. **** Also, drift detection jobs trigger [webhooks](../../integrations/webhooks.md) like regular runs, where they're clearly marked as such (`driftDetection` field).

![Resource marked as drifted in the stack's Resources view](<../../assets/screenshots/Spacelift (4).png>)

## Drift detection in practice

With drift detection enabled on the stack, [proposed runs](../run/proposed.md) are quietly executing in the background. If they do not detect any changes, the only way you'd know about them is by viewing all runs in the _Account > Runs_ section and filtering or grouping by drift detection parameter - here is an example:

![](<../../assets/screenshots/Spacelift (5).png>)

But once your job detects drift (and you've enabled [reconciliation](drift-detection.md#to-reconcile-or-not-to-reconcile)), it triggers a regular tracked run. This run is subject to the same rules as a regular tracked run is. For example, if you set your stack not to [deploy changes automatically](stack-settings.md#autodeploy), the run will end up in an [_Unconfirmed_](../run/tracked.md#unconfirmed) state, waiting for your decision. The same thing will happen if a [plan policy](../policy/terraform-plan-policy.md) produces a warning using a matched `warn` rule.

## Policy input

The only real difference between a drift detection job and one triggered manually is that the run section of your policy input will have the `drift_detection` field set to `true` - and this applies to both [plan](../policy/terraform-plan-policy.md) and [trigger](../policy/trigger-policy.md) policies. You can use this mechanism to add extra controls to your drift detection strategy. For example, if you're automatically deploying your changes but want a human to look at drift before reconciling it, you can add the following section to your [plan policy](../policy/terraform-plan-policy.md) body:

```yaml
warn["Drift reconciliation requires manual approval"] {
  input.spacelift.run.drift_detection
}
```
