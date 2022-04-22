# CLI Configuration

For some of our Terraform users, a convenient way to configure the Terraform CLI behavior is through customizing the `~/.terraformrc` file.

During the preparing phase of a run, Spacelift creates a configuration file at the default location: `~/.terraformrc`. This file contains credentials that are needed to communicate with remote services.

## Extending CLI configuration

Extending the Terraform CLI behavior can be done by using [mounted files](../../concepts/configuration/environment.md#mounted-files):

#### Using mounted files

Any mounted files with names ending in `.terraformrc` will be appended to `~/.terraformrc`.

!!! Info
The Terraform CLI configuration file syntax supports [these settings](https://www.terraform.io/docs/cli/config/config-file.html#available-settings)




