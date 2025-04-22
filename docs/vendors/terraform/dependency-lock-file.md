# Dependency Lock File

All versions of OpenTofu and more recent versions of Terraform can optionally track dependency selections using a [Dependency Lock File](https://opentofu.org/docs/language/files/dependency-lock/){: rel="nofollow"} named `.terraform.lock.hcl`, in a similar fashion to npm's `package-lock.json` file.

If this file is present in the [project root for your stack](../../concepts/stack/stack-settings.md#project-root), OpenTofu/Terraform will use it. Otherwise, it will dynamically determine the dependencies to use.

## Generating & Updating the File

OpenTofu and Terraform creators recommend including the Dependency Lock File in your version control repository, alongside your infrastructure code.

You can generate or update this file by running `tofu/terraform init` locally and committing it into your repository.

An alternative option would be to run the `tofu/terraform init` in a [Task](../../concepts/run/task.md), print it to the Task logs, copy/paste the content from the Task logs into the `.terraform.lock.hcl` file, and commit it into your repository.
