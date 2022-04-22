# Policy

## Introduction

Policy-as-code is the idea of expressing rules using a high-level programming language and treating them as you normally treat code, which includes version control as well as continuous integration and deployment. This approach extends the infrastructure-as-code approach to also cover the rules governing this infrastructure, and the platform that manages it.

Spacelift as a development platform is built around this concept and allows defining policies that involve various decision points in the application. User-defined policies can decide:

* Login: [who gets to log in](login-policy.md) to your Spacelift account and with what level of access;
* Access: [who gets to access individual Stacks](stack-access-policy.md) and with what level of access;
* Approval: [who can approve or reject a run](approval-policy.md) and how a run can be approved;
* Initialization: [which Runs and Tasks can be started](run-initialization-policy.md);
* Plan: [which changes can be applied](terraform-plan-policy.md);
* Push: [how Git push events are interpreted](git-push-policy.md);
* Task: [which one-off commands can be executed](task-run-policy.md);
* Trigger: [what happens when blocking runs terminate](trigger-policy.md);

You can refer to [this section](./#available-policies) to learn more about commonalities and differences between these policies, or to the dedicated article about each policy to dive deep into its details.

## How it works

Spacelift uses an open-source project called [**Open Policy Agent**](https://www.openpolicyagent.org) and its rule language, [**Rego**](https://www.openpolicyagent.org/docs/latest/policy-language/)**,** to execute user-defined pieces of code we call **Policies** at various decision points. Policies come in different flavors that we call **types**, with each type being executed at a different decision point.

You can think of policies as snippets of code that receive some JSON-formatted input and are allowed to produce some output in a predefined form. This input normally represents the data that should be enough to make some decision in its context. Each policy type exposes slightly different data, so please refer to their respective schemas for more information.

Except for [login policies](login-policy.md) that are global, all other policy types operate on the [stack](../stack/) level, and they can be attached to multiple stacks, just as [contexts](../configuration/context.md) are, which both facilitates code reuse and allows flexibility. Policies only affect stacks they're attached to. Please refer to the [relevant section of this article](./#attaching-policies) for more information about attaching policies.

Multiple policies of the same type can be attached to a single stack, in which case they are evaluated separately to avoid having their code (like local variables and helper rules) affect one another. However, once these policies are evaluated against the same input, their results are combined. So if you allow user login from one policy but deny it from another, the result will still be a denial.

### Policy language

[Rego](https://www.openpolicyagent.org/docs/latest/policy-language/) - the language that we're using to execute policies - is a very elegant, Turing incomplete data query language. It takes a few hours (tops) to get your head around all of its quirks but if you can handle SQL and the likes of [`jq`](https://stedolan.github.io/jq/), you'll find Rego pretty familiar. For each policy, we also give you plenty of examples that you can tweak to achieve your goals, and each of those examples comes with a link allowing you to execute it in [the Rego playground](https://play.openpolicyagent.org).

### Constraints

To keep policies functionally pure and relatively snappy, we disabled some Rego built-ins that can query external or runtime data. These are:

* `http.send`
* `opa.runtime`
* `rego.parse_module`
* `time.now_ns`
* `trace`

Disabling `time.now_ns` may seem surprising at first - after all, what's wrong with getting the current timestamp? Alas, depending on the current timestamp will make your policies impure and thus tricky to test - and we encourage you to [test your policies thoroughly](./#testing-policies)! You will notice though that the current timestamp in Rego-compatible form (Unix nanoseconds) is available as `request.timestamp_ns` in every policy payload, so please use it instead.

Policies must be self-contained and cannot refer to external resources (e.g., files in a VCS repository).

## Available policies

There are currently seven types of supported policies and while each of them is different, they have a lot in common. In particular, they can fall into one of the two groups based on what rules are expected to return.

[Login](login-policy.md) and [access](stack-access-policy.md) policies expect rules to return a **boolean value** (_true_ or _false_). Each type of policy defines its own set of rules corresponding to different access levels. In these cases, various types of rules can be positive or negative - that is, they can explicitly **allow** or **deny** access.

The second group of policies ([initialization](run-initialization-policy.md), [plan](terraform-plan-policy.md), and [task](task-run-policy.md)) is expected to generate a [**set of strings**](https://www.openpolicyagent.org/docs/latest/policy-language/#generating-sets) that serve as _direct feedback_ to the user. Those rules are generally negative in that they **can only block** certain actions - it's only their lack that counts as an implicit success.

Here's a practical difference between the two types:

**boolean.rego**
```opa
package spacelift

# This is a simple deny rule.
# When it matches, no feedback is provided.
deny {
  true
}
```

**string.rego**
```opa
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

| Type                                           | Purpose                                                                               | Types                 | Returns       | Rules                                              |
| ---------------------------------------------- | ------------------------------------------------------------------------------------- | --------------------- | ------------- | -------------------------------------------------- |
| [Login](login-policy.md)                       | Allow or deny login, grant admin access                                               | Positive and negative | `boolean`     | _allow, admin, deny, deny\_admin_                  |
| [Access](stack-access-policy.md)               | Grant or deny appropriate level of stack access                                       | Positive and negative | `boolean`     | _read, write, deny, deny\_write_                   |
| [Initialization](run-initialization-policy.md) | Blocks suspicious [runs](../run/) before they [start](../run/#initializing)           | Negative              | `set<string>` | _deny_                                             |
| [Plan](terraform-plan-policy.md)               | Gives feedback on [runs](../run/) after [planning](../run/proposed.md#planning) phase | Negative              | `set<string>` | _deny_, _warn_                                     |
| [Push](git-push-policy.md)                     | Determines how a Git push event is interpreted                                        | Positive and negative | `boolean`     | _track, propose, ignore, ignore\_track, notrigger_ |
| [Task](task-run-policy.md)                     | Blocks suspicious [tasks](../run/task.md) from running                                | Negative              | `set<string>` | _deny_                                             |
| [Trigger](trigger-policy.md)                   | Selects [stacks](../stack/) for which to trigger a [tracked run](../run/tracked.md)   | Positive              | `set<string>` | _trigger_                                          |

## Helper Functions

The following helper functions can be used in Spacelift policies:

| Name                     | Description                                                                                                                                                                            |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `output := sanitized(x)` | `output` is the string `x` sanitized using the same algorithm we use to sanitize secrets.                                                                                              |
| `result := exec(x)`      | Executes the command `x`. `result` is an object containing `status`, `stdout` and `stderr`. Only applicable for run initialization policies for [private workers](../worker-pools.md). |

## Creating policies

There are two ways of creating policies - through the web UI and through the [Terraform provider](../../vendors/terraform/terraform-provider.md). We generally suggest the latter as it's much easier to manage down the line and [allows proper unit testing](./#testing-policies). Here's how you'd define a plan policy in Terraform and attach it to a stack (also created here with minimal configuration for completeness):

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

On the other hand, if you want to create a policy in the UI, here's how you could go about that. **Note that you must be a Spacelift admin to manage policies**. First, go to the Policies screen in your account view, and click the _Add policy_ button:

![](../../assets/images/Policies_%C2%B7_spacelift-io%20%281%29.png)

This takes you to the policy creation screen where you can choose the type of policy you want to create, and edit its body. For each type of policy you're also given an explanation and a few examples. We'll be creating an [access policy](stack-access-policy.md) that gives members of the _Engineering_ GitHub team read access to a stack:

![](../../assets/images/New_policy_%C2%B7_spacelift-io%20%282%29.png)

Once you're done, click on the _Create policy_ button to save it. Don't worry, policy body is mutable so you'll always be able to edit it if need be.

## Attaching policies

### Automatically

Policies, with the exception of [Login policies](login-policy.md), can be automatically attached to stacks using the `autoattach:label` special label where `label` is the name of a label attached to stacks.

In the example below, the policy will be automatically attached to all the stacks with the label `production`.

![](../../assets/images/CleanShot%202022-03-10%20at%2016.03.48%402x.png)

### Manually

In the web UI attaching policies is done in the stack management view, in the Policies tab:

![](../../assets/images/Edit_stack_%C2%B7_We_test_in_prod.png)

We only have one policy, so let's select it and attach it:

![](../../assets/images/Edit_stack_%C2%B7_We_test_in_prod%20%281%29.png)

Cool, your policy is attached and from now on it will affect the stack. You can detach it from this view, too.

## Policy workbench

One thing we've noticed while working with policies in practice is that it takes a while to get them right. This is not only because the concept or the underlying language introduce a learning curve, but also because the feedback cycle can be slow: write a plan policy, make a code change, trigger a run, verify policy behavior... rinse and repeat. This can easily take hours.

Enter **policy workbench**. Policy workbench allows you to capture policy evaluation events so that you can adjust the policy independently and therefore shorten the entire cycle. In order to make use of the workbench, you will first need to [sample policy inputs](./#sampling-policy-inputs).

### Sampling policy inputs

Each of Spacelift's policies supports an additional boolean rule called `sample`. Returning `true` from this rule means that the input to the policy evaluation is captured, along with the policy body at the time and the exact result of the policy evaluation. You can for example just capture every evaluation with a simple:

```opa
sample { true }
```

If that feels a bit simplistic and spammy, you can adjust this rule to capture only certain types of inputs. For example, in this case we will only want to capture evaluations that returned in an empty least for `deny` reasons (eg. with a [plan](terraform-plan-policy.md) or [task](task-run-policy.md) policy):

```opa
sample { count(deny) == 0 }
```

You can also sample a certain percentage of policy evaluations. Given that we don't generally allow nondeterministic evaluations, you'd need to depend on a source of randomness internal to the input. In this example we will use the timestamp - note that since it's originally expressed in nanoseconds, we will turn it into milliseconds to get a better spread. We'll also want to sample every 10th evaluation:

```opa
sample {
  millis := round(input.request.timestamp_ns / 1e6)
  millis % 100 <= 10
}
```

### Why sample?

Capturing all evaluations sounds tempting but it will also be extremely messy. We're only showing **100 most recent evaluations from the past 7 days**, so if you capture everything then the most valuable samples can be drowned by irrelevant or uninteresting ones. Also, sampling adds a small performance penalty to your operations.

### Policy workbench in practice

In order to show you how to work with the policy workbench, we are going to use a [task policy](task-run-policy.md) that whitelists just two tasks - an innocent `ls`, and tainting a particular resource. It also only samples successful evaluations, where the list of `deny` reasons is empty:

!!! Info
    This example comes from our [test repo](https://github.com/spacelift-io/terraform-starter), which gives you hands-in experience with most Spacelift functionalities within 10-15 minutes, depending on whether you like to RTFM or not. We strongly recommend you give it a go.


![](../../assets/images/Allow_only_safe_commands_%C2%B7_marcinwyszynski.png)

In order to get to the policy workbench, first click on the Edit button in the upper right hand corner of the policy screen:

![](../../assets/images/Allow_only_safe_commands_%C2%B7_marcinwyszynski%20%281%29.png)

Then, click on the Show simulation panel link on the right hand side of the screen:

![](../../assets/images/Editing_Allow_only_safe_commands_%C2%B7_marcinwyszynski%20%281%29.png)

If your policy has been used evaluated and sampled, your screen should look something like this:

![](../../assets/images/Editing_Allow_only_safe_commands_%C2%B7_marcinwyszynski.png)

On the left hand side you have the policy body. On the right hand side there's a dropdown with timestamped evaluations (inputs) of this policy, color-coded for their ultimate outcome. Selecting one of the inputs allows you to simulate the evaluation:

![](../../assets/images/Editing_Allow_only_safe_commands_%C2%B7_marcinwyszynski%20%282%29.png)

While running simulations, you can edit both the input and the policy body. If you edit the policy body, or choose an input that has been evaluated with a different policy body, you will get a warning like this:

![](../../assets/images/Editing_Allow_only_safe_commands_%C2%B7_marcinwyszynski%20%283%29.png)

Clicking on the _Show changes_ link within that warning shows you the exact difference between the policy body in the editor panel, and the one used for evaluating the selected input:

![](../../assets/images/Editing_Allow_only_safe_commands_%C2%B7_marcinwyszynski%20%284%29.png)

Once you're happy with your new policy body, you can click on the _Save changes_ button to make sure that the new body is used for future evaluations.

### Is it safe?

Yes, policy sampling is perfectly safe. Session data may contain some personal information like username, name and IP, but that data is only persisted for 7 days. Most importantly, in [plan policies](terraform-plan-policy.md) the inputs hash all the string attributes of resources, ensuring that no sensitive data leaks through this means.

![](../../assets/images/Editing_Enforce_password_strength_%C2%B7_marcinwyszynski.png)

Last but not least, the policy workbench - including access to previous inputs - is only available to **Spacelift account administrators**.

## Testing policies

!!! Info
    In the examples for each type of policy we invite you to play around with the policy and its input [in the Rego playground](https://play.openpolicyagent.org). While certainly useful, we won't consider it proper unit testing.


The whole point of policy-as-code is being able to handle it as code, which involves everyone's favorite bit - testing. Testing policies is crucial because you don't want them accidentally allow the wrong crowd to do the wrong things.

Luckily, Spacelift uses a well-documented and well-supported open source language called Rego, which has built-in support for testing. Testing Rego is extensively covered in [their documentation](https://www.openpolicyagent.org/docs/latest/policy-testing/) so in this section we'll only look at things specific to Spacelift.

Let's define a simple [login policy](login-policy.md) that denies access to [non-members](login-policy.md#account-membership), and write a test for it:

**deny-non-members.rego**
```opa
package spacelift

deny { not input.session.member }
```

You'll see that we simply mock out the `input` received by the policy:

**deny-non-members_test.rego**
```opa
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

Testing policies that provide feedback to the users is only slightly more complex. Instead of checking for boolean values, you'll be testing for set equality. Let's define a simple [run initialization policy](run-initialization-policy.md) that denies commits to a particular branch (because why not):

**deny-sandbox.rego**
```opa
package spacelift

deny[sprintf("don't push to %s", [branch])] {
  branch := input.commit.branch
  branch == "sandbox"
}
```

In the respective test, we will check that the set return by the **deny** rule either has the expected element for the matching input, or is empty for non-matching one:

**deny-sandbox_test.rego**
```opa
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

Again, we can then test it in the console using `opa test` command (note the glob, which captures both the source and its associated test):

```bash
❯ opa test deny-sandbox*
PASS: 2/2
```

!!! Success
    We suggest you always unit test your policies and apply the same continuous integration principles as with your application code. You can set up a CI project using the vendor of your choice for the same repository that's linked to the Spacelift project that's defining those policies, to get an external validation.

