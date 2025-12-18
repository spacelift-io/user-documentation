---
description: Telemetry configuration guides for Spacelift in Kubernetes.
---

# Telemetry in Kubernetes

These guides cover configuring telemetry collection for Spacelift installations running in Kubernetes. Telemetry helps you monitor service performance, trace requests across components, and troubleshoot issues in your Spacelift deployment.

## Available guides

Choose the telemetry backend that best fits your observability stack:

- **[Datadog Telemetry in Kubernetes](./k8s-datadog.md)** - Configure the Datadog agent to collect traces and metrics from Spacelift services. Ideal if you're already using Datadog for observability.

- **[OpenTelemetry with Grafana Stack in Kubernetes](./k8s-otel-grafana-stack.md)** - Set up OpenTelemetry Collector with Grafana Tempo and Grafana UI for an open-source tracing solution. This guide provides a complete end-to-end setup including storage and visualization.

- **[OpenTelemetry with Jaeger in Kubernetes](./k8s-otel-jaeger.md)** - Set up OpenTelemetry Collector with Jaeger for distributed tracing. Jaeger combines storage and UI in a single platform, making it simpler to deploy than separate components.

## Reference documentation

For detailed information about telemetry configuration options, supported backends, and environment variables, see the [telemetry reference documentation](../../reference/telemetry.md).
