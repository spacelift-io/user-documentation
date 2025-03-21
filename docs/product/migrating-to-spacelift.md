# Migrating to Spacelift

Migrating from one Infrastructure as Code CI/CD provider to another can feel daunting. This is why we created a [migration kit](https://github.com/spacelift-io/spacelift-migration-kit){: rel="nofollow"} that takes care of the heavy lifting.

Edit a few settings, and let it do the hard work. Then review, and possibly tweak, the generated code, and finally have your Spacelift entities created.

There is no one-size-fits-all for this kind of migration. This is why we designed this tool to be flexible and easy to hack to meet your specific needs. Feel free to reach out to our [support team](./support/README.md) if you need any help or guidance.

## Overview

The migration process is as follows:

- Export the definition for your resources at your current vendor.
- Generate the Terraform code to recreate similar resources at Spacelift using the [Terraform provider](https://registry.terraform.io/providers/spacelift-io/spacelift/latest/docs){: rel="nofollow"}.
- Review and possibly edit the generated Terraform code.
- Commit the Terraform code to a repository.
- Create a manager Spacelift stack that points to the repository with the Terraform code.

!!! tip
    Currently, only Terraform Cloud and Terraform Enterprise are supported as sources. The instructions below apply to both.

## Prerequisites

- [Python](https://www.python.org/downloads/) 3.13.1 or newer
- [Poetry](https://python-poetry.org/) 2.0.1 or newer

## Installation

- Ensure that Python is installed.
- Download the Migration Kit: `git clone git@github.com:spacelift-io/spacelift-migration-kit.git` (or other available
  methods in GitHub).
- Go to the Migration Kit folder: `spacelift-migration-kit`.
- Install the Python dependencies and the `spacemk` command in a Python virtual environment: `poetry install`.
- Activate the Python virtual environment: `$(poetry env activate)`.

## Usage

### Configuration

Copy the `config.yml.example` file to `config.yml` and edit it as needed.

Environment variables can be referenced by their name preceded by the `$` sign (e.g., `$API_TOKEN`).
This is helpful if you do not want to store sensitive information in the configuration file.

If a `.env` file is present at the root of the Spacelift Migration Kit folder, it will be automatically loaded when running `spacemk` and the tests, and the environment variables it contains will be available to that process.

### Audit

This step is optional but recommended. It will analyze your current setup and display statistics in the terminal. Also, an Excel file with the list of entities to be migrated is created (`tmp/report.xlsx`).

Additionally, it will perform checks and warn you of possible problems. For example, entities cannot be
automatically migrated and might need to be handled manually.

### Migration

The migration is split into a few different steps that need to be run in order.

#### Export

The `spacemk export` command exports information about the source provider entities and stores them as a normalized JSON file (`tmp/data.json`).

That file can be reviewed and modified before moving to the next step.

#### Generate

The `spacemk generate` command uses the normalized JSON file from the export step and uses a [Jinja template](https://jinja.palletsprojects.com/) to generate Terraform code that uses the [Spacelift provider](https://registry.terraform.io/providers/spacelift-io/spacelift/latest/docs) to create Spacelift entities that mimic the behavior of the source provider entities.

The generated code can be found in the `tmp/code/main.tf` file. Feel free to review and edit it as needed.

#### Publish

Once the Terraform code has been generated, push the `tmp/code/main.tf` file to a git repository of your choosing that is available to your Spacelift account.

#### Deploy

After pushing the generated Terraform has been pushed to a git repository, create a manager stack in Spacelift.

Point it to the repository, and possibly folder, where you stored the Terraform code, and make sure to **mark it as administrative**.

Finally, trigger a run to create the Spacelift entities.

#### Set Sensitive Variable Values

This step can be skipped if there are no sensitive variables defined.

To avoid storing sensitive variable values in Terraform code and the state file, the `generate` command does not set the value for those variables.

Once the stacks have been created, set the values for the `spacelift` section of the `config.yml` file and run the
`spacemk set-sensitive-env-vars` command to set the value for the sensitive environment variables.

#### Set Terraform Variables with Invalid Names

This step can be skipped if there are no Terraform variables with an invalid name.

Among [the different ways to pass variable values to Terraform](https://developer.hashicorp.com/terraform/language/values/variables#using-input-variable-values), Spacelift uses environment variables named `TF_VAR_` followed by the name of a declared variable.

However, Terraform allows the use of characters in variable names that are not allowed in environment variable names (e.g., `-`).

To work around this issue, the Spacelift Migration Kit identifies Terraform variables with invalid names and stores them in a mounted file named `tf_vars_with_invalid_name.auto.tfvars` so that it gets automatically loaded by Terraform.

Once the stacks have been created, set the values for the `spacelift` section of the `config.yml` file and run the
`spacemk set-tf-vars-with-invalid-name` command to set the values for the Terraform variables with invalid names.

#### Import State

This step will connect spacelift to TFC/TFE and import the state of the stacks created by the migration.
To do this, simply run the command `spacemk import-state-files-to-spacelift`.
This will create a context in spacelift with your TFC/TFE credentials, attach it to your newly created stacks and start a task to import the state from TFC directly.
It does _not_ use the state on disk (in the `tmp` directory) but rather fetches the state from TFC directly.

When doing this step, we authenticate to both TFC/TFE _and_ Spacelift. This means that you need to have the necessary credentials for both providers in your `config.yml` file.

#### Create Module Versions

This step can be skipped if there are no modules defined.

Once the modules have been created, set the values for the `github` section of the `config.yml` file and run the
`spacemk create-module-versions` command to re-create existing module versions.

### Cleanup

All temporary local artifacts are stored in the `tmp` folder. Delete some or all of it to clean up.

Additionally, you can destroy the Spacelift resources created by the manager stack and then the manager stack to fully remove the migration artifacts.

**The source vendor setup is left untouched by the Migration Kit** and can be deleted once the migration
has been verified to be successful.

## Customization

Every migration is different, and while the Spacelift Migration Kit aims at doing most of the heavy lifting, there is often a need for customizing the workflow.

Spacelift Migration Kit has been designed to be easily extended and modified. All customizations are stored in the `custom` folder.

### Custom Template

The `generate` command uses a [Jinja template](https://jinja.palletsprojects.com/) that can be overridden partially or entirely by creating a file named `main.tf.jinja` in the `custom/templates` folder.

To selectively override pieces of the base template, add the following instruction at the top of the custom template:

```jinja2
{% raw %}
{% extends "base.tf.jinja" %}
{% endraw %}
```

Then, override any block by declaring it in the custom template.

Here is an example:

```jinja2
{% raw %}
{% extends "base.tf.jinja" %}

{% block stacks %}
…
custom code to generate the Terraform code to define the Spacelift stacks
…
{% endblock %}
{% endraw %}
```

Available blocks can be found in the [base.tf.jinja](https://github.com/spacelift-io/spacelift-migration-kit/blob/main/spacemk/templates/base.tf.jinja) template.

It should be rarely needed, but if you can override the base template entirely by not including the `{% raw %}{% extends "base.tf.jinja" %}{% endraw %}` instruction.

### Custom Command

You can add a custom command by creating a Python file in the `custom/commands` folder based on the following code:

```python
import click

@click.command(help="Custom command.")
def custom():
    print("This is a custom command")

```

The file can have any name, but we recommend naming it after the command name. In the example above, the file would be `custom.py`.

If the custom command needs some configuration settings, they can be added to the `config.yml` file, and the configuration passed to the command:

```python
import click

@click.command(help="Custom command.")
@click.decorators.pass_meta_key("config")
def custom(config):
    print(f"This is a custom command with a custom setting {config.get('custom.foo', 'bar')}")
```

The commands are managed by the [click](https://click.palletsprojects.com/) Python library. Check its documentation or the Spacelift Migration Kit native commands for examples.

### Custom Exporter

There might be no native exporter for your source provider, or you might need to tweak an existing provider.

To do so, you can create a Python file in the `custom/exporters` folder. It must be named after the exporter and define a class named `<CapitalizedExporterName>Exporter` that derives from the `spacemk.exporters.BaseExporter` class for new exporters or a [native exporter class](https://github.com/spacelift-io/spacelift-migration-kit/tree/main/spacemk/exporters) when overriding an existing exporter.

Here are a few examples:

| Exporter Name | Filename     | Class Name       |
| ------------- | ------------ | ---------------- |
| `foo`         | `foo.py`     | `FooExporter`    |
| `foo_bar`     | `foo_bar.py` | `FooBarExporter` |

Here is an example:

```python
from spacemk.exporters import BaseExporter

class CustomExporter(BaseExporter):
    def _extract_data(self) -> list[dict]:
        data = []

        …
        custom code to extract data
        …

        return data

    def _map_data(self, src_data: dict) -> dict:
        data = []

        …
        custom code to map data source data to Spacelift normalized data definitions
        …

        return data
```

### Custom Python Packages

If the custom Python code requires packages not included in Spacelift Migration Kit, you can create a `requirements.txt` file in the `custom` folder and install those dependencies with the following command:

```shell
pip install -r custom/requirements.txt
```

### Storing Customizations

#### Simple Use Case

Customizations live in the `custom` folder. This is fine for most use cases but could be a problem if more than one engineer works on the migration or if you need to collaborate with Spacelift engineers on advanced migrations.

#### Advanced Use Case

For those advanced use cases, the proposed approach is to create a private clone of this repository and version your customizations there.

Here are the steps to create the private clone:

<!-- markdownlint-disable MD029 -->

1. Create a bare clone of the repository. This is temporary and will be removed, so just do it wherever.

```shell
git clone --bare git@github.com:spacelift-io/spacelift-migration-kit.git
```

2. Create a new private repository in your VCS provider and name it `spacelift-migration-kit`.

3. Mirror-push your bare clone to your new `spacelift-migration-kit` repository.

   ```shell
   cd spacelift-migration-kit.git
   git push --mirror git@github.com:<ACCOUNT NAME>/spacelift-migration-kit.git
   ```

4. Remove the temporary local clone you created in step 1.

```shell
cd ..
rm -rf spacelift-migration-kit.git
```

5. You can now clone your `spacelift-migration-kit` repository on your machine where you see fit.

```shell
git clone git@github.com:<ACCOUNT NAME>/spacelift-migration-kit.git
```

6. Add the original `spacelift-migration-kit` repository as `upstream` to fetch updates. The example below uses GitHub but you can use any git VCS provider information.

```shell
git remote add upstream git@github.com:spacelift-io/spacelift-migration-kit.git
git remote set-url --push upstream DISABLE
```

7. The git remotes for your local clone, listed with `git remote -v` should look like this:

```shell
origin git@github.com:<ACCOUNT NAME>/spacelift-migration-kit.git (fetch)
origin git@github.com:<ACCOUNT NAME>/spacelift-migration-kit.git (push)
upstream git@github.com:spacelift-io/spacelift-migration-kit.git (fetch)
upstream DISABLE (push)
```

8. Interact with your `origin` remote as usual. You can pull changes from the original repository by fetching from the `upstream` remote and rebasing on top of your local branch.
<!-- markdownlint-enable MD029 -->

```shell
git fetch upstream
git rebase upstream/main
```

There should not be any conflicts if you keep your modifications in the `custom` folder, but if there are, solve them as usual.

## Using NonVCS Workspaces

Spacelift requires a VCS provider to create a stack. However, you can migrate a non-VCS (cli driven) workspace to spacelift using the `spacemk update-vcs-config` command.
This command will read a CSV that tells spacemk "this workspace is a non-VCS workspace and in spacelift should point at this repository".

Before using the `generate` command, you need to create the csv that will tie workspaces to repositories in git. In the migration kit repo, there is a `vcs_config.csv` file that you can use as a template.
Fill this CSV out for all non-vcs repositories and then run `spacemk update-vcs-config` to update the stack configurations. Once this is complete, you can run the `generate` command as usual and you will see that the stacks are now pointing to the provided repository.

### vcs_config.csv

The VCS Config CSV file must include the following headers:

- `WorkspaceName` is the name of the workspace in your source TACOS provider.
- `ProjectRoot` is the path to the project root your workspace should use.
- `Branch` is the branch that the workspace should use.
- `Namespace` is, generally, the organization or user that owns the repository. For example, if im using a repository in the spacelift-io GitHub organization, the namespace would be `spacelift-io`.
- `RepoName` is the name of the repository.
- `VCSProvider` is one of `gitlab`, `bitbucket` or `github_enterprise` depending on the provider you are using. Can also be unset if using the default VCS integration.

## Uninstallation

- Delete the Python virtual environment: `poetry env remove --all`.
- Delete the `spacelift-migration-kit` folder.

## Support

If you found a bug or want to submit a feature request, please use the repository issues.

If you need help or guidance, please reach out to your Solutions Engineer or our [support](https://docs.spacelift.io/product/support/).
