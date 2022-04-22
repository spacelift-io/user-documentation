# Handling .tfvars

For some of our Terraform users, the most convenient solution to configure a stack is to specify its input values in a variable definitions file that is then passed to Terraform executions in _plan_ and _apply_ phases.

Spacelift supports this approach, but does not provide a separate mechanism, depending instead on a combination of Terraform's built-in mechanisms and Spacelift-provided primitives like:

* [environment variables](../../concepts/configuration/environment.md#environment-variables);
* [mounted files](../../concepts/configuration/environment.md#mounted-files)
* [`before_init` ](../../concepts/configuration/runtime-configuration/#before\_init-scripts)scripts;

### Using environment variables

In Terraform, special environment variables can be used to pass extra flags to executed commands like _plan_ or _apply_. These are the more generic [`TF_CLI_ARGS` __ and `TF_CLI_ARGS_name`](https://www.terraform.io/docs/cli/config/environment-variables.html#tf\_cli\_args-and-tf\_cli\_args\_name) that only affects a specific command. In Spacelift, environment variables can be defined directly on stacks and modules, as well as on [contexts](../../concepts/configuration/context.md) attached to those. As an example, let's declare the following environment variable:

![](/assets/images/Environment_%C2%B7_cube2222-testing-spacelift.png)

In our particular case we don't have this file checked in, so the run will fail:

![](/assets/images/Update_main_tf_%C2%B7_cube2222-testing-spacelift.png)

But we can supply this file dynamically using [mounted files](../../concepts/configuration/environment.md#mounted-files) functionality.

### Using mounted files

If the variable definitions file is not part of the repo, we can inject it dynamically. The above example can be fixed by supplying the variables file at the requested path:

![](/assets/images/Environment_%C2%B7_cube2222-testing-spacelift%20%281%29.png)

Note that there are "magical" names you can give to your variable definitions files that always get autoloaded, without the need to supply extra CLI arguments. [According to the documentation](https://www.terraform.io/docs/language/values/variables.html#variable-definitions-tfvars-files), Terraform automatically loads a number of variable definitions files if they are present:

* Files named exactly `terraform.tfvars` or `terraform.tfvars.json`.
* Any files with names ending in `.auto.tfvars` or `.auto.tfvars.json`.

The above can be used in conjunction with another Spacelift building block, [`before_init` hooks](../../concepts/configuration/runtime-configuration/#before\_init-scripts).

### Using before_init hooks

If you need to use different variable definitions files for different projects, would like to have them checked in to the repo, but would also want to avoid supplying extra CLI arguments, you could just dynamically move files - whether as a move, copy or a symlink to one of the autoloaded locations. This should happen in one of the `before_init` steps. Example:

![](/assets/images/Edit_stack_%C2%B7_cube2222-testing-spacelift.png)
