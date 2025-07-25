# Integrate source code with Spacelift

For everything but raw Git, integrate your source code with Spacelift on the _Source code_ tab.

![](<../../assets/screenshots/getting-started/source-code/set-up-integration.png>)

1. Click **Set up integration**.
2. Select your VCS from the dropdown.
3. Follow the wizard to configure the integration.

Your source code can be stored on any of the supported version control systems (VCS):

- [GitHub](GitHub.md)
- [GitLab](GitLab.md)
- Bitbucket
    - [Cloud](Bitbucket-Cloud.md)
    - [Data Center/Server](Bitbucket-DataCenter.md)
- [Azure DevOps](Azure-DevOps.md)
- Raw Git

## Example starter repository

We provide a [Terraform Starter repository](https://github.com/spacelift-io/terraform-starter){: rel="nofollow"} you can fork to test Spacelift's capabilities right away.

!!! tip
    If you are using the Terraform starter repository, and you did not sign up for your Spacelift account with GitHub, you may need to add the environment variable `TF_VAR_github_app_namespace` with the value as your organization name or GitHub handle. You can do this under the `Environment` tab in the stack.
