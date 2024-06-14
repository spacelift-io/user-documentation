# Spacelift Kubernetes Operator

Spacelift Kubernetes Operator is a [Kubernetes operator](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/){: rel="nofollow"} that allows you to manage Spacelift resources using Kubernetes [Custom Resource](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/){: rel="nofollow"} (CR).

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

You need to create an [Opaque secret](https://kubernetes.io/docs/concepts/configuration/secret/#opaque-secrets){: rel="nofollow"} with your [Spacelift API key](../api.md#spacelift-api-key--token) so the operator can authenticate with the Spacelift API. The secret's name has to be `spacelift-credentials` and it requires 3 keys:

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
  name: Test space created from Operator
  parentSpace: root
EOF
```

This command will create a new Space in your Spacelift instance. You can check if it was created successfully in the UI. Use this command to delete the Space:

```bash
kubectl delete space space-test
```

⚠️ **Note**: The operator currently does not delete the Space when the CR is deleted. You'll need to manually delete the Space in Spacelift.
