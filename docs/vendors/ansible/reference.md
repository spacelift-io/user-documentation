---
description: Details about all available Ansible-specific configuration options.
---

# Reference

## Stack Settings

- **Playbook** - A playbook file to run on a stack.
- **Skip Plan** - Runs on Spacelift stacks typically have plan and apply phase. In Ansible for plan phase we are running Ansible in [check mode](https://docs.ansible.com/ansible/latest/user_guide/playbooks_checkmode.html#using-check-mode). However, not all Ansible modules support check mode and it can result in a run failure. You could configure your playbook to ignore certain errors (e.g. using `ignore_errors: "{{ ansible_check_mode }}"`) or choose to skip plan phase whatsoever (e.g. in situations when handling check failures at the playbook level is not an option).

## Other settings
For most of below settings there is usually more than one way to configure it (usually either through environment variables or through _ansible.cfg_ file). More on Ansible configuration can be found in [official Ansible docs](https://docs.ansible.com/ansible/latest/reference_appendices/config.html).

### SSH private key location
If you want to use SSH to connect to your hosts you will need to provide a path to SSH private key. You can do that using [`ANSIBLE_PRIVATE_KEY_FILE`](https://docs.ansible.com/ansible/latest/reference_appendices/config.html#default-private-key-file) environment variable.

### Forcing color mode for Ansible
By default, Ansible will not color the output when running without TTY. You could enable coloured output using [`ANSIBLE_FORCE_COLOR`](https://docs.ansible.com/ansible/latest/reference_appendices/config.html#ansible-force-color) environment variable.

### Debugging Ansible runs
When running into issues with Ansible playbooks a good way to debug the runs is to increase ansible verbosity level using [`ANSIBLE_VERBOSITY`](https://docs.ansible.com/ansible/latest/reference_appendices/config.html#default-verbosity) environment variable.

### Controlling SSH ControlPath parameter
Ansible uses `ControlMaster` and `ControlPath` SSH options to speed up playbook execution. On some occasions you might want to modify default values to make it compatible with your execution environment. Depending on your exact set up, you might want to adjust some of SSH settings Ansible uses.

On Spacelift Ansible stack we are setting [`ANSIBLE_SSH_CONTROL_PATH_DIR`](https://docs.ansible.com/ansible/2.5/reference_appendices/config.html#ansible-ssh-control-path-dir) to `/tmp/.ansible/cp` if not configured by the user otherwise.

## File permissions
There are a few nuances with certain files' permissions when using Ansible.

### ansible.cfg
If you use `ansible.cfg` file within a repository (or - more generally - within current working directory) make sure that permissions on that file (and parent directory) are set properly. You can find more details in official Ansible documentation in section on [avoiding security risks with `ansible.cfg`](https://docs.ansible.com/ansible/2.5/reference_appendices/config.html#avoiding-security-risks-with-ansible-cfg-in-the-current-directory)

### SSH private key files
If you are using SSH to connect to your hosts, then you need to make sure that private keys delivered to the worker have correct permissions.

As ssh man page states:
> These files contain sensitive data and should be readable by the user but not accessible by others (read/write/execute). `ssh` will simply ignore a private key file if it is accessible by others.

Typically, you would like to deliver private keys directly at the [worker level](../../concepts/worker-pools.md) where you can fully manage your environment. If that is not an option, you can always use our [read-only](../../concepts/configuration/environment.md#a-note-on-visibility) [mounted files](../../concepts/configuration/environment.md#mounted-files) or any other option you find suitable.
