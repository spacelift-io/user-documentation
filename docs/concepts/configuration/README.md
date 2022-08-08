# Configuration

While Spacelift stacks typically link source code with infrastructure resources, it is often the broadly defined configuration that serves as the glue that's keeping everything together. These can be that access credentials, backend definitions or user-defined variables affecting the behavior of resource definitions found in the "raw" source code.

This section focuses on three aspects of configuration, each of which warrants its own help article:

- [Direct stack environment](environment.md), that is environment variables and mounted files;
- [Contexts](context.md), that is environments (often partially defined) shared between [stacks](../stack/README.md) and/or [Terraform modules](../../vendors/terraform/module-registry.md);
- [Runtime configuration](runtime-configuration/README.md) as defined in the `.spacelift/config.yml` file;

## A general note on precedence

Some configuration settings can be defined on multiple levels. If they're _over-defined_ (the same setting is defined multiple times), the end result will depend on generic rules of precedence. These rules will be the same for all applicable settings:

- stack-specific [runtime configuration](runtime-configuration/README.md) will take the highest precedence;
- configuration defined directly (either through the [environment](environment.md), or [settings](../stack/stack-settings.md)) on the stack will go second;
- common runtime configuration will go next;
- anything defined at the [context](context.md) level will take the lowest precedence - furthermore, contexts can be attached with a [priority level](context.md#a-note-on-priority) further defining the exact precedence;
