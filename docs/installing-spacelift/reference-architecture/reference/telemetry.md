---
description: Telemetry reference documentation.
---

# Telemetry

The Spacelift backend services emit telemetry data that can be collected and visualised using a variety of tools. This document describes how to configure Spacelift to emit those data.

## Supported telemetry backends

The telemetry backend can be set by configuring the `OBSERVABILITY_VENDOR` environment variable. The following backends are supported:

| Backend       | Environment variable value | Notes                                                                           |
| ------------- | -------------------------- | ------------------------------------------------------------------------------- |
| Datadog       | `Datadog`                  | Uses the Datadog agent for both tracing and metrics.                            |
| AWS X-Ray     | `AWS`                      | Uses the AWS X-Ray daemon for tracing and CloudWatch for metrics.               |
| OpenTelemetry | `OpenTelemetry`            | Uses the OpenTelemetry collector for both tracing and metrics.                  |
| Disabled      | `Disabled`                 | Disables telemetry collection entirely. Same effect as not having the variable. |

!!! note
    All of our services (server, drain, scheduler and workers) support the `OBSERVABILITY_VENDOR` configuration.

!!! note
    When using X-Ray, make sure `cloudwatch:PutMetricsData` IAM permission is granted to the service's role.

## Configuration options

All backends share a common requirement: the only mandatory configuration is the respective agent's address, provided as an environment variable. Additional settings are optional.

!!! note
    Spacelift automatically sets the service name based on the active service, so we recommend not to define `DD_SERVICE`, `AWS_XRAY_TRACING_NAME`, or `OTEL_SERVICE_NAME`.

### Datadog

The [Datadog SDK](https://github.com/DataDog/dd-trace-go){: rel="nofollow"}'s only required environment variable is the `DD_AGENT_HOST` environment variable. There are a few other optional environment variables that can be set, such as `DD_ENV`, `DD_SERVICE`, `DD_TAGS`, etc. For a full list of available environment variables, see the [Datadog Go SDK documentation](https://docs.datadoghq.com/tracing/trace_collection/library_config/go/){: rel="nofollow"}.

### AWS X-Ray

For X-Ray, you need to provide the `AWS_XRAY_DAEMON_ADDRESS` variable. Optional variables include `AWS_XRAY_CONTEXT_MISSING`, `AWS_XRAY_TRACING_NAME`, etc. See the [AWS X-Ray Go SDK documentation](https://docs.aws.amazon.com/xray/latest/devguide/xray-sdk-go-configuration.html){: rel="nofollow"} for more details.

### OpenTelemetry

OpenTelemetry requires `OTEL_EXPORTER_OTLP_ENDPOINT` to point to the OpenTelemetry collector. Important: the Spacelift application is configured to use the GRPC protocol for communication with the agent so make sure it is enabled on the collector's side. Eg.:

```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
```

In this example, the `OTEL_EXPORTER_OTLP_ENDPOINT` should be set to something like `http://<collector-address>:4317`. Please note that even though the endpoint is GRPC, the `http://` prefix is still needed.

The rest of the configuration options can be found in the [OpenTelemetry SDK documentation](https://opentelemetry.io/docs/languages/sdk-configuration/){: rel="nofollow"}.
