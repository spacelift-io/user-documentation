# Configuration Management

The **Configuration Management view** is designed to enhance visibility, control, and monitoring of Ansible tasks across your stacks and runs.

This feature is available only for Ansible stacks, helping you monitor the last status of each item in your Ansible inventory. Configuration Management helps you:

- **Increase visibility:** Unified workflows for all tools, including Terraform, OpenTofu, and Ansible.
- **Encourage automation:** Seamlessly integrate infrastructure control and configuration management with stack dependencies.
- **Improve audit capabilities:** Collect, analyze, and filter data from execution logs.
- **Understand tasks intuitively:** Visualize and filter tasks with ease.

## Where to find it

### Stack view

The _Configuration Management_ view is available in the stack view, replacing the _Resources_ view for Ansible stacks.

1. In Spacelift, navigate to _Ship Infra_ > _Stacks_.
2. In the list, click the name of an Ansible stack.
3. Click **Configuration Management**.

![Configuration management view in stacks](<../../assets/screenshots/concepts/configuration-management/stack-view.png>)

!!! Info
    The _Configuration Management_ view replaces the _Resources_ view. If you need to see resources (e.g. because you have some historical resources to investigate), you can switch between the _Configuration Management_ and _Resources_ views with the **Enable configuration management view** toggle.

### Resources view

The _Configuration Management_ view is also a separate tab in the _Resources_ view.

![Configuration management tab in Resources view](<../../assets/screenshots/concepts/configuration-management/configuration-management-view.png>)

### Run view

The _Tasks_ tab in the _Run_ view provides detailed visibility into Ansible task execution during a run.

1. In Spacelift, navigate to _Ship Infra_ > _Stacks_.
2. In the list, click the name of an Ansible stack.
3. On the _Tracked runs_ tab, click the name of a task to inspect.
4. Click **Tasks**.

![Tasks tab in Run view](<../../assets/screenshots/concepts/configuration-management/run-view.png>)

## Key features

### Task monitoring

- View the last status of every item in your Ansible inventory, showing the outcome of the most recent run.
- Navigate seamlessly through tasks to analyze their status, logs, and execution details.

### Enhanced run list view

The updated run list now includes Ansible statuses, providing immediate insights without diving into individual runs.

### Detailed logs in task details

Access detailed logs for task execution in the task details tab to diagnose and debug issues efficiently.
