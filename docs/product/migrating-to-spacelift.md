# Migrating to Spacelift

Migrating from one Infrastructure as Code CI/CD provider to another can feel daunting. This is why we created a [migration kit](https://github.com/spacelift-io/spacelift-migration-kit){: rel="nofollow"} that takes care of the heavy lifting.

Edit a few settings, and let it do the hard work. Then review, and possibly tweak, the generated code, and finally have your Spacelift entities created.

There is no one-size-fits-all for this kind of migration. This is why we designed this tool to be flexible and easy to hack to meet your specific needs. Feel free to reach out to our [support team](./support/README.md) if you need any help or guidance.

## Overview

The migration process is as follows:

- Export the definition for your resources at your current vendor.
- Generate the Terraform code to recreate similar resources at Spacelift using the [Terraform provider](https://registry.terraform.io/providers/spacelift-io/spacelift/latest/docs).
- Review and possibly edit the generated Terraform code.
- Commit the Terraform code to a repository.
- Create a manager Spacelift stack that points to the repository with the Terraform code.

!!! tip
    Currently, only Terraform Cloud and Terraform Enterprise are supported as sources. The instructions below apply to both.

## Prerequisites

- Terraform

## Instructions

### Preparation

- Clone the [Spacelift Migration Kit repository locally](https://github.com/spacelift-io/spacelift-migration-kit){: rel="nofollow"}.
- Use the `terraform login spacelift.io` command to ensure that Terraform can interact with your Spacelift account.

Depending on the exporter used, you may need additional steps:

- **Terraform Cloud/Enterprise**: Use the `terraform login` command to ensure that Terraform can interact with your Terraform Cloud/Enterprise account.

### Pre-Migration Cleanup

In order to start fresh, clean up files and folders from previous runs.

```shell
rm -rf ./out ./{exporters/tfc,generator,manager-stack}/.terraform ./{exporters/tfc,generator,manager-stack}/.terraform.lock.hcl ./{exporters/tfc,generator,manager-stack}/terraform.tfstate ./{exporters/tfc,generator,manager-stack}/terraform.tfstate.backup
```

### Export the resource definitions and Terraform state

- Choose an exporter and copy the example `.tfvars` file for it into `exporter.tfvars`.
- Edit that file to match your context.
- Run the following commands:

```shell
cd exporters/<EXPORTER>
terraform init
terraform apply -auto-approve -var-file=../../exporter.tfvars
```

A new `out` folder should have been created. The `data.json` files contains the mapping of your vendor resources to the equivalent Spacelift resources, and the `state-files` folder contains the files for the Terraform state of your stacks, if the state export was enabled.

Please note that once exported the Terraform state files can be imported into Spacelift or to any backend supported by Terraform.

### Generate the Terraform code

- If you want to customize the template that generates the Terraform code, run `cp ../../generator/generator.tftpl ../generator.tftpl`, and edit the `generator.tftpl` file at the root of the repository. If present, it will be used automatically.
- Run the following commands:

```shell
cd ../../generator
terraform init
terraform apply -auto-approve -var-file=../out/data.json
```

### Review and edit the generated Terraform code

A `main.tf` should have been generated in the `out` folder. It contains all the Terraform code for your Spacelift resources.

Mapping resources from a vendor to Spacelift resources is not an exact science. There are gaps in functionality and caveats in the mapping process.

Please carefully review the generated Terraform code and make sure that it looks fine. If it does not, repeat the process with a different configuration or edit the Terraform code.

### Commit the Terraform code

When the Terraform code is ready, commit it to a repository.

### Create a manager Spacelift stack

It is now time to create a Spacelift stack that will point to the committed Terraform code that manages your Spacelift resources.

- Copy the example `manager-stack.example.tfvars` file into `manager-stack.tfvars` .
- Edit that file to match your context.
- Run the following commands:

```shell
cd ../manager-stack
terraform init
terraform apply -auto-approve -var-file=../manager-stack.tfvars
```

After the stack has been created, a tracked run will be triggered automatically. That run will create the defined Spacelift resources.

### Post-Migration Cleanup

Before you can use Spacelift to manage your infrastructure,  you may need to make changes to the Terraform code for your infrastructure, depending on the Terraform state is managed.

If the Terraform state is managed by Spacelift,perform the following actions, otherwise you can skip this section:

- Remove any [backend](https://developer.hashicorp.com/terraform/language/settings/backends/configuration#using-a-backend-block)/[cloud](https://developer.hashicorp.com/terraform/language/settings/terraform-cloud) block from the Terraform code that manages your infrastructure to avoid a conflict with Spacelift's backend.
- Delete the `import_state_file` arguments from the Terraform code that manages your Spacelift resources.
- After the manager stack has successfully run, the mounted Terraform state files are not needed anymore and can be deleted by setting the `import_state` argument to `false` in the `manager-stack.tfvars` file and run `terraform apply -auto-approve -var-file=../manager-stack.tfvars` in the `manager-stack` folder.

## Sources

### Terraform Cloud/Enterprise

#### Known Limitations

The limitations listed below come from the original provider. We are actively looking for workarounds.

- The variable sets are not exposed so they cannot be listed and exported.
- The name of the Version Control System (VCS) provider for a stack is not returned so it has to be set in the exporter configuration file.
- When the branch for the stack is the repository default branch, the value is empty. You can set the value for the default branch in the exporter configuration file, or edit the generated Terraform code.

#### Glossary

| Terraform Cloud/Enterprise | Spacelift                                                    |
| -------------------------- | ------------------------------------------------------------ |
| Agent Pool                 | [Worker Pool](../concepts/worker-pools.md)                   |
| Organization               | [Account](https://docs.spacelift.io/getting-started#step-1-create-your-spacelift-account) |
| Policy                     | [Policy](../concepts/policy/README.md)                       |
| Project                    | [Space](../concepts/spaces/README.md)                        |
| Variable                   | [Environment Variable](https://docs.spacelift.io/concepts/configuration/environment#environment-variables) |
| Variable Set               | [Context](../concepts/configuration/context.md)              |
| Workspace                  | [Stack](../concepts/stack/README.md)                         |
