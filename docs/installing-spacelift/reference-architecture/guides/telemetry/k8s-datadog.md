---
description: Configuring Datadog telemetry for Spacelift running in Kubernetes.
---

# Datadog Telemetry in Kubernetes

This guide provides a way to configure Datadog telemetry for your Spacelift installation running in Kubernetes. By deploying the Datadog agent in your cluster, you can collect traces and metrics from Spacelift services to monitor performance and troubleshoot issues.

Spacelift backend services emit telemetry data that can be collected by the Datadog agent. Once configured, you'll be able to visualize service performance, trace requests across components, and monitor application metrics in your Datadog dashboard.

## Prerequisites

Before proceeding with the installation, ensure you have:

- A running Spacelift installation in Kubernetes.
- A [Datadog account](https://www.datadoghq.com/){: rel="nofollow"} with an API key.
- [kubectl](https://kubernetes.io/docs/tasks/tools/){: rel="nofollow"} configured to access your cluster.
- [Helm 3 or later](https://helm.sh/docs/helm/helm_install/){: rel="nofollow"} installed.

!!! info
    For more information about telemetry configuration options and supported backends, see the [telemetry reference documentation](../../reference/telemetry.md).

## Install the Datadog agent

First, add the Datadog Helm repository and update it:

```shell
helm repo add datadog https://helm.datadoghq.com
helm repo update
```

Next, create a dedicated namespace for the Datadog agent:

```shell
kubectl create namespace datadog
```

Install the Datadog agent using Helm. Replace `<DATADOG_API_KEY>` with your actual Datadog API key and `<DATADOG_SITE>` with your Datadog site (e.g., `datadoghq.com` for US1, `datadoghq.eu` for EU, `us3.datadoghq.com` for US3, etc.):

```shell
helm install datadog-agent \
    --namespace datadog \
    --set datadog.apiKey=<DATADOG_API_KEY> \
    --set datadog.site=<DATADOG_SITE> \
    datadog/datadog
```

!!! tip
    It's recommended to add custom tags to help organize and filter your telemetry data. Here's an example with additional tags:

    ```shell
    helm install datadog-agent \
        --namespace datadog \
        --set datadog.apiKey=12356apikey789 \
        --set datadog.site=datadoghq.com \
        --set "datadog.tags[0]=app:spacelift" \
        --set "datadog.tags[1]=environment:production" \
        datadog/datadog
    ```

## Configure Spacelift

Once the Datadog agent is running, you need to configure Spacelift to send telemetry data to it.

### Update Spacelift configuration

The Spacelift services need two environment variables to enable Datadog telemetry:

- `OBSERVABILITY_VENDOR` - Set to `Datadog` to enable the Datadog telemetry backend.
- `DD_AGENT_HOST` - The fully qualified domain name of the Datadog agent service.

The `DD_AGENT_HOST` value follows the Kubernetes DNS format: `{service-name}.{namespace}.svc.cluster.local`. Based on the installation above, the value would be `datadog-agent.datadog.svc.cluster.local`.

Update the `spacelift-shared` secret with these variables:

```shell
kubectl patch secret spacelift-shared -n spacelift \
  --type=merge \
  -p '{"stringData":{"DD_AGENT_HOST":"datadog-agent.datadog.svc.cluster.local","OBSERVABILITY_VENDOR":"Datadog"}}'
```

!!! note
    If you used a different namespace or service name when installing the Datadog agent, make sure to adjust the `DD_AGENT_HOST` value accordingly.

### Restart Spacelift services

For the configuration changes to take effect, restart the Spacelift deployments:

```shell
kubectl rollout restart deployment -n spacelift \
  spacelift-drain \
  spacelift-scheduler \
  spacelift-server
```

### Verify the setup

Check the application logs to ensure there are no errors related to telemetry:

```shell
kubectl logs -n spacelift deployment/spacelift-server
```

If the configuration is correct, you should start seeing telemetry data appear in your Datadog dashboard within a few minutes.

## Maintenance

### Upgrading the Datadog agent

To upgrade the Datadog agent to a newer version, first check for available versions:

```shell
helm search repo datadog/datadog --versions
```

Then upgrade to the desired version:

```shell
helm upgrade datadog-agent \
    --namespace datadog \
    --set datadog.apiKey=<DATADOG_API_KEY> \
    --set datadog.site=<DATADOG_SITE> \
    --version <NEW_VERSION> \
    datadog/datadog
```

## Additional configuration

The [Datadog Go SDK](https://github.com/DataDog/dd-trace-go){: rel="nofollow"} supports additional environment variables for fine-tuning telemetry collection. You can set these in the `spacelift-shared` secret if needed:

- `DD_ENV` - The environment tag (e.g., `production`, `staging`).
- `DD_TAGS` - Additional tags in the format `key1:value1,key2:value2`.
- `DD_TRACE_SAMPLE_RATE` - Sample rate for trace collection (default: `1.0`).

For a complete list of available configuration options, see the [Datadog Go SDK documentation](https://docs.datadoghq.com/tracing/trace_collection/library_config/go/){: rel="nofollow"}.

!!! warning
    Spacelift automatically sets the service name based on the active service (`server`, `drain`, `scheduler`). We recommend _not_ setting the `DD_SERVICE` environment variable to avoid overriding this behavior.

## Cleanup and uninstallation

If you need to remove Datadog telemetry from your cluster, follow these steps to completely clean up all resources.

First, verify which releases are installed:

```shell
helm list --all-namespaces
```

Based on the output, uninstall the Datadog agent:

```shell
helm uninstall datadog-agent -n datadog
```

Finally, delete the datadog namespace to remove all remaining resources:

```shell
kubectl delete namespace datadog
```

### Disable Spacelift telemetry configuration

If you've already set up the telemetry configuration in Spacelift, at this point it should throw errors since the Datadog agent is no longer available. To fully disable telemetry in Spacelift, patch the `spacelift-shared` secret to clear the environment variables:

```shell
kubectl patch secret spacelift-shared -n spacelift \
  --type=merge \
  -p '{"stringData":{"DD_AGENT_HOST":"","OBSERVABILITY_VENDOR":"Disabled"}}'

kubectl rollout restart deployment -n spacelift \
  spacelift-drain \
  spacelift-scheduler \
  spacelift-server
```
