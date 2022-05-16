# Helm

There is no native support within Spacelift for Helm, but you can use the [`helm template`](https://helm.sh/docs/helm/helm_template/) command in a _before plan_ hook to generate the Kubernetes resource definitions to deploy.

Please note, the following caveats apply:

* Using `helm template` means that you are not using the full Helm workflow, which may cause limitations or prevent certain Charts from working.
* You need to use a custom [Spacelift worker image](../../integrations/docker.md#customizing-the-runner-image) that has Helm installed, or alternatively you can install Helm using a _before init_ hook.

The rest of this page will go through an example of deploying the [Spacelift Workerpool Helm Chart](https://github.com/spacelift-io/spacelift-workerpool-k8s) using the Kubernetes integration. See [here](https://github.com/spacelift-io/kubernetes-helm-example) for an example repository.

## Prerequisites

The following prerequisites are required to follow the rest of this guide:

* A Kubernetes cluster that you can authenticate to from a Spacelift stack.
* A namespace called `spacelift-worker` that exists within that cluster.

## Repository Creation

Start by creating a new repository for your Helm stack. This repository only needs to contain a single item - a _kustomization.yaml_ file:

```
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: spacelift-worker

resources:
  # spacelift-worker-pool.yaml will be generated in a pre-plan hook
  - spacelift-worker-pool.yaml
```

The kustomization file is used to tell `kubectl` where to find the file containing the output of the `helm template` command, and prevents `kubectl` from attempting to apply every yaml file in your repository. This is important if you want to commit a `values.yaml` file to your repository.

!!! info
    Our example repository contains a values.yaml file used to configure some of the chart values. This isn't required, and is simply there for illustrative purposes.

## Create a new Stack

### Define Behavior

Follow the same steps to create your stack as per the [Getting Started](getting-started.md#create-a-new-stack) guide, but when you get to the _Define Behavior_ step, add the following commands as _before plan_ hooks:

```
helm repo add spacelift https://downloads.spacelift.io/helm
helm template spacelift-worker-pool spacelift/spacelift-worker --values values.yaml --set "replicaCount=$SPACELIFT_WORKER_REPLICAS" --set "credentials.token=$SPACELIFT_WORKER_POOL_TOKEN" --set "credentials.privateKey=$SPACELIFT_WORKER_POOL_PRIVATE_KEY" > spacelift-worker-pool.yaml
```

Also, make sure to specify your custom _Runner image_ that has Helm installed if you are not installing Helm using a _before init_ hook.

Once you've completed both steps, you should see something like this:

![](<../../assets/screenshots/image (109).png>)

### Configure Environment

Once you have successfully created your Stack, add values for the following environment variables to your Stack environment:

* `SPACELIFT_WORKER_REPLICAS` - the number of worker pool replicas to create**.**
* `SPACELIFT_WORKER_POOL_TOKEN` - the token downloaded when creating your worker pool.
* `SPACELIFT_WORKER_POOL_PRIVATE_KEY` - your base64-encoded private key.

Your Stack environment should look something like this:

![](<../../assets/screenshots/image (117) (1).png>)

## Configure Integrations

Configure any required Cloud Provider integrations as per the [Getting Started](getting-started.md#configure-integrations) guide.

## Trigger a Run

This example assumes that a Kubernetes namespace called `spacelift-worker` already exists. If it doesn't, create it using `kubectl create namespace spacelift-worker` before triggering a run.

!!! info
    You can use a [Spacelift Task](../../concepts/run/task.md) to run the `kubectl create namespace` command.

Triggering runs works exactly the same as when not using Helm. Once the planning stage has completed, you should see a preview of your changes, showing the Chart resources that will be created:

![](<../../assets/screenshots/image (116) (1).png>)

After approving the run, you should see the changes applying, along with a successful rollout of your Chart resources:

![](<../../assets/screenshots/image (110) (1).png>)

