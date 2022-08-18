# Ansible Galaxy

If you followed previous examples in our Ansible documentation, you might have noticed that we do not do much in the Initialization phase.

![Empty initialization phase](../../assets/screenshots/ansible/ansible-13-empty-initialization.png)

If it comes to Ansible stacks, during that phase we try to auto-detect the _requirements.yml_ file that will be used to install dependencies. We will look for it in the following locations:

- _requirements.yml_ in root directory
- _roles/requirements.yml_ for roles requirements
- _collectinos/requirements.yml_ for collections requirements

As an example, try using an example _requirements.yml_ file.

```yaml title="Example requirements.yml file"
---
collections:
  - name: community.grafana
    version: 1.3.1
```

After our Initialization phase detects this file, it will use **ansible-galaxy** to install those dependencies.

![Installing community.grafana collection](../../assets/screenshots/ansible/ansible-14-installing-dependency.png)
