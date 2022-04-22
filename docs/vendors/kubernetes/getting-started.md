---
description: Creating your first Kubernetes Stack with Spacelift, step by step.
---

# Getting Started

## Repository Creation

Start by creating a new deployment repository and name the file as `deployment.yaml` with the following code:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  selector:
    matchLabels:
      app: nginx
  replicas: 2 # tells deployment to run 2 pods matching the template
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
        ports:
        - containerPort: 80
```

You can learn more about this example deployment by navigating to the [Run a Stateless Application Using a Deployment ](https://kubernetes.io/docs/tasks/run-application/run-stateless-application-deployment/)website from the official Kubernetes documentation.

Looking at the code, you will find that it deploys a single instance of Nginx.

## Create a new Stack

In Spacelift, go ahead and click the **Add Stack** button to create a Stack in Spacelift.

![](/assets/images/k8s-create-a-new-stack.png)

### Integrate VCS

Select the repository you created in the initial step, as seen in the picture.

![Configuring the VCS settings.](/assets/images/k8s-integrate-vcs.png)

### Configure Backend

Choose Kubernetes from the dropdown list and type out the **namespace**.

!!! Info
Spacelift does not recommend leaving the Namespace blank due to the elevated level of access privilege required.


![](/assets/images/k8s-configure-backend.png)

### Define Behavior

Select the arrow next to _Show Advanced Options_ to expose the advanced configuration options.\
\
To ensure the success of a Kubernetes deployment, the following options should be reviewed and validated.

* Runner Image: By Default, Spacelift will add the necessary binary to run `kubectl` if not found. Including runner images not provided by Spacelift.
* Customize workflow: During the initialization phase, you must specify the necessary command to ensure _kubeconfig_ is updated and authenticated to the Kubernetes Cluster you will be authenticating against.

!!! Info
Spacelift can authenticate against any Kubernetes cluster, including local or cloud provider managed instances.


![](/assets/images/k8s-define-behavior.png)

In the example above, I am authenticating to an AWS EKS Cluster and used the following command to update the kubeconfig for the necessary cluster.\
\
`aws eks update-kubeconfig --region $region-name --name $cluster-name`

!!! Info
`Update the previous variables according to your deployment.`\
``

* `$region-name:` AWS region where your Kubernetes cluster resides
* `$cluster-name:` Name of your Kubernetes clusters


The above allows the worker to authenticate to the proper cluster before running the specified Kubernetes deployment in the repository that we created earlier.

!!! Warning
Authentication with a Cloud Provider is _**required**_.\
\
After you Name the Stack, follow the Cloud Integrations section to ensure Spacelift can authenticate to your Kubernetes Cluster.


### Name the Stack

Provide the name of your Stack. _Labels_ and _Description_ are not required but recommended.

![](/assets/images/k8s-name-stack.png)

Saving the Stack will redirect you to its Tracked Runs (Deployment) page.

![](/assets/images/k8s-triggered-runs.png)

## Configure Integrations

To authenticate against a Kubernetes cluster provided by Cloud Provider managed service, Spacelift requires integration with the associated Cloud Provider.

Navigate to the **Settings**, **Integrations** page and select the dropdown arrow to access the following selection screen:

![](/assets/images/k8s-integration-selection.png)

!!! Warning
Necessary permissions to the Kubernetes Cluster are required.


The following links will help you set up the necessary integration with your Cloud Provider of choice.

* [AWS](../../integrations/cloud-providers/aws.md)
* [Azure](../../integrations/cloud-providers/azure.md)
* [GCP](../../integrations/cloud-providers/gcp.md)

Once you have configured the necessary integration, navigate the Stack landing page and Trigger a Run.

## Trigger a Run

To Trigger a Run, select _**Trigger**_ on the right side of the Stacks view.

![](/assets/images/k8s-trigger.png)

!!! Info
**Spacelift Label**\
****\
****To help identify resources deployed to your Kubernetes cluster, Spacelift will add the following label to all resources.\
\
`spacelift-stack=<stack-slug>`


### Triggered Run Status

Please review the [documentation](broken-reference) for a detailed view of each Run Phase and Status associated with Kubernetes.

#### Unconfirmed

After you manually trigger the Run in the Stack view, Spacelift will deploy a runner image, initialize the Cloud Provider, Authenticate with the Kubernetes Cluster and run the Deployment specified in the repository.\
\
After a successful planning phase, you can check the log to see the planned changes.

![](/assets/images/k8s-unconfirmed.png)

!!! Info
**Planning Phase**

Spacelift utilizes the dry run functionality of `kubectl apply to`compare your code to the current state of the cluster and output the list of changes to be made.\
``\
``A slightly different dry run mode depending on the scenario:

* `--dry-run=server:`Utilized when resources are available
* `--dry-run-client:`Utilized when <mark style="color:red;">**no**</mark> resources _****_ are available


To confirm the Triggered run, click the _**CONFIRM**_ button.

#### Finished Deployment

The following screen highlights the Finished Run and output from a successful deployment to your Kubernetes cluster.

![](/assets/images/k8s-finished.png)

!!! Info
**Applying**

The default timeout is set to 10 minutes. If a Kubernetes Deployment is expected to take longer, you can customize that using the KUBECTL\_ROLLOUT\_TIMEOUT environment variable.\
\
Review the [documentation](../../concepts/configuration/environment.md) to find out more about Spacelift environment variables..


### Default Removal of Deployments

!!! Info
By default; if a YAML file is removed from your repository, the resources with an attached `spacelift-stack=<stack-slug>`label will be removed from the Kubernetes cluster. \


The `--prune` flag will be utilized.




