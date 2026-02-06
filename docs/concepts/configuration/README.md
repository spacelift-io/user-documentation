# Configuration

While Spacelift stacks typically link source code with infrastructure resources, the configuration is what keeps everything together. Configuration includes anything that affects the behavior of resource definitions found in the "raw" source code, including access credentials, backend definitions, and user-defined variables.

This section focuses on three aspects of configuration:

- [Direct stack environment](environment.md): Environment variables and mounted files.
- [Contexts](context.md): Environments (often partially defined) shared between [stacks](../stack/README.md) and/or [OpenTofu/Terraform modules](../../vendors/terraform/module-registry.md).
- [Runtime configuration](runtime-configuration/README.md): Configuration as defined in the `.spacelift/config.yml` file.

## Precedence

Some configuration settings can be defined on multiple levels. If they're _over-defined_ (the same setting is defined multiple times), the end result will depend on generic rules of precedence.

These rules of precedence will be the same for all applicable settings:

1. Stack-specific [runtime configuration](runtime-configuration/README.md).
2. Common runtime configuration.
3. Configuration defined directly (either through the [environment](environment.md), or [settings](../stack/stack-settings.md)) on the stack.
4. Anything defined at the [context](context.md) level. Furthermore, contexts can be attached with a [priority level](context.md#on-priority) further defining the exact precedence.
