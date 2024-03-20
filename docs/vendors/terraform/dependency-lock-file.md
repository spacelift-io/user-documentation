# Dependency Lock File

Recent versions of Terraform can optionally track dependency selections using a [Dependency Lock File](https://www.terraform.io/language/files/dependency-lock){: rel="nofollow"} named `.terraform.lock.hcl`, in a similar fashion to npm's `package-lock.json` file.

If this file is present in the [project root for your stack](../../concepts/stack/stack-settings.md#project-root), Terraform will use it. Otherwise, it will dynamically determine the dependencies to use.

## Generating & Updating the File

Terraform recommends including the Dependency Lock File in your version control repository, alongside your infrastructure code.

You can generate or update this file by running `terraform init` locally and committing it into your repository.

An alternative option would be to run the `terraform init` in a [Task](../../concepts/run/task.md), print it to the Task logs, copy/paste the content from the Task logs into the `.terraform.lock.hcl` file, and commit it into your repository.
