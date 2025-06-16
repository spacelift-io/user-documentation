---
description: Consuming Spacelift data in Datadog
---

# Datadog integration

Spacelift can send data to Datadog to help you monitor your infrastructure and Spacelift stacks using Datadog's excellent monitoring and analytics tools. Our integration with Datadog focuses primarily on runs and lets you create dashboards and alerts to answer questions like:

- How many runs are failing?
- Which stacks see the most activity?
- How long does it take to plan a given stack?
- How long does it take to apply a stack?
- What is the load on my Spacelift private workers?
- How many resources am I changing?
- ...and many more!

Here's a very simple dashboard we've created based on this integration that shows the performance of our continuous regression tests:

![Dashboard screenshot](../../assets/screenshots/datadog-screenshot.png)

If you'd like to use the same dashboard, the JSON is provided below.

<details> <!-- markdownlint-disable-line MD033 -->
<summary>Click to expand</summary> <!-- markdownlint-disable-line MD033 -->

{% raw %}

```json
{
  "title": "Spacelift CI performance",
  "description": "",
  "widgets": [
    {
      "id": 1204455947489370,
      "definition": {
        "title": "Overall time spent",
        "title_size": "16",
        "title_align": "left",
        "show_legend": true,
        "legend_layout": "auto",
        "legend_columns": ["avg", "min", "max", "value", "sum"],
        "type": "timeseries",
        "requests": [
          {
            "formulas": [{ "formula": "query1" }],
            "queries": [
              {
                "name": "query1",
                "data_source": "metrics",
                "query": "sum:spacelift.integration.run.timing{$Space AND $Stack AND $Environment AND $WorkerPool AND state NOT IN (queued,confirmed,unconfirmed)} by {state}"
              }
            ],
            "response_format": "timeseries",
            "style": {
              "palette": "dog_classic",
              "line_type": "solid",
              "line_width": "normal"
            },
            "display_type": "bars"
          }
        ]
      },
      "layout": { "x": 0, "y": 0, "width": 6, "height": 4 }
    },
    {
      "id": 4165236413630572,
      "definition": {
        "title": "Resource changes",
        "title_size": "16",
        "title_align": "left",
        "show_legend": true,
        "legend_layout": "auto",
        "legend_columns": ["avg", "min", "max", "value", "sum"],
        "type": "timeseries",
        "requests": [
          {
            "formulas": [{ "formula": "query1" }],
            "queries": [
              {
                "name": "query1",
                "data_source": "metrics",
                "query": "sum:spacelift.integration.run.resources{$Space,$Stack,$Environment,run_type:tracked} by {change_type}.as_count()"
              }
            ],
            "response_format": "timeseries",
            "style": {
              "palette": "dog_classic",
              "line_type": "solid",
              "line_width": "normal"
            },
            "display_type": "bars"
          }
        ]
      },
      "layout": { "x": 6, "y": 0, "width": 6, "height": 4 }
    },
    {
      "id": 7535326510979494,
      "definition": {
        "title": "Run outcomes",
        "title_size": "16",
        "title_align": "left",
        "show_legend": true,
        "legend_layout": "auto",
        "legend_columns": ["avg", "min", "max", "value", "sum"],
        "type": "timeseries",
        "requests": [
          {
            "formulas": [{ "formula": "query1" }],
            "queries": [
              {
                "name": "query1",
                "data_source": "metrics",
                "query": "sum:spacelift.integration.run.count{$Space,$Stack,$Environment} by {final_state}.as_count()"
              }
            ],
            "response_format": "timeseries",
            "style": {
              "palette": "dog_classic",
              "line_type": "solid",
              "line_width": "normal"
            },
            "display_type": "bars"
          }
        ]
      },
      "layout": { "x": 0, "y": 4, "width": 6, "height": 4 }
    },
    {
      "id": 3687311929209224,
      "definition": {
        "title": "Worker pool usage",
        "title_size": "16",
        "title_align": "left",
        "show_legend": true,
        "legend_layout": "auto",
        "legend_columns": ["avg", "min", "max", "value", "sum"],
        "type": "timeseries",
        "requests": [
          {
            "formulas": [{ "formula": "query1" }],
            "queries": [
              {
                "name": "query1",
                "data_source": "metrics",
                "query": "sum:spacelift.integration.run.count{$Environment,$Space} by {worker_pool}.as_count()"
              }
            ],
            "response_format": "timeseries",
            "style": {
              "palette": "dog_classic",
              "line_type": "solid",
              "line_width": "normal"
            },
            "display_type": "bars"
          }
        ]
      },
      "layout": { "x": 6, "y": 4, "width": 6, "height": 4 }
    },
    {
      "id": 3469740549844082,
      "definition": {
        "title": "Drift detection load",
        "title_size": "16",
        "title_align": "left",
        "show_legend": true,
        "legend_layout": "auto",
        "legend_columns": ["avg", "min", "max", "value", "sum"],
        "type": "timeseries",
        "requests": [
          {
            "formulas": [{ "formula": "query1" }],
            "queries": [
              {
                "name": "query1",
                "data_source": "metrics",
                "query": "sum:spacelift.integration.run.count{$Environment,$Space,$WorkerPool,$Stack} by {drift_detection}.as_count()"
              }
            ],
            "response_format": "timeseries",
            "style": {
              "palette": "dog_classic",
              "line_type": "solid",
              "line_width": "normal"
            },
            "display_type": "bars"
          }
        ]
      },
      "layout": { "x": 0, "y": 8, "width": 6, "height": 3 }
    },
    {
      "id": 2802853783337572,
      "definition": {
        "title": "Plan policy outcomes",
        "title_size": "16",
        "title_align": "left",
        "show_legend": true,
        "legend_layout": "auto",
        "legend_columns": ["avg", "min", "max", "value", "sum"],
        "type": "timeseries",
        "requests": [
          {
            "formulas": [{ "formula": "query1" }],
            "queries": [
              {
                "name": "query1",
                "data_source": "metrics",
                "query": "sum:spacelift.integration.run.policies{$Environment,$Space,$WorkerPool,$Stack,policy_type:plan} by {policy_outcome}"
              }
            ],
            "response_format": "timeseries",
            "style": {
              "palette": "dog_classic",
              "line_type": "solid",
              "line_width": "normal"
            },
            "display_type": "bars"
          }
        ]
      },
      "layout": { "x": 6, "y": 8, "width": 6, "height": 3 }
    }
  ],
  "template_variables": [
    {
      "name": "Environment",
      "prefix": "env",
      "available_values": ["preprod", "prod"],
      "default": "*"
    },
    {
      "name": "Space",
      "prefix": "space",
      "available_values": [],
      "default": "*"
    },
    {
      "name": "WorkerPool",
      "prefix": "worker_pool",
      "available_values": [],
      "default": "*"
    },
    {
      "name": "Stack",
      "prefix": "stack",
      "available_values": [],
      "default": "*"
    }
  ],
  "layout_type": "ordered",
  "notify_list": [],
  "reflow_type": "fixed",
  "tags": []
}
```

