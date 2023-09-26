---
description: Exporting Spacelift data to Prometheus
---

# Prometheus integration

The Prometheus exporter allows you to monitor various metrics about your Spacelift account over time. You can then use tools like Grafana to visualize those changes and Alertmanager to take actions based on account metrics. Several metrics are available, and you can find the complete list of available metrics [here](https://github.com/spacelift-io/prometheus-exporter#available-metrics).

## How it works

The Prometheus exporter is an adaptor between Prometheus and the Spacelift GraphQL API. Whenever Prometheus asks for the current metrics, the exporter makes a GraphQL request and converts it into the metrics format Prometheus expects.

Read more on our blog: [Monitoring Your Spacelift Account via Prometheus](https://spacelift.io/blog/prometheus-exporter-for-spacelift).
