# Spacelift Configuration Operator

!!! warning
    The Spacelift Kubernetes Operator support is currently limited. Resources removed from the cluster are not removed in Spacelift.

Spacelift Kubernetes Operator is an open-source ([`spacelift-operator`](https://github.com/spacelift-io/spacelift-operator){: rel="nofollow"}) [Kubernetes operator](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/){: rel="nofollow"} that allows you to manage Spacelift resources using Kubernetes [Custom Resource](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/){: rel="nofollow"} (CR).

!!! quote "Definition"
    A custom resource is an extension of the Kubernetes API that is not necessarily available in a default Kubernetes installation. It represents a customization of a particular Kubernetes installation. However, many core Kubernetes functions are now built using custom resources, making Kubernetes more modular.

## Kubernetes version compatibility

The spacelift controller is compatible with Kubernetes version v1.26+. The controller may also work with older versions, but we do not guarantee and provide support for unmaintained Kubernetes versions.

## Installation

### Install the CRD and the operator

```bash
kubectl apply -f https://downloads.spacelift.io/spacelift-operator/latest/manifests.yaml
```

!!! hint
    You can also download the manifest file, inspect it first, and then apply it using `kubectl apply -f <path-to-manifest-file>`.

This command will install the [Custom Resource Definition](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/){: rel="nofollow"} (CRD) and the operator itself.

### Create a secret with your Spacelift API key

You need to create an [Opaque secret](https://kubernetes.io/docs/concepts/configuration/secret/#opaque-secrets){: rel="nofollow"} with your [Spacelift API key](../api.md#spacelift-api-key-token) so the operator can authenticate with the Spacelift API. The secret's name has to be `spacelift-credentials` and it requires 3 keys:

- `SPACELIFT_API_KEY_ENDPOINT` - the URL of your Spacelift instance (e.g. `https://mycorp.app.spacelift.io`),
- `SPACELIFT_API_KEY_ID` - the ID of your API key,
- `SPACELIFT_API_KEY_SECRET` - the secret of your API key.

Here's an example of how to create the secret using the CLI:

```bash
kubectl create secret generic spacelift-credentials --from-literal=SPACELIFT_API_KEY_ENDPOINT='https://mycorp.app.spacelift.io' --from-literal=SPACELIFT_API_KEY_ID='<your-api-key-id>' --from-literal=SPACELIFT_API_KEY_SECRET='<your-api-key-secret>'
```

That's it! Now you can try it out by creating a test [Space](../../concepts/spaces/README.md).

### Create a test Space

```bash
kubectl apply -f - <<EOF
apiVersion: app.spacelift.io/v1beta1
kind: Space
metadata:
  name: space-test
spec:
  parentSpace: root
EOF
```

This command will create a new Space in your Spacelift instance. You can check if it was created successfully in the UI. Use this command to delete the Space:

```bash
kubectl delete space space-test
```

⚠️ **Note**: The operator currently does not delete the Space when the CR is deleted. You'll need to manually delete the Space in Spacelift.

## Usage

### Available resources

The operator currently supports the following resources:

- [Space](../../concepts/spaces/README.md)
- [Context](../../concepts/configuration/context.md)
- [Stack](../../concepts/stack/README.md)
- [Run](../../concepts/run/README.md)
- [Policy](../../concepts/policy/README.md)

### Available fields

The fields that you can use are available in the manifest file, or you can check out the definitions in the GitHub repository:

- [CRDs](https://github.com/spacelift-io/spacelift-operator/tree/main/config/crd/bases){: rel="nofollow"}
- [Go entities](https://github.com/spacelift-io/spacelift-operator/tree/main/api/v1beta1){: rel="nofollow"}

## Troubleshooting

### Debugging

The operator is built with [kubebuilder](https://book.kubebuilder.io/){: rel="nofollow"} and uses [zap](https://github.com/uber-go/zap){: rel="nofollow"} for logging. The default loglevel is `info`. You can change this by editing the manifest file (look for the `public.ecr.aws/spacelift-io/spacelift-operator` container) and adding an argument to the argument list:

```yaml
args:
  - "<existing-arguments>"
  - "--zap-log-level=debug"
```

Valid levels are: `debug`, `info` and `error`.

### Common issues

#### Resource does not appear in Spacelift

First of all, check the logs of the operator (perhaps you need [debug level](#debugging) logging?). Most often the issue is that Spacelift has rejected the request. The logs should contain the error message from Spacelift.
