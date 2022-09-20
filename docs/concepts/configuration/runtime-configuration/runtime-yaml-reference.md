# YAML reference

This document is a reference for the Spacelift configuration keys that are used in the `.spacelift/config.yml` file to configure one or more [Stacks](../../stack/README.md).

!!! warning
    The `.spacelift/config.yml` file must be located at the root of your repository, not at the [project root](../../stack/stack-settings.md#project-root).

## Stack settings

- [`version`](runtime-yaml-reference.md#version)
- [`stack_defaults`](runtime-yaml-reference.md#stack_defaults)
- [`stacks`](runtime-yaml-reference.md#stacks)

## Module settings

- [`version`](runtime-yaml-reference.md#version)
- [`module_version`](runtime-yaml-reference.md#module_version)
- [`test_defaults`](runtime-yaml-reference.md#test_defaults)
- [`tests`](runtime-yaml-reference.md#tests)

### `version`

The version property is optional and currently ignored but for the sake of completeness you may want to set the value to "1".

### `stack_defaults`

`stack_defaults` represent default settings that will apply to every stack defined in the [id-settings](runtime-yaml-reference.md#stack-id) map. Any default setting is overridden by an explicitly set stack-specific value.

| Key                 | Required | Type                 | Description                                                                                                                                      |
| ------------------- | -------- | -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `after_apply`       | N        | list<string\>        | List of commands executed [after applying changes](../../stack/stack-settings.md#before-apply-scripts).                                          |
| `after_destroy`     | N        | list<string\>        | List of commands executed after destroying managed resources.                                                                                    |
| `after_init`        | N        | list<string\>        | List of commands executed [after first interacting with the backend](../../stack/stack-settings.md#before-init-scripts) (eg. terraform init).    |
| `after_perform`     | N        | list<string\>        | List of commands executed after [performing a custom task](../../run/task.md#performing-a-task)                                                  |
| `after_plan`        | N        | list<string\>        | List of commands executed after [planning changes](../../run/proposed.md#planning)                                                               |
| `before_apply`      | N        | list<string\>        | List of commands executed [before applying changes](../../stack/stack-settings.md#before-apply-scripts).                                         |
| `before_destroy`    | N        | list<string\>        | List of commands executed before destroying managed resources.                                                                                   |
| `before_init`       | N        | list<string\>        | List of commands executed [before first interacting with the backend](../../stack/stack-settings.md#before-init-scripts) (eg. `terraform init`). |
| `before_perform`    | N        | list<string\>        | List of commands executed before [performing a custom task](../../run/task.md#performing-a-task)                                                 |
| `before_plan`       | N        | list<string\>        | List of commands executed before [planning changes](../../run/proposed.md#planning)                                                              |
| `environment`       | N        | map<string, string\> | Map of extra [environment variables](../environment.md#environment-variables) and their values passed to the job                                 |
| `project_root`      | N        | string               | Optional folder inside the repository serving as the [root of your stack](../../stack/stack-settings.md#project-root)                            |
| `runner_image`      | N        | string               | Name of the [custom runner image](../../stack/stack-settings.md#runner-image), if any                                                            |
| `terraform_version` | N        | string               | For Terraform stacks, [Terraform version number to be used](../../../vendors/terraform/version-management.md#intro-to-terraform-versioning)      |

### `stacks`

The stacks section is a map using stack public ID (slug) as keys and stack settings - described in [this section](runtime-yaml-reference.md#stack_defaults) - as values. If you're using this mapping together with stack defaults, note that any default setting is overridden by an explicitly set stack-specific value. This is particularly important for list and map fields where one may assume that these are merged. In practice, they're not merged - they're replaced. If you want merging semantics, [YAML provides native methods to merge arrays and maps](http://blogs.perl.org/users/tinita/2019/05/reusing-data-with-yaml-anchors-aliases-and-merge-keys.html).

### `module_version`

Module version is a **required string** value that must conform to the [semantic versioning scheme](https://semver.org/){: rel="nofollow"}. Note that pre-releases and builds/nightlies are not supported - only the standard `$major.$minor.$patch` format will work.

### `test_defaults`

Test defaults are runtime settings following [this scheme](runtime-yaml-reference.md#stack_defaults) that will apply to all test cases for a [module](../../../vendors/terraform/module-registry.md).

### `tests`

The `tests` section represents a list of test cases for a module, each containing the [standard runtime settings](runtime-yaml-reference.md#stack_defaults) in addition to the test-specific settings:

| Key      | Required | Type   | Description                                                 |
| -------- | -------- | ------ | ----------------------------------------------------------- |
| name     | Y        | string | Unique name of the test case                                |
| negative | N        | bool   | Indicates whether the test is _negative_ (expected to fail) |