{% endraw %}

</details>

## Prerequisites

The Datadog integration is based on our [notification policy](../../concepts/policy/notification-policy.md) feature, which requires at least an active [Cloud tier](https://spacelift.io/pricing){: rel="nofollow"} subscription. While building a notification-based Datadog integration from scratch is possible, we've created a [Terraform module](https://registry.terraform.io/modules/spacelift-io/datadog/spacelift/latest){: rel="nofollow"} that will set up all the necessary integration elements for you.

This module will only create Spacelift assets:

- a [notification policy](../../concepts/policy/notification-policy.md) that will send data to Datadog;
- a [webhook endpoint](../webhooks.md) that serve as a notification target for the policy;
- a webhook secret header that will securely authenticate the payload with Datadog;

## Setting up the integration

To set up the integration, you'll need to have a [Datadog account](https://www.datadoghq.com/){: rel="nofollow"} and a [Datadog API key](https://docs.datadoghq.com/account_management/api-app-keys/#api-keys){: rel="nofollow"}. If you don't have an administrative stack declaratively manage your Spacelift resources, we suggest you create one, and add module instantiation to it according to its usage instructions. We suggest that you pass the Datadog API key as a [stack secret](../../concepts/configuration/environment.md#environment-variables), or - even better - retrieve it from a remote secret store (eg. AWS Parameter Store) using Terraform.

If you intend to monitor your entire account (our suggested approach), we suggest that the module is installed in the [root space](../../concepts/spaces/access-control.md) of your Spacelift account. If you only want to monitor a subset of your stacks, you can install the module in their respective space.

## Metrics

The following metrics are sent:

- `spacelift.integration.run.count` (counter) - a simple count of runs;
- `spacelift.integration.run.timing` (counter, nanoseconds) - the duration of different run states. In addition to [common tags](#common-tags), this metric is also tagged with the state name, eg. `state:planning`, `state:applying`, etc.;
- `spacelift.integration.run.resources` (counter) - the resources affected by a run. In addition to [common tags](#common-tags), this metric is also tagged with the change type, eg. `change_type:added`, `change_type:changed`, etc.;

## Common tags

Common tags for all metrics are the following:

- `account` (string) : name of the Spacelift account generating the metric;
- `branch` (string): name of the Git branch the run was triggered from;
- `drift_detection` (boolean): whether the run was triggered by drift detection;
- `run_type` (string): type of a run, eg. "tracked", "proposed", etc.;
- `run_url` (string): link to the run that generated the metric;
- `final_state` (string): the terminal state of the run, eg. "finished", "failed", etc.;
- `space` (string): name of the Spacelift space the run belongs to;
- `stack` (string): name of the Spacelift stack the run belongs to;
- `worker_pool` (string): name of the Spacelift worker pool the run was executed on - for the public worker pool this value is always `public`;

## Extending the integration

The benefit of building this integration on top of a notification policy is that you can easily extend it to send additional data to Datadog, change the naming of your metrics, change the tags, etc. To do so, you'll need to edit the policy body generated by the module. You can do so by editing the policy in the Spacelift UI, or by forking the module and editing the policy body in the module's source code.

Note that this is an advanced feature, and we recommend that you only do so if you're already familiar with Spacelift's notification policy feature and Datadog's API, or are willing to learn about them.
