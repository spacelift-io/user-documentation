# Policy

{% if is_saas() %}
!!! Info
    This feature is only available to paid Spacelift accounts. Please check out our [pricing page](https://spacelift.io/pricing){: rel="nofollow"} for more information.
{% endif %}

Policy-as-code is the idea of expressing rules using a high-level programming language and treating them as you normally treat code, which includes version control as well as continuous integration and deployment. This approach extends the infrastructure-as-code approach to also cover the rules governing this infrastructure, and the platform that manages it.

Spacelift as a development platform is built around this concept and allows defining policies that involve various decision points in the application. User-defined policies can decide:

- **Login**: [Who gets to log in](login-policy.md) to your Spacelift account and with what level of access.
- **Access**: [Who gets to access individual Stacks](stack-access-policy.md) and with what level of access. Access policies have been replaced by [space access control](../spaces/access-control.md).
- **Approval**: [Who can approve or reject a run](approval-policy.md) and how a run can be approved.
- **Initialization**: [Which runs and tasks can be started](run-initialization-policy.md). Initialization policies have been replaced by [approval policies](./approval-policy.md).
- **Notification**: [Routing and filtering notifications](notification-policy.md).
- **Plan**: [Which changes can be applied](terraform-plan-policy.md).
- **Push**: [How Git push events are interpreted](push-policy/README.md).
- **Task**: [Which one-off commands can be executed](task-run-policy.md). Task run policies have been replaced by [approval policies](./approval-policy.md).
- **Trigger**: [What happens when blocking runs terminate](trigger-policy.md). Trigger policies have been mostly replaced by [stack dependencies](../stack/stack-dependencies.md).

Please refer to the following table for information on what each policy types returns, and the rules available within each policy.

| Type | Purpose | Types | Returns | Rules |
|------|---------|-------|---------|-------|
| [Login](login-policy.md) | Allow or deny login, grant admin access | Positive and negative | `boolean` | `allow`, `admin`, `deny`, `deny_admin` |
| [Access](stack-access-policy.md) | Grant or deny appropriate level of stack access | Positive and negative | `boolean` | `read`, `write`, `deny`, `deny_write` |
| [Approval](approval-policy.md) | Who can approve or reject a run and how a run can be approved | Positive and negative | `boolean` | `approve, reject` |
| [Initialization](run-initialization-policy.md) | Blocks suspicious [runs](../run/README.md) before they [start](../run/README.md#initializing) | Negative | `set<string>`      | `deny` |
| [Notification](notification-policy.md) | Routes and filters notifications | Positive | `map<string, any>` | `inbox`, `slack`, `webhook` |
| [Plan](terraform-plan-policy.md) | Gives feedback on [runs](../run/README.md) after [planning](../run/proposed.md#planning) phase | Negative | `set<string>` | `deny`, `warn` |
| [Push](push-policy/README.md) | Determines how a Git push event is interpreted | Positive and negative | `boolean` | `track`, `propose`, `ignore`, `ignore_track`, `notrigger`, `notify` |
| [Task](task-run-policy.md) | Blocks suspicious [tasks](../run/task.md) from running | Negative | `set<string>` | `deny` |
| [Trigger](trigger-policy.md) | Selects [stacks](../stack/README.md) for which to trigger a [tracked run](../run/tracked.md) | Positive | `set<string>` | `trigger` |

!!! tip
    We maintain a [library of example policies](https://github.com/spacelift-io/spacelift-policies-example-library){: rel="nofollow"} that are ready to use or alter to meet your specific needs.

    For up-to-date policy input information you can also refer to [official Spacelift policy contract schema](https://app.spacelift.io/.well-known/policy-contract.json){:+ rel="nofollow"}.

    If you cannot find what you are looking for, please reach out to [our support](../../product/support/README.md#contact-support) and we will craft a policy to do exactly what you need.

## How it works

Spacelift uses an open-source project called [**Open Policy Agent**](https://www.openpolicyagent.org/){: rel="nofollow"} and its rule language, [**Rego**](https://www.openpolicyagent.org/docs/latest/policy-language/){: rel="nofollow"}, to execute policies at various decision points.

You can think of policies as snippets of code that receive some JSON-formatted input (the data needed to make a decision) and are allowed to produce an output in a predefined form.  Each policy type exposes slightly different data, so please refer to their respective schemas for more information.

[Login policies](./login-policy.md) are global. All other policy types operate on the [stack](../stack/README.md) level and can be attached to multiple stacks, like [contexts](../configuration/context.md), which facilitates code reuse and allows flexibility. Policies only affect stacks they're [attached to](#attaching-policies).

Multiple policies of the same type can be attached to a single stack, in which case they are evaluated separately to avoid having their code (like local variables and helper rules) affect one another. Once these policies are evaluated against the same input, their results are **combined**. So if you allow user login from one policy but deny it from another, the result will still be a denial.

### OPA version

We update the version of OPA that we are using regularly. To find out the version we are currently running, use this query:

```graphql
query getOPAVersion{
    policyRuntime {
        openPolicyAgentVersion
    }
}
```

For more detailed information about the GraphQL API and its integration, please refer to the [API documentation](../../integrations/api.md).

### Policy language

[Rego](https://www.openpolicyagent.org/docs/latest/policy-language/){: rel="nofollow"}, the language we're using to execute policies, is a very elegant, Turing incomplete data query language. If you know SQL and [`jq`](https://stedolan.github.io/jq/){: rel="nofollow"}, you should find Rego familiar and only need a few hours to understand its quirks. For each policy, we also provide examples you can tweak to achieve your goals.

### Rego constraints

To keep policies functionally pure and relatively snappy, we disabled some Rego built-ins that can query external or runtime data. These are:

- `http.send`
- `opa.runtime`
- `rego.parse_module`
- `time.now_ns`
- `trace`

Policies must be self-contained and cannot refer to external resources (e.g. files in a VCS repository).

!!! info

    Disabling `time.now_ns` may seem surprising, but depending on the current timestamp it can make your policies impure and thus tricky to test. We encourage you to [test your policies thoroughly](#testing-policies)!
    
    The current timestamp in Rego-compatible form (Unix nanoseconds) is available as `spacelift.request.timestamp_ns` in plan policy payloads, so please use it instead.

## Policy returns and rules

Please refer to the following table for information on what each policy types returns, and the rules available within each policy.

| Type  | Purpose  | Types   | Returns   | Rules  |
|-------|----------|---------|-----------|--------|
| [Login](login-policy.md) | Allow or deny login, grant admin access | Positive and negative | `boolean` | `allow`, `admin`, `deny`, `deny_admin`|
| [Access](stack-access-policy.md) | Grant or deny appropriate level of stack access | Positive and negative | `boolean` | `read`, `write`, `deny`, `deny_write` |
| [Approval](approval-policy.md) | Who can approve or reject a run and how a run can be approved | Positive and negative | `boolean` | `approve`, `reject` |
| [Initialization](run-initialization-policy.md) | Blocks suspicious [runs](../run/README.md) before they [start](../run/README.md#initializing) | Negative | `set<string>` | `deny` |
| [Notification](notification-policy.md) | Routes and filters notifications | Positive | `map<string, any>` | `inbox`, `slack`, `webhook` |
| [Plan](terraform-plan-policy.md) | Gives feedback on [runs](../run/README.md) after [planning](../run/proposed.md#planning) phase | Negative | `set<string>` | `deny`, `warn` |
| [Push](push-policy/README.md) | Determines how a Git push event is interpreted | Positive and negative | `boolean` | `track`, `propose`, `ignore`, `ignore_track`, `notrigger`, `notify` |
| [Task](task-run-policy.md) | Blocks suspicious [tasks](../run/task.md) from running | Negative | `set<string>` | `deny` |
| [Trigger](trigger-policy.md) | Selects [stacks](../stack/README.md) for which to trigger a [tracked run](../run/tracked.md) | Positive | `set<string>` | `trigger` |

!!! tip
    We maintain a [library of example policies](https://github.com/spacelift-io/spacelift-policies-example-library){: rel="nofollow"} that you can tweak to meet your specific needs or use as-is.

    If you cannot find what you are looking for, please reach out to [our support](../../product/support/README.md) and we will craft a policy to do exactly what you need.

### Boolean

[Login](login-policy.md) and [access](stack-access-policy.md) policies expect rules to return a **boolean value** (_true_ or _false_). Each type of policy defines its own set of rules corresponding to different access levels. In these cases, various types of rules can be positive or negative (that is, they can explicitly **allow** or **deny** access).

### Set of strings

The second group of policies ([initialization](run-initialization-policy.md), [plan](terraform-plan-policy.md), and [task](task-run-policy.md)) is expected to generate a [**set of strings**](https://www.openpolicyagent.org/docs/latest/policy-language/#generating-sets){: rel="nofollow"} that serve as _direct feedback_ to the user. Those rules are generally negative in that they **can only block** certain actions. Only their lack counts as an implicit success.

Here's a practical difference between the two types:

=== "Boolean returns"
    ```opa title="boolean.rego"
    package spacelift

    # This is a simple deny rule.
    # When it matches, no feedback is provided.
    deny {
      true
    }
    ```

=== "String returns"
    ```opa title="string.rego"
    package spacelift

    # This is a deny rule with string value.
    # When it matches, that value is reported to the user.
    deny["the user will see this"] {
      true
    }
    ```

For the policies that generate a set of strings, you want these strings to be both informative and relevant, so you'll see this pattern a lot in the examples:

```opa
package spacelift

we_dont_create := { "scary", "resource", "types" }

# This is an example of a plan policy.
deny[sprintf("some rule violated (%s)", [resource.address])] {
  some resource
  created_resources[resource]

  we_dont_create[resource.type]
}
```

### Complex objects

[Notification](notification-policy.md) policies will generate and return more complex objects, typically JSON objects. In terms of syntax, the returned values are still very similar to policies that return sets of strings, but they provide additional information inside the returned decision.

For example, this rule which will return a JSON object to be used when creating a custom notification:

```opa
package spacelift

inbox[{
  "title": "Tracked run finished!",
  "body": sprintf("Run ID: %s", [run.id]),
  "severity": "INFO",
}] {
  run := input.run_updated.run
  run.type == "TRACKED"
  run.state == "FINISHED"
}
```

### Helper functions

The following helper functions can be used in Spacelift policies:

| Name | Description |
| ---- | ----------- |
| `output := sanitized(x)` | `output` is the string `x` sanitized using the same algorithm we use to sanitize secrets. |
| `result := exec(x)` | Executes the command `x`. `result` is an object containing `status`, `stdout` and `stderr`. Only applicable for run initialization policies for [private workers](../worker-pools). |

## Creating policies

You can create policies through the web UI and the [Terraform provider](../../vendors/terraform/terraform-provider.md). We generally suggest the latter, as it's much easier to manage down the line and [allows proper unit testing](#testing-policies).

### With the Terraform provider

Here's how you would define a plan policy in Terraform and attach it to a stack (also created here with minimal configuration):

```opa
resource "spacelift_stack" "example-stack" {
  name       = "Example stack"
  repository = "example-stack"
  branch     = "master"
}

# This example assumes that you have Rego policies in a separate
# folder called "policies".
resource "spacelift_policy" "example-policy" {
  name = "Example policy"
  body = file("${path.module}/policies/example-policy.rego")
  type = "TERRAFORM_PLAN"
}

resource "spacelift_policy_attachment" "example-attachment" {
  stack_id  = spacelift_stack.example-stack.id
  policy_id = spacelift_policy.example-policy.id
}
```

### With the web UI

**You must be a Spacelift admin to manage policies**.

You can create approval, push, plan, trigger, and notification policies in the web UI. [Login policies](./login-policy.md) are created in a different section of the UI.

![Click Create Policy at the top right of the view.](<../../assets/screenshots/create-policy1.png>)

1. Navigate to the _Enforce Guardrails_ > _Policies_ tab in Spacelift.
2. Click **Create policy**.
3. Fill in the required policy details:
      1. **Name**: Enter a unique, descriptive name for the policy.
      2. **Type**: Select the type of policy from the dropdown.
      3. **Space**: Select the space to create the policy in.
      4. **Description** (optional): Enter a (markdown-supported) description for the policy.
      5. **Labels** (optional): Add labels to help sort and filter your policies. You can use `autoattach:label` to attach the policy to stacks or modules with the chosen `label` automatically.
4. Click **Continue** to edit the policy.
      - You'll see an example policy body based on the type you chose. Remove the comments from any rules you'd like to apply and add or change rules as needed.
5. Click **Create policy**. You can always edit policies as needed.

### Policy structure

We prepend variable definitions to each policy. These variables can be different for each type, but the prepended code is very similar. Here's an example for the [Approval](approval-policy.md) policy:

```opa
package spacelift

# This is what Spacelift will query for when evaluating policies.
result = {
  "approve": approve,
  "reject": reject,
  "flag": flag,
  "sample": sample,
}

# Default to ensure that "approve" is defined.
default approve = false

# Default to ensure that "reject" is defined.
default reject = false

# Default to ensure that "sample" is defined.
default sample = false

# Placeholder to ensure that "flag" will be a set.
flag["never"] {
  false
}
```

!!! warning
    You can't change predefined variable types. Doing so will result in a policy validation error and the policy won't be saved.

## Attaching policies

### Automatically (with labels)

With the exception of [login policies](login-policy.md), policies can be automatically attached to stacks using the `autoattach:label` special label. Replace `label` with the name of a label attached to stacks and/or modules in your Spacelift account you wish the policy to be attached to.

#### Policy attachment example

Adding `autoattach:needs_approval` label to your policy will automatically attach the policy to all stacks/modules with the label `needs_approval`. This can be done with any label you're using on your stacks and modules.

![Attach policy to anything with the needs_approval label](<../../assets/screenshots/approval_needed.png>)

#### Wildcard policy attachments

You can also attach a policy to stacks/modules using a wildcard. For example, using `autoattach:*` as a label will attach the policy to all stacks/modules.

### Manually

In the web UI, attaching policies is done in the stack management view:

![Select a policy and manually attach it to the stack](<../../assets/screenshots/policies/Policies_AttachtoStack.png>)

1. Navigate to the _Ship Infra_ > _Stacks_ tab.
2. Click the name of the stack to attach a policy to.
3. Click the **Policies** tab, then click **Attach policy**.
4. Select policy details:
    ![Attach a policy to a stack](<../../assets/screenshots/policies/AttachPolicyDrawer.png>)
      - **Policy type**: Select the type of policy from the dropdown list.
      - **Select policy**: Choose the specific policy to add from the dropdown list.
5. Click **Attach**.

## Policy workbench

Sometimes, it takes trial and error to get policies working as intended. This is due to several factors: an unfamiliarity with the concept, a learning curve with the policy language, and/or the slow feedback cycle. Generally, feedback can easily take hours as you iterate through writing a plan policy, making a code change, triggering a run, verifying policy behavior, and rinsing and repeating.

Enter **policy workbench**. Policy workbench captures policy evaluation events so that you can adjust the policy independently, shortening the entire cycle. In order to use the workbench, you will first need to sample policy inputs.

### Sample policy inputs

Each of Spacelift's policies supports an additional boolean rule called `sample`. Returning `true` from this rule means that the input to the policy evaluation is captured, along with the policy body at the time and the exact result of the policy evaluation. You can, for example, capture every evaluation with a simple:

```opa
sample { true }
```

If that feels a bit simplistic, you can adjust this rule to capture only certain types of inputs. For example, in this case we only want to capture evaluations that returned in an empty list for `deny` reasons (e.g. with a [plan](terraform-plan-policy.md) or [task](task-run-policy.md) policy):

```opa
sample { count(deny) == 0 }
```

You can also sample a certain percentage of policy evaluations. Given that we don't generally allow nondeterministic evaluations, you'd need to depend on a source of randomness internal to the input. In this example, we will use the timestamp turned into milliseconds from nanoseconds to get a better spread. We'll also sample every 10th evaluation:

```opa
sample {
  millis := round(input.spacelift.request.timestamp_ns / 1e6)
  millis % 100 <= 10
}
```

### Why sample?

Capturing all evaluations sounds tempting, but it will also be extremely messy. Spacelift only shows the **100 most recent evaluations from the past 7 days**. If you capture everything, the most valuable samples can be drowned by irrelevant or uninteresting ones. Also, sampling adds a smaller performance penalty to your operations.

### Policy workbench in practice

To show you how to work with the policy workbench, we are going to use a [task policy](task-run-policy.md) that allowlists just two tasks: an innocent `ls`, and tainting a particular resource. It also only samples successful evaluations, where the list of `deny` reasons is empty.

!!! info
    This example comes from our [test Terraform repo](https://github.com/spacelift-io/terraform-starter){: rel="nofollow"}, which gives you hands-on experience with most Spacelift functionalities within 10-15 minutes.

1. On the _Enforce Guardrails_ > _Policies_ tab, click the name of the policy to edit in the workbench.
2. Click **Show simulation panel** on the right-hand side of the screen.
    ![Show simulation panel button](<../../assets/screenshots/Simulation-panel.png>)
3. If your policy has been evaluated and sampled, you will see the policy body on the left-hand side of the screen and a dropdown with timestamped evaluations (inputs) on the right-hand side. The evaluations are color-coded based on their outcomes.
    ![See previous inputs](<../../assets/screenshots/Simulation-panel2.png>)
4. Select one of the inputs in the dropdown, then click **Simulate**.
    ![Simulate an input](<../../assets/screenshots/Simulation-panel3.png>)
5. While running simulations, you can modify both the input and the policy body. If you change the policy body, or select an input that was evaluated using a different policy version, a warning will appear:
    ![Simulation change warning](<../../assets/screenshots/Simulation-change1.png>)
6. Click **Show changes** in the warning to view the exact differences between the policy body in the editor and the one used for the selected input.
    ![Show changes](<../../assets/screenshots/Simulation-change2.png>)
7. When you are satisfied with your updated policy, click **Save changes** so future evaluations use the new policy body.

### Filtering samples

The samples view offers powerful filtering options to help you quickly locate relevant samples. You can filter samples by:

- Stack name
- Outcome
- Pull request ID
- Push branch
- Stack repository

![Samples view](<../../assets/screenshots/policy-samples.png>)

Once you have identified the sample you want, click the three dots beside its outcome and select **Use to simulate** to run a simulation with that sample.

### Is policy sampling safe?

Policy sampling is perfectly safe. Session data may contain some personal information like username, name, and IP, but that data is only persisted for 7 days. Most importantly, in [plan policies](terraform-plan-policy.md), the inputs hash all the string attributes of resources, ensuring that no sensitive data leaks through this means.

Last but not least, the policy workbench (including access to previous inputs) is only available to **Spacelift account administrators**.

## Policy library

OPA can be difficult to learn, especially if you are just starting out with it. [The policy workbench](#policy-workbench) is great for helping you get policies right, but with the policy library, we take it up a notch.

The policy library gives you the ability to import templates as regular policies, directly inside your Spacelift account, that can be easily modified to meet your needs.

On the _Enforce Guardrails_ > _Policies_ tab in Spacelift, you will see a new section: **Templates**.

![Templates section](<../../assets/screenshots/policy_library.png>)

You can filter the policies based on the policy type or labels. There are examples available for all supported policy types.

### Import policy templates

1. When you find a policy template you would like to add to your account, click **Import**.
2. Edit policy details (optional):
    ![Create policy from import](<../../assets/screenshots/policy_library_drawer.png>)
      1. **Name**: Enter a descriptive name for the policy.
      2. **Type**: Ensure the policy type is correct.
      3. **Space**: Select the space to create the policy in.
      4. **Description** (optional): Enter a (markdown-supported) description for the policy.
      5. **Labels** (optional): Add labels to help sort and filter your policies. You can use `autoattach:label` to attach the policy to stacks or modules with the chosen `label` automatically.
3. Click **Continue** to edit the policy.
    ![Edit policy body](<../../assets/screenshots/policy_library_policy_edit.png>)
      - You'll see an example policy body based on the type you chose. Remove the comments from any rules you'd like to apply and add or change rules as needed.
4. Click **Create policy**. You can always edit policies as needed.

## Testing policies

!!! info
    We invite you to play around with policy examples and inputs [in the Rego playground](https://play.openpolicyagent.org/){: rel="nofollow"}. However, this is not a replacement for proper unit testing.

The whole point of policy-as-code is being able to handle it as code, which involves testing. Testing policies is crucial to make sure they aren't allowing unauthorized actions or too restrictive.

Spacelift uses a well-documented and well-supported open-source language, [Rego](#policy-language), which has built-in support for testing. Testing Rego is extensively covered in [their documentation](https://www.openpolicyagent.org/docs/latest/policy-testing/){: rel="nofollow"} so in this section we'll only look at things specific to Spacelift.

Let's define a simple [login policy](login-policy.md) that denies access to [non-members](login-policy.md#restricting-access-in-specific-circumstances), and write a test for it:

```opa title="deny-non-members.rego"
package spacelift

deny { not input.session.member }
```

You'll see that we simply mock out the `input` received by the policy:

```opa title="deny-non-members_test.rego"
package spacelift

test_non_member {
    deny with input as { "session": { "member": false } }
}

test_member_not_denied {
    not deny with input as { "session": { "member": true } }
}
```

We can then test it in the console using `opa test` command (note the glob, which captures both the source and its associated test):

```bash
❯ opa test deny-non-members*
PASS: 2/2
```

Testing policies that provide feedback to the users is only slightly more complex. Instead of checking for boolean values, you'll be testing for set equality. Let's define a simple [run initialization policy](run-initialization-policy.md) that **denies commits** to a particular branch:

```opa title="deny-sandbox.rego"
package spacelift

deny[sprintf("don't push to %s", [branch])] {
  branch := input.commit.branch
  branch == "sandbox"
}
```

In the test, we will check that the set return by the **deny** rule either has the expected element for the matching input, or is empty for non-matching one:

```opa title="deny-sandbox_test.rego"
package spacelift

test_sandbox_denied {
  expected := { "don't push to sandbox" }

  deny == expected with input as { "commit": { "branch": "sandbox" } }
}

test_master_not_denied {
  expected := set()

  deny == expected with input as { "commit": { "branch": "master" } }
}
```

Again, we can test the policy in the console using `opa test` (note the glob, which captures both the source and its associated test):

```bash
❯ opa test deny-sandbox*
PASS: 2/2
```

!!! tip
    We suggest you always unit test your policies and apply the same continuous integration principles as with your application code. You can set up a CI project using your vendor of choice for the same repository that's linked to the Spacelift project that's defining those policies, to get an external validation.

## Policy flags

By default, each policy is completely self-contained and does not depend on the result of previous policies. However, there are some situations where you want to introduce a chain of policies passing data to one another.

Different types of policies have access to different types of data required to make a decision, and you can use policy flags to pass that data between them.

Say you have a [push policy](./push-policy/README.md) with access to the list of files affected by a push or a PR event. You want to introduce a form of ownership control, where changes to different files need approval from different users. For example, a change in the `network` directory may require approval from the network team, while a change in the `database` directory needs an approval from the DBAs.

Approvals are handled by an [approval policy](./approval-policy.md) but it doesn't retain access to the list of affected files you need. This is where policy flags come in: set arbitrary review flags on the run in the push policy. This can be a separate push policy as in this example, or part of one of your pre-existing push policies. For simplicity, our example will only focus on `network`.

```rego title="flag_for_review.rego"
package spacelift

network_review_flag = "review:network"

flag[network_review_flag] {
  startswith(input.push.affected_files[_], "network/")
}

flag[network_review_flag] {
  startswith(input.pull_request.diff[_], "network/*")
}
```

Now, we can introduce a network approval policy using this flag.

```rego title="network-review.rego"
package spacelift

network_review_required {
  input.run.flags[_] == "review:network"
}

approve { not network_review_required }
approve {
  input.reviews.current.approvals[_].session.teams[_] == "DBA"
}
```

There are a few things worth knowing about flags:

- They are **arbitrary strings** and Spacelift makes no assumptions about their format or content.
- They can be **reset** by policies that set them (see [policy flag reset](policy-flag-reset.md) for details).
- They are **passed between policy types**. If you have multiple policies of the same type, they will not be able to see each other's flags.
- They can be set by any policies that explicitly **touch a run**: [push](./push-policy/README.md), [approval](./approval-policy.md), [plan](./terraform-plan-policy.md) and [trigger](./trigger-policy.md).
- They are always accessible through `run`'s `flags` property whenever the `run` resource is present in the input document.

Flags are shown in the Spacelift GUI, so even if you're not using them to explicitly pass the data between different types of policies, they can still be useful for debugging purposes. Here's an example of an approval policy exposing decision-making details:

![Approval policy with flags](<../../assets/screenshots/policy_flags_gui_example.png>)

## Backwards-compatibility

Policies, like the rest of Spacelift functionality, are generally kept fully backwards-compatible. Input fields of policies aren't removed and existing policy "invocation sites" are kept in place.

Occasionally policies might be deprecated, and once unused, disabled, but this is a process in which we work very closely with any affected users to make sure they have ample time to migrate and aren't negatively affected.

However, we do reserve the right to add new fields to policy inputs and introduce additional invocation sites. For example, we could introduce a new input event type to the push policy, and existing push policies will start getting those events. Thus, users are expected to write their policies in a way that new input types are handled gracefully, by checking for the event type in their rules.

For example, in a push policy, you might write a rule as follows:

```rego title="backwards-compatibility.rego"
track {
  not is_null(input.pull_request)
  input.pull_request.labels[_] == "deploy"
}
```

As you can see, the first line in the `track` rule makes sure that we only respond to events that contain the `pull_request`j field.
