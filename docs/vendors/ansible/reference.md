---
description: Details about all available Ansible-specific configuration options.
---

# Reference

## Stack Settings

- **Playbook** - A playbook file to run on a stack.
- **Skip Plan** - Runs on Spacelift stacks typically have a planning and an applying phase. In Ansible for the planning phase we are running Ansible in [check mode](https://docs.ansible.com/ansible/latest/user_guide/playbooks_checkmode.html#using-check-mode){: rel="nofollow"}. However, not all Ansible modules support check mode and it can result in a run failure. You could configure your playbook to ignore certain errors (e.g. using `ignore_errors: "{{ ansible_check_mode }}"`) or choose to skip the planning phase entirely (e.g. in situations when handling check failures at the playbook level is not an option).

## Other settings

For most of the settings below, there is usually more than one way to configure it (usually either through environment variables or through `ansible.cfg` file). More on Ansible configuration can be found in [official Ansible docs](https://docs.ansible.com/ansible/latest/reference_appendices/config.html).

### SSH private key location

If you want to use SSH to connect to your hosts you will need to provide a path to  the SSH private key. You can do that using the [`ANSIBLE_PRIVATE_KEY_FILE`](https://docs.ansible.com/ansible/latest/reference_appendices/config.html#default-private-key-file){: rel="nofollow"} environment variable.

### Forcing color mode for Ansible

By default, Ansible will not color the output when running without TTY. You could enable colored output using the [`ANSIBLE_FORCE_COLOR`](https://docs.ansible.com/ansible/latest/reference_appendices/config.html#ansible-force-color){: rel="nofollow"} environment variable.

### Debugging Ansible runs

When running into issues with Ansible playbooks a good way to debug the runs is to increase the Ansible verbosity level using the [`ANSIBLE_VERBOSITY`](https://docs.ansible.com/ansible/latest/reference_appendices/config.html#default-verbosity){: rel="nofollow"} environment variable.

### Controlling SSH ControlPath parameter

Ansible uses `ControlMaster` and `ControlPath` SSH options to speed up playbook execution. On some occasions, you might want to modify default values to make them compatible with your execution environment. Depending on your exact setup, you might want to adjust some of the SSH settings Ansible uses.

The default value for [`ANSIBLE_SSH_CONTROL_PATH_DIR`](https://docs.ansible.com/ansible/2.5/reference_appendices/config.html#ansible-ssh-control-path-dir) is `/tmp/.ansible/cp`.

## File permissions

There are a few nuances with certain files' permissions when using Ansible.

### ansible.cfg

If you use `ansible.cfg` file within a repository (or - more generally - within the current working directory) make sure that permissions on that file (and parent directory) are set properly. You can find more details in official Ansible documentation in the section on [avoiding security risks with `ansible.cfg`](https://docs.ansible.com/ansible/2.5/reference_appendices/config.html#avoiding-security-risks-with-ansible-cfg-in-the-current-directory){: rel="nofollow"}

### SSH private key files

If you are using SSH to connect to your hosts, then you need to make sure that private keys delivered to the worker have the correct permissions.

As the ssh man page states:
> These files contain sensitive data and should be readable by the user but not accessible by others (read/write/execute). `ssh` will simply ignore a private key file if it is accessible by others.

Typically, you would like to deliver private keys directly at the [worker level](../../concepts/worker-pools.md) where you can fully manage your environment. If that is not an option, you can always use our [read-only](../../concepts/configuration/environment.md#a-note-on-visibility) [mounted files](../../concepts/configuration/environment.md#mounted-files) or any other option you find suitable.
