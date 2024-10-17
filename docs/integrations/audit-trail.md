# Audit trail

!!! info
    Note that Audit Trail is an Enterprise plan feature.

Spacelift supports auditing all operations that change Spacelift resources. We provide a built-in audit log as well as webhook functionality to allow you to optionally store your audit logs in a third party system.

## Built-in logs

As an admin, you can view Audit trail logs by navigating to the Audit trail section of your account settings and choosing the _logs_ tab:

![](<../assets/screenshots/audit-trail-logs.png>)

You can look for specific events using filters (on the left side) and the date picker (in the top-right corner).

![](<../assets/screenshots/audit-trail-logs-filters.png>)

You can see the details:

![](<../assets/screenshots/audit-trail-logs-details-button.png>)
![](<../assets/screenshots/audit-trail-logs-details.png>)

You can also go to the affected resource or apply another filter:

![](<../assets/screenshots/audit-trail-logs-dropdown.png>)

### Retention

Logs are kept for 30 days.

## Webhook Setup

In order to set up the audit trail, navigate to the Audit trail section of your account settings and choosing the _configuration_ tab, and click the _Set up_ button:

![](<../assets/screenshots/audit-trail-page.png>)

You will then need to provide a webhook endpoint and an arbitrary secret that you can later use for [verifying payload](audit-trail.md#verifying-payload).
Optionally you can specify the custom headers that will be added to each HTTP request and enable `Include runs` option, which controls whether run state change events will be sent to the audit webhook in addition to standard audit events.
Let's use ngrok for the purpose of this tutorial:

![](<../assets/screenshots/setup-audit-trail.png>)

If you choose to automatically enable the functionality, clicking the _Save_ button will verify that payloads can be delivered (the endpoint returns a 2xx status code). This gives us an opportunity to look at the payload:

```json
{
  "account": "example",
  "action": "audit_trail_webhook.set",
  "actor": "github::name",
  "context": {
    "mutation": "auditTrailSetWebhook"
  },
  "data": {
    "args": {
      "Enabled": true,
      "Endpoint": "https://example-audithook.com/",
      "SecretSHA": "xxxfffdddwww"
    }
  },
  "remoteIP": "0.0.0.0",
  "timestamp": 1674124447947
}
```

...and the headers - the interesting ones are highlighted:

![](<../assets/screenshots/ngrok_-_Inspect (1).png>)

### Usage

Every audit trail payload conforms to the same schema:

- `account`: name (subdomain) of the affected Spacelift account;
- `action`: name of the performed action;
- `actor`: actor performing the action - the `::` format shows both the actor identity (second element), and the source of the identity (first element)
- `context`: some contextual metadata about the request;
- `data`: action-specific payload showing arguments passed to the request. Any sensitive arguments (like secrets) are sanitized;

Below is a sample:

```json
{
  "account": "example",
  "action": "stack.create",
  "actor": "github::name",
  "context": {
    "mutation": "stackCreate"
  },
  "data": {
    "ID": "audit-trail-demo",
    "args": {
      "Input": {
        "Administrative": false,
        "AfterApply": [],
        "AfterDestroy": [],
        "AfterInit": [],
        "AfterPerform": [],
        "AfterPlan": [],
        "AfterRun": [],
        "Autodeploy": false,
        "Autoretry": false,
        "BeforeApply": [],
        "BeforeDestroy": [],
        "BeforeInit": [],
        "BeforePerform": [],
        "BeforePlan": [],
        "Branch": "showcase",
        "Description": "",
        "GithubActionDeploy": true,
        "IsDisabled": null,
        "Labels": [],
        "LocalPreviewEnabled": false,
        "Name": "audit-trail-demo",
        "Namespace": "spacelift-io",
        "ProjectRoot": "",
        "ProtectFromDeletion": false,
        "Provider": "SHOWCASE",
        "Repository": "terraform-starter",
        "RunnerImage": null,
        "Space": "legacy",
        "TerraformVersion": null,
        "VendorConfig": {
          "Ansible": null,
          "CloudFormation": null,
          "Kubernetes": null,
          "Pulumi": null,
          "Terraform": {
            "use_smart_sanitization": null,
            "version": "1.3.7",
            "workspace": null
          }
        },
        "WorkerPool": null
      },
      "ManageState": true,
      "Slug": null,
      "StackObjectID": null
    }
  },
  "remoteIP": "0.0.0.0",
  "timestamp": 1674124447947
}
```

### Disabling and deleting the audit trail

The audit trail can be disabled and deleted at any point, but for both events we will send the appropriate payload. We suggest that you always treat these at least as important security signals, if not alerting conditions:

```json
{
  "account": "example",
  "action": "audit_trail_webhook.delete",
  "actor": "github::user",
  "context": {
    "mutation": "auditTrailDeleteWebhook"
  },
  "data": {},
  "remoteIP": "0.0.0.0",
  "timestamp": 1674124447947
}
```

### Verifying payload

Spacelift uses the same similar verification mechanism as GitHub. With each payload we send 2 headers, `X-Signature` and `X-Signature-256`. `X-Signature` header contains the SHA1 hash of the payload, while `X-Signature-256` contains the SHA256 hash. We're using the exact same mechanism as GitHub to generate signatures, please refer to [this article](https://medium.com/@vampiire/how-to-verify-the-authenticity-of-a-github-apps-webhook-payload-8d63ccc81a24){: rel="nofollow"} for details.

### Sending logs to AWS

We provide a [reference implementation](https://github.com/spacelift-io-examples/terraform-aws-spacelift-events-collector){: rel="nofollow"} for sending the Audit Trail logs to an AWS S3 bucket.

It works as-is but can also be tweaked to route the logs to other destinations with minimal effort.

### Failures

Audit trail deliveries are retried on failure.
