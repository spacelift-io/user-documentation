# External modules

Those of our customers who are not yet using our private module registry may want to pull modules from various external sources supported by Terraform. This article discusses a few most popular types of module sources and how to use them in Spacelift.

## Cloud storage

The easiest ones to handle are cloud sources - [S3](https://www.terraform.io/docs/language/modules/sources.html#s3-bucket) and [GCS](https://www.terraform.io/docs/language/modules/sources.html#gcs-bucket) buckets. Access to these can be granted using our [AWS](../../integrations/cloud-providers/aws.md) and [GCP](../../integrations/cloud-providers/gcp.md) integrations - or - if you're using [private Spacelift workers](../../concepts/worker-pools.md) hosted on either of these clouds, you may not require any authentication at all!

## Git repositories

Git is by far the most popular external module source. This example will focus on [GitHub](https://www.terraform.io/docs/language/modules/sources.html#github) as the most popular one, but the advice applies to other VCS providers. In general, Terraform retrieves Git-based modules using one of the two supported transports - HTTPS or SSL. Assuming your repository is private, you will need to give Spacelift credentials required to access it.

### Using HTTPS

Git with HTTPS is slightly simpler than SSH - all you need is a personal access token, and you need to make sure that it ends up in the `~/.netrc` file, which Terraform will use to log in to the host that stores your source code.

Assuming you already have a token you can use, create a file like this:

```bash
machine github.com
login $yourLogin
password $yourToken
```

Then, upload this file to your stack's Spacelift environment as a [mounted file](../../concepts/configuration/environment.md#mounted-files). In this example, we called that file `github.netrc`:

![](<../../assets/screenshots/Mouse_Highlight_Overlay (4).png>)

Add the following commands as ["before init" hooks](../../concepts/stack/stack-settings.md#customizing-workflow) to append the content of this file to the `~/.netrc` proper:

```bash
cat /mnt/workspace/github.netrc >> ~/.netrc
chmod 600 ~/.netrc
```

### Using SSH

Using SSH isn't much more complex, but it requires a bit more preparation. Once you have a public-private key pair (whether it's a [personal](https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account) SSH key or a single-repo [deploy key](https://docs.github.com/en/developers/overview/managing-deploy-keys#deploy-keys)), you will need to pass it to Spacelift and make sure it's used to access your VCS provider. Once again, we're going to use the [mounted file](../../concepts/configuration/environment.md#mounted-files) functionality to pass the _private_ key called `id_ed25519` to your stack's environment:

![](<../../assets/screenshots/Mouse_Highlight_Overlay (5).png>)

Add the following commands as ["before init" hooks](../../concepts/stack/stack-settings.md#before-init-scripts) to "teach" our SSH agent to use this key for GitHub:

```bash
mkdir -p ~/.ssh
cp /mnt/workspace/id_ed25519 ~/.ssh/id_ed25519
chmod 400 ~/.ssh/id_ed25519
ssh-keyscan -t rsa github.com >> ~/.ssh/known_hosts
```

The above example warrants a little explanation. First, we're making sure that the `~/.ssh` directory exists - otherwise, we won't be able to put anything in there. Then we copy the private key file mounted in our workspace to the SSH configuration directory and give it proper permissions. Last but not least, we're using the `ssh-keyscan` utility to retrieve the public SSH host key for github.com and add it to the list of known hosts - this will avoid your code checkout failing due to what would otherwise be an interactive prompt asking you whether to trust that key.

## Dedicated third-party registries

For users storing their modules in dedicated external private registries, like [Terraform Cloud's one](https://www.terraform.io/docs/cloud/registry/index.html), you will need to supply credentials in the `.terraformrc` file - this approach is documented in the [official documentation](https://www.terraform.io/docs/cli/config/config-file.html#credentials).

In order to faciliate that, we've introduced a special mechanism for extending the CLI configuration that does not even require using before\_init hooks. You can read more about it [here](cli-configuration.md).

## To mount or not to mount?

That is the question. And there isn't a single right answer. Instead, there is a list of questions to consider. By mounting a file, you're giving us access to its content. No, we're not going to read it, and yes, we have it encrypted using a fancy multi-layered mechanism, but still - we have it. So the main question is **how sensitive the credentials are**. Read-only deploy keys are probably the least sensitive - they only give read access to a single repository, so these are the ones where convenience may outweigh other concerns. On the other hand, personal access tokens may be pretty powerful, even if you generate them from service users. The same thing goes for personal SSH keys. Guard these well.

So if you don't want to mount these credentials, what are your options? First, you can put these credentials directly into your [private runner image](../../integrations/docker.md#using-private-docker-images). But that means that anyone in your organization who uses the private runner image gets access to your credentials - and that may or may not be what you wanted.

The other option is to store the credentials externally in one of the secrets stores - like [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/) or [HashiCorp Vault](https://www.vaultproject.io) and retrieve them in one of your [`before_init`](../../concepts/stack/stack-settings.md#before-init-scripts) scripts before putting them in the right place (`~/.netrc` file, `~/.ssh` directory, etc.).

!!! info
    If you decide to mount, we advise that you store credentials in [contexts](../../concepts/configuration/context.md) and attach these to stacks that need them. This way you can avoid credentials sprawl and leak.
