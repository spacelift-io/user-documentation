# Kustomize

Kubernetes support in Spacelift is driven by Kustomize with native support in `kubectl`.

We used Kustomize to make all resources created using the Spacelift Kubernetes support have unique labels attached to them:

- `spacelift-stack: <stack-slug>`
- `app.kubernetes.io/managed-by: spacelift`

All operations Spacelift does will be done only on resources with the `spacelift-stack: <stack-slug>`.

If you are not using Kustomize, Spacelift will transparently create a `kustomization.yaml` file that will reference all yaml files in the Stack's project root and subdirectories.

If you are using Kustomize, then we will only add a label transformer to your kustomization.yaml file.
