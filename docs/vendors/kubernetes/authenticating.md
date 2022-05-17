# Authenticating

The Kubernetes integration relies on using `kubectl`'s native authentication to connect to your cluster. You can use the `$KUBECONFIG` environment variable to find the location of the Kubernetes configuration file, and configure any credentials required.

You should perform any custom authentication as part of a _before init_ hook to make sure that `kubectl` is configured correctly before any commands are run, as shown in the following example:

![](<../../assets/screenshots/image (110).png>)

The following sections provide examples of how to configure the integration manually, as well as using Cloud-specific tooling.

## Manual Configuration

Manual configuration allows you to connect to any Kubernetes cluster accessible by your Spacelift workers, regardless of whether your cluster is on-prem or hosted by a cloud provider. The Kubernetes integration automatically sets the `$KUBECONFIG` environment variable to point at `/mnt/workspace/.kube/config`, giving you a number of options:

- You can use a [mounted file](../../concepts/configuration/environment.md#mounted-files) to mount a pre-prepared config file into your workspace at `/mnt/workspace/.kube/config`.
- You can use a _before init_ hook to create a kubeconfig file, or to download it from a trusted location.

Please refer to the [Kubernetes documentation](https://kubernetes.io/docs/tasks/access-application-cluster/configure-access-multiple-clusters/) for more information on configuring kubectl.

## AWS

The simplest way to connect to an AWS EKS cluster is using the AWS CLI tool. To do this, add the following _before init_ hook to your Stack:

```bash
aws eks update-kubeconfig --region $REGION_NAME --name $CLUSTER_NAME
```

!!! info
    - The `$REGION_NAME` and `$CLUSTER_NAME` environment variables must be defined in your Stack's environment.
    - This relies on either using the Spacelift [AWS Integration](../../integrations/cloud-providers/aws.md), or ensuring that your workers have permission to access the EKS cluster.

## Azure

The simplest way to connect to an AKS cluster in Azure is using the [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/) to automatically add credentials to your kubeconfig. To do this your stack needs to use a custom runner image with the Azure CLI installed, and needs to run two _before init_ hooks:

- `az login` - logs into the Azure CLI.
- `az aks get-credentials` - adds credentials for your cluster to the kubeconfig file.

Depending on your exact use-case, you may need to use slightly different versions of the `az login` command. This guide outlines two main scenarios.

!!! info
    Please note that both examples assume that your stack has an `$AKS_CLUSTER_NAME` and `$AKS_RESOURCE_GROUP` environment variable configured containing the name of the AKS cluster and the resource group name of the cluster respectively.

### Using the Spacelift Azure Integration

When using our [Azure integration](../../integrations/cloud-providers/azure.md#spacelift-managed-integration), you can use the computed `$ARM_*` environment variables to login as the Service Principal for the integration:

```bash
az login --service-principal -u "$ARM_CLIENT_ID" -t "$ARM_TENANT_ID" -p "$ARM_CLIENT_SECRET"
az aks get-credentials --name "$AKS_CLUSTER_NAME" --resource-group "$AKS_RESOURCE_GROUP"
```

### Using private workers with Managed Identities

When using [private workers with a managed identity](../../integrations/cloud-providers/azure.md#managed-identities), you can use the identity of that worker to login:

```bash
az login --identity
az aks get-credentials --name "$AKS_CLUSTER_NAME" --resource-group "$AKS_RESOURCE_GROUP"
```

## GCP

You can use the gcloud CLI to authenticate with a GKE cluster when using the [Spacelift GCP integration](../../integrations/cloud-providers/gcp.md) using the `gcloud container clusters get-credentials` command. For this to work, you need to use a custom runner image that has the [gcloud CLI](https://cloud.google.com/sdk/gcloud) and [kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl) installed.

The Spacelift GCP integration automatically generates an access token for your GCP service account, and this token can be used for getting your cluster credentials as well as accessing the cluster. To do this, add the following _before init_ hooks to your Stack:

```bash
# Output the token into a temporary file, use gcloud to get
# the cluster credentials, then remove the tmp file
echo "$GOOGLE_OAUTH_ACCESS_TOKEN" > /mnt/workspace/gcloud-access-token
gcloud container clusters get-credentials $GKE_CLUSTER_NAME \
  --region $GKE_CLUSTER_REGION \
  --project $GCP_PROJECT_NAME \
  --access-token-file /mnt/workspace/gcloud-access-token
rm /mnt/workspace/gcloud-access-token

# Remove and re-create the user, using the automatically generated access token
kubectl config delete-user $(kubectl config current-context)
kubectl config set-credentials $(kubectl config current-context) --token=$GOOGLE_OAUTH_ACCESS_TOKEN
```

Please note, your Stack needs to have the following environment variables set for this script to work:

- `GKE_CLUSTER_NAME` - the name of your cluster.
- `GKE_CLUSTER_REGION` - the region the cluster is deployed to.
- `GCP_PROJECT_NAME` - the name of your GCP project.

!!! info
    The `get-credentials` command configures your _kubeconfig_ file to use the `gcloud config config-helper` command to allow token refresh. Unfortunately this command will not work when we only have an access token available. The script provided works around this by manually removing and re-creating the user details in the config file.

### Single Zone Deployment

If your cluster is deployed to a single zone, you can use the `--zone` flag instead of the `--region` flag in the `gcloud container clusters get-credentials` command:

```bash
gcloud container clusters get-credentials $GKE_CLUSTER_NAME \
  --zone $GKE_CLUSTER_ZONE \
  --project $GCP_PROJECT_NAME \
  --access-token-file /mnt/workspace/gcloud-access-token
```
