# Docker

Every job in Spacelift is processed inside a fresh, isolated Docker container. This approach provides reasonable isolation and resource allocation and - let's face it - is a [pretty standard approach these days](https://circleci.com/docker/){: rel="nofollow"}.

## Standard runner image

By default, Spacelift uses the latest version of the[`public.ecr.aws/spacelift/runner-terraform`](https://gallery.ecr.aws/spacelift/runner-terraform){: rel="nofollow"} image, a simple Alpine image with a small bunch of universally useful packages. Feel free to refer to the [Dockerfile](https://github.com/spacelift-io/runner-terraform/blob/main/Dockerfile){: rel="nofollow"} that builds this image.

!!! info
    Given that we use Continuous Deployment on our backend and Terraform provider, we **explicitly don't want to version** the runner image. Feature previews are available under a `future` tag, but we'd advise against using these as the API might change unexpectedly.

### Standard runner image flavors

- `runner-terraform:latest` (default) - includes `aws` CLI
- `runner-terraform:gcp-latest` - includes `gcloud` CLI
- `runner-terraform:azure-latest` - includes `az` CLI

!!! note
    The reason we have separate images for cloud providers is that the `gcloud` and `az` CLIs are enormous and we don't want to bloat the default image with them.

## Allowed registries on public worker pools

On public worker pools, only Docker images from the following registries are allowed to be used for runner images:

- azurecr.io (Azure Container Registry)
- dkr.ecr.<region\>.amazonaws.com (All regions are supported)
- docker.io
- docker.pkg.dev
- gcr.io (Google Cloud Container Registry)
- ghcr.io (GitHub Container Registry)
- public.ecr.aws
- quay.io
<!-- markdownlint-disable-next-line MD044 -->
- registry.gitlab.com
- registry.hub.docker.com

## Customizing the runner image

The best way to customizing your Terraform execution environment is to build a custom runner image and use [runtime configuration](../concepts/configuration/runtime-configuration/README.md#runner_image-setting) to tell Spacelift to use it instead of the standard runner. If you're not using [Spacelift provider](../vendors/terraform/terraform-provider.md) with Terraform 0.12, you can use any image supporting (by far the most popular) AMD64 architecture and add your dependencies to it.

If you want our tooling in your image, there are two possible approaches. The first approach is to **build on top of our image**. We'd suggest doing that only if your customizations are relatively simple. For example, let's add a custom CircleCI provider to your image. They have a releases page allowing you to just `curl` the right version of the binary and put it in the `/bin` directory:

```docker title="Dockerfile"
FROM public.ecr.aws/spacelift/runner-terraform:latest

WORKDIR /tmp
RUN curl -O -L https://github.com/mrolla/terraform-provider-circleci/releases/download/v0.3.0/terraform-provider-circleci-linux-amd64 \
  && mv terraform-provider-circleci-linux-amd64 /bin/terraform-provider-circleci \
  && chmod +x /bin/terraform-provider-circleci
```

For more sophisticated use cases it may be cleaner to **use Docker's** [**multistage build feature**](https://docs.docker.com/develop/develop-images/multistage-build/){: rel="nofollow"} to build your image and add our tooling on top of it. As an example, here's the case of us building a Terraform [sops](https://github.com/mozilla/sops){: rel="nofollow"} [provider](https://github.com/carlpett/terraform-provider-sops){: rel="nofollow"} from source using a particular version. We want to keep our image small so we'll use a separate builder stage.

The following approach works for Terraform version 0.12 and below, where custom Terraform providers colocated with the Terraform binary are automatically used.

```docker
FROM public.ecr.aws/spacelift/runner-terraform:latest as spacelift
FROM golang:1.13-alpine as builder

WORKDIR /tmp

# Note how we don't bother building the provider statically because
# we're using Alpine for our final runner image, too.
RUN git clone https://github.com/carlpett/terraform-provider-sops.git \
  && cd terraform-provider-sops \
  && git checkout c5ffe6ebfac0a56fd60d5e7d77e0f2a73c34c3b7 \
  && go build -o /terraform-provider-sops

FROM alpine:3.10
COPY --from=spacelift /bin/terraform-provider-spacelift /bin/terraform-provider-spacelift
COPY --from=builder /terraform-provider-sops /bin/terraform-provider-sops

RUN adduser --disabled-password --no-create-home --uid=1983 spacelift
```

!!! info
    Note the `adduser` bit. **Spacelift runs its Docker workflows as user `spacelift` with UID 1983**, so make sure that:

    * this user exists and has the right UID, otherwise you won't have access to your files;
    * whatever you need accessed and executed in your custom image has the right ownership and/or permissions;

    Depending on your image flavor, the exact command to add the user may be different.

!!! tip
    Any `ENTRYPOINT` and `CMD` customization will be ignored because the Spacelift worker binary must be the root process in the container.

    If you need to customize the shell (e.g., dynamically set environment variables or export functions), you can do so in a [`before_init` hook](../concepts/stack/stack-settings.md#customizing-workflow).

### Custom providers from Terraform 0.13 onwards

Since Terraform 0.13, custom providers require a slightly different approach. You will build them the same way as described above, but the path now will be different. In order to work with the new API, we require that you put the provider binaries in the `/plugins` directory and maintain a particular naming scheme. The above `sops` provider example will work with Terraform 0.13 if the following stanza is added to the `Dockerfile`.

```docker
COPY --from=builder /terraform-provider-sops /plugins/registry.myorg.io/myorg/sops/1.0.0/linux_amd64/terraform-provider-sops
```

In addition, the custom provider must be explicitly required in the Terraform code, like this:

```terraform
terraform {
  required_providers {
    spacelift = {
      source = "registry.myorg.io/myorg/sops"
    }
  }
}
```

Note that the source as defined above and the plugin path as defined in the Dockerfile are entirely arbitrary but **must match**. You can read more in the [official Terraform 0.13 upgrade documentation](https://www.terraform.io/upgrade-guides/0-13.html#in-house-providers){: rel="nofollow"}.

## Using private Docker images

If you're using Spacelift's default public [worker pool](../concepts/worker-pools.md), you're required to use public images. This is by design - if we allowed using private images, they would be cached by the Docker daemon and accessible to all customers using the same shared worker.

Hence, only private workers support private Docker images. To enable private image support, first, execute `docker login` command with the proper registry credentials. Spacelift agent will read the credentials from Docker's configuration directory, but you will need to point it to the correct location by setting the `SPACELIFT_DOCKER_CONFIG_DIR` environment variable.

### Special case: ECR

ECR is a special case because those credentials tend to expire pretty quickly, and you'd need to add a mechanism to refresh them periodically if you wanted to maintain live access to the registry (cached images would not be affected by expired credentials). Given that many of our customers use EC2 to host their worker pools, we implemented a special mechanism to support private images hosted in ECR.

This access is seamless - if the launcher detects that a runner image is hosted in ECR, it tries to use the existing credentials (e. g. EC2 instance role credentials) to generate the registry access token automatically on each job execution. With ECR images you don't even need to execute `docker login`.

## Best practices

Here's a bunch of things we consider essential to keep your Docker usage relatively safe.

### If unsure, build from source

Building from the source is generally safer than using a pre-built binary, especially if you can review the code beforehand and make sure you're always building the code you've reviewed. You can use a Git commit hash, like we did above.

### Use well-known bases

If you're building an image from a source other than [`public.ecr.aws/spacelift/runner-terraform`](https://gallery.ecr.aws/spacelift/runner-terraform){: rel="nofollow"}, please prefer well-known and well-supported base images. Official images are generally safe, so choose something like `golang:1.13-alpine` over things like `imtotallylegit/notascamipromise:best-golang-image`. There's a bunch of services out there offering Docker image vulnerability scanning, so that's an option as well.

### Limit push access

Your stack is only as safe as the runner image you're using for it. A malicious actor is able to doctor your runner image in a way that will allow them to take over your stack and all its associated cloud provider accounts in a snap. Please always review the code, and only allow `docker push` access to your most trusted associates.

!!! info
    In our default public worker pool, **we only support publicly available Docker images**. If you need private Docker images, you can log in to any Docker registry from a worker in a [private worker pool](../concepts/worker-pools.md).
