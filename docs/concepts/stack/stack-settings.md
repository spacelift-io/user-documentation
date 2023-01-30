# Stack settings

This article covers all settings that are set **directly on the stack**. It's important to note that these are not the only settings that affect how [runs](../run/README.md) and [tasks](../run/task.md) within a given stack are processed - [environment](../configuration/environment.md), attached [contexts](../configuration/context.md), [runtime configuration](../configuration/runtime-configuration/README.md) and various integrations will all play a role here, too.

## Video Walkthrough

<div style="padding:56.25% 0 0 0;position:relative;"><iframe src="https://player.vimeo.com/video/755645223?h=74912655ff&amp;badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen style="position:absolute;top:0;left:0;width:100%;height:100%;" title="Stack Settings"></iframe></div><script src="https://player.vimeo.com/api/player.js"></script>

## Common settings

### Administrative

This setting indicates whether a stack has administrative privileges within the [space](https://docs.spacelift.io/concepts/spaces/index.html) it lives in. Runs executed by administrative stacks receive an API token that gives them administrative access to a subset of the Spacelift API used by our [Terraform provider](../../vendors/terraform/terraform-provider.md), which means they can create, update and destroy Spacelift resources.

The main use case is to create one or a small number of administrative stacks that declaratively define the rest of Spacelift resources like other stacks, their [environments](../configuration/environment.md), [contexts](../configuration/context.md), [policies](../policy/README.md), [modules](../../vendors/terraform/module-registry.md), [worker pools](../worker-pools.md) etc. in order to avoid ClickOps.

Another pattern we've seen is stacks exporting their outputs as a [context](../configuration/context.md) to avoid exposing their entire state through the Terraform remote state pattern or using external storage mechanisms, like [AWS Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html){: rel="nofollow"} or [Secrets Manager](https://aws.amazon.com/secrets-manager/){: rel="nofollow"}.

If this sounds interesting and you want to give it a try, please refer to the [help article exclusively dedicated to Spacelift's Terraform provider](../../vendors/terraform/terraform-provider.md).

### Autodeploy

Indicates whether changes to the stack can be [applied](../run/README.md#applying) automatically. When autodeploy is set to _true_, any change to the [tracked branch](#repository-and-branch) will automatically be [applied](../run/README.md#applying) if the [planning](../run/README.md#planning) phase was successful and there are no plan policy warnings.

Consider setting it to _true_ if you always do a code review before merging to the tracked branch, and/or want to rely on [plan policies](../policy/terraform-plan-policy.md) to automatically flag potential problems. If each candidate change goes through a meaningful human code review with stack [writers](../policy/stack-access-policy.md#readers-and-writers) as reviewers, having a separate step to confirm deployment may be overkill. You may also want to refer to a [dedicated section](../policy/terraform-plan-policy.md#automated-code-review) on using plan policies for automated code review.

### Autoretry

Indicates whether obsolete proposed changes will be retried automatically. When autoretry is set to _true_ and a change gets applied, all Pull Requests to the [tracked branch](#repository-and-branch) conflicting with that change will be reevaluated based on the changed state.

This saves you from manually retrying runs on Pull Requests when the state changes. This way it also gives you more confidence, that the proposed changes will actually be the actual changes you get after merging the Pull Request.

Autoretry is only supported for [Stacks](./README.md) with a private [Worker Pool](../worker-pools.md) attached.

### Customizing workflow

Spacelift workflow can be customized by adding extra commands to be executed before and after each of the following phases:

- [Initialization](../run/README.md#initializing) (`before_init` and `after_init`, respectively)
- [Planning](../run/proposed.md#planning) (`before_plan` and `after_plan`, respectively)
- [Applying](../run/tracked.md#applying) (`before_apply` and `after_apply`, respectively)
- [Destroying](../run/test-case.md) (`before_destroy` and `after_destroy`, respectively)
- [Performing](../run/task.md#performing-a-task) (`before_perform` and `after_perform`, respectively)

You can also set up hooks (`after_run`) that will execute after each actively processed run, regardless of its outcome. These hooks will execute as part of the last "active" state of the run and will have access to an environment variable called `TF_VAR_spacelift_final_run_state` indicating the final state of the run.

Note here that all hooks, including the `after_run` ones, execute on the worker. Hence, the `after_run` hooks will not fire if the run is not being processed by the worker - for example, if the run is terminated outside of the worker (eg. canceled, discarded), there is an issue setting up the workspace or starting the worker container, or the worker container is killed while processing the run.

These commands may serve one of two general purposes - either to make some modifications to your workspace (eg. set up symlinks, move files around etc.) or perhaps to run validations using something like [`tfsec`](https://github.com/tfsec/tfsec){: rel="nofollow"}, [`tflint`](https://github.com/terraform-linters/tflint){: rel="nofollow"} or `terraform fmt`.

!!! danger
    When a run resumes after having been paused for any reason (e.g., confirmation, approval policy), the remaining phases are run in a new container. As a result, any tool installed in a phase that occurred before the pause won't be available in the subsequent phases. A better way to achieve this would be to bake the tool into a [custom runner image](../../integrations/docker.md#customizing-the-runner-image).

!!! info
    If any of the "before" hooks fail (non-zero exit code), the relevant phase is not executed. If the phase itself fails, none of the "after" hooks get executed.

The workflow can be customized either using our [Terraform provider](https://registry.terraform.io/providers/spacelift-io/spacelift/latest/docs/resources/stack){: rel="nofollow"} or in the GUI. The GUI has a very nice editor that allows you to select the phase you want to customize and add commands before and after each phase. You will be able to add and remove commands, reorder them using _drag and drop_ and edit them in-line. Note how the commands that precede the customized phase are the "before" hooks (`ps aux` and `ls` in the example below), and the ones that go after it are the "after" hooks (`ls -la .terraform`):

![](<../../assets/screenshots/Mouse_Highlight_Overlay (7).png>)

Perhaps worth noting is the fact that these commands run in the same shell session as the phase itself. So the phase will have access to any shell variables exported by the preceding scripts.

Environment variables are preserved from one phase to the next.

!!! info
    These scripts can be overridden by the [runtime configuration](../configuration/runtime-configuration/README.md#before_init-scripts) specified in the `.spacelift/config.yml` file.

### Enable local preview

Indicates whether creating [proposed Runs](../run/proposed.md) based on user-uploaded local workspaces is allowed.

If this is enabled, you can use [spacectl](https://github.com/spacelift-io/spacectl) to create a proposed run based on the directory you're in:

```bash
spacectl stack local-preview --id <stack-id>
```

!!! danger
    This in effect allows anybody with write access to the Stack to execute arbitrary code with access to all the environment variables configured in the Stack.

    Use with caution.

### Name and description

Stack name and description are pretty self-explanatory. The required _name_ is what you'll see in the stack list on the home screen and menu selection dropdown. Make sure that it's informative enough to be able to immediately communicate the purpose of the stack, but short enough so that it fits nicely in the dropdown, and no important information is cut off.

The optional _description_ is completely free-form and it supports [Markdown](https://daringfireball.net/projects/markdown/){: rel="nofollow"}. This is perhaps a good place for a thorough explanation of the purpose of the stack, perhaps a link or two, and an obligatory cat GIF.

!!! warning
    Based on the original _name_, Spacelift generates an immutable slug that serves as a unique identifier of this stack. If the name and the slug diverge significantly, things may become confusing.

    So even though you can change the stack name at any point, we strongly discourage all non-trivial changes.

### Labels

Labels are arbitrary, user-defined tags that can be attached to Stacks. A single Stack can have an arbitrary number of these, but they **must** be unique. Labels can be used for any purpose, including UI filtering, but one area where they shine most is user-defined [policies](../policy/README.md#policies-and-stack-labels) which can modify their behavior based on the presence (or lack thereof) of a particular label.

### Project root

Project root points to the directory within the repo where the project should start executing. This is especially useful for monorepos, or indeed repositories hosting multiple somewhat independent projects. This setting plays very well with [Git push policies](../policy/git-push-policy.md), allowing you to easily express generic rules on what it means for the stack to be affected by a code change.

!!! info
    The project root can be overridden by the [runtime configuration](../configuration/runtime-configuration/README.md#project_root-setting) specified in the `.spacelift/config.yml` file.

### Repository and branch

_Repository_ and _branch_ point to the location of the source code for a stack. The repository must either belong to the GitHub account linked to Spacelift  (its choice may further be limited by the way the Spacelift GitHub app has been installed) or to the GitLab server integrated with your Spacelift account. For more information about these integrations, please refer to our [GitHub](../../integrations/source-control/github.md) and [GitLab](../../integrations/source-control/gitlab.md) documentation respectively.

Thanks to the strong integration between GitHub and Spacelift, the link between a stack and a repository can survive the repository being renamed in GitHub. If you're storing your repositories in GitLab then you need to make sure to manually (or programmatically, using [Terraform](../../vendors/terraform/terraform-provider.md)) point the stack to the new location of the source code.

!!! info
    Spacelift does not support moving repositories between GitHub accounts, since Spacelift accounts are strongly linked to GitHub ones. In that case the best course of action is to take your Terraform state, download it and import it while recreating the stack (or multiple stacks) in a different account. After that, all the stacks pointing to the old repository can be safely deleted.

    Moving a repository between GitHub and GitLab or the other way around is simple, however. Just change the provider setting on the Spacelift project, and point the stack to the new source code location.

_Branch_ signifies the repository branch **tracked** by the stack. By default, that is unless a [Git push policy](../policy/git-push-policy.md) explicitly determines otherwise, a commit pushed to the tracked branch triggers a deployment represented by a **tracked** run. A push to any other branch by default triggers a test represented by a **proposed** run. More information about git push policies, tracked branches, and head commits can be found [here](../policy/git-push-policy.md#git-push-policy-and-tracked-branch).

Results of both tracked and proposed runs are displayed in the source control provider using their specific APIs - please refer to our [GitHub](../../integrations/source-control/github.md) and [GitLab](../../integrations/source-control/gitlab.md) documentation respectively to understand how Spacelift feedback is provided for your infrastructure changes.

!!! info
    A branch _must_ exist before it's pointed to in Spacelift.

### Runner image

Since every Spacelift job (which we call [runs](../run/README.md)) is executed in a separate Docker container, setting a custom runner image provides a convenient way to prepare the exact runtime environment your infra-as-code flow is designed to use.

Additionally, for our Pulumi integration overriding the default runner image is the canonical way of selecting the exact Pulumi version and its corresponding language SDK.

You can find more information about our use of Docker in [this dedicated help article](../../integrations/docker.md).

!!! info
    Runner image can be overridden by the [runtime configuration](../configuration/runtime-configuration/README.md#runner_image-setting) specified in the `.spacelift/config.yml` file.

!!! warning
    On the public worker pool, Docker images can only be pulled from [allowed registries](../../integrations/docker.md#allowed-registries-on-public-worker-pools). On private workers, images can be stored in any registry, including self-hosted ones.

### Worker pool

## Terraform-specific settings

### Version {: #terraform-version}

The Terraform version is set when a stack is created to indicate the version of Terraform that will be used with this project. However, Spacelift covers the entire [Terraform version management](../../vendors/terraform/version-management.md) story, and applying a change with a newer version will automatically update the version on the stack.

### Workspace {: #terraform-workspace}

[Terraform workspaces](https://www.terraform.io/docs/language/state/workspaces.html){: rel="nofollow"} are supported by Spacelift, too, as long as your state backend supports them. If the workspace is set, Spacelift will try to first [_select_, and then - should that fail - automatically _create_](https://www.terraform.io/docs/language/state/workspaces.html#using-workspaces){: rel="nofollow"} the required workspace on the state backend.

If you're [managing Terraform state through Spacelift](../../vendors/terraform/state-management.md), the workspace argument is ignored since Spacelift gives each stack a separate workspace by default.

## Pulumi-specific settings

### Login URL {: #pulumi-login-url}

Login URL is the address Pulumi should log into during Run initialization. Since we do not yet provide a full-featured Pulumi state backend, you need to bring your own (eg. [Amazon S3](https://www.pulumi.com/docs/intro/concepts/state/#logging-into-the-aws-s3-backend){: rel="nofollow"}).

You can read more about the login process [here](https://www.pulumi.com/docs/reference/cli/pulumi_login/){: rel="nofollow"}. More general explanation of Pulumi state management and backends is available [here](https://www.pulumi.com/docs/intro/concepts/state/){: rel="nofollow"}.

### Stack name {: #pulumi-stackname}

The name of the Pulumi stack which should be selected for backend operations. Please do not confuse it with the [Spacelift stack name](stack-settings.md#stack-name) - they _may_ be different, though it's probably good if you can keep them identical.
