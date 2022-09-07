---
description: Take your Infrastructure as Code to the next level
---

# 👋 Hello, Spacelift!

Spacelift is a sophisticated, continuous integration and deployment (CI/CD) platform for _infrastructure-as-code,_ currently supporting [Terraform](https://www.terraform.io/){: rel="nofollow"}, [Pulumi](https://www.pulumi.com/){: rel="nofollow"}, [AWS CloudFormation](https://aws.amazon.com/cloudformation/){: rel="nofollow"}, and [Kubernetes](https://kubernetes.io/){: rel="nofollow"}. It's designed and implemented by long-time DevOps practitioners based on previous experience with large-scale installations - dozens of teams, hundreds of engineers, and tens of thousands of cloud resources.

At the same time, Spacelift is super easy to get started with - you can go from zero to fully managing your cloud resources within less than a minute, with no pre-requisites. It integrates nicely with the large players in the field - notably [GitHub](integrations/source-control/github.md) and [AWS](integrations/cloud-providers/aws.md).

If you're new to Spacelift, please spend some time browsing through the articles in the same order as they appear in the menu - start with the main concepts and follow with integrations. If you're more advanced, you can navigate directly to the article you need, or use the search feature to find a specific piece of information. If you still have questions, feel free to [reach out to us.](https://spacelift.io/contact)

## Do I need another CI/CD for my infrastructure?

Yes, we believe it's a good idea. While in an ideal world one CI system would be enough to cover all use cases, we don't live in an ideal world. Regular CI tools can get you started easily, but Terraform has a rather unusual execution model and a highly stateful nature. Also, mind the massive blast radius when things go wrong. We believe Spacelift offers a perfect blend of regular CI's versatility and methodological rigor of a specialized, security-conscious infrastructure tool - enough to give it a shot even if you're currently happy with your infra-as-code CI/CD setup.

In the following sections, we'll try to present the main challenges of running Terraform in a general purpose CI system, as well as show how Spacelift addresses those. At the end of the day, it's mostly about two things - collaboration and security.

### Collaboration

> Wait, aren't CIs built for collaboration?

Yes, assuming stateless tools and processes. Running stateless builds and tests is what regular CIs are exceptionally good at. But many of us have noticed that deployments are actually trickier to get right. And that's hardly a surprise. They're more stateful, they may depend on what's already running. Terraform and your infrastructure, in general, is an **extreme example of a stateful system**. It's so stateful that it actually has something called [**state**](https://www.terraform.io/docs/state/index.html){: rel="nofollow"} (see what we just did there?) as one of its core concepts.

CIs generally struggle with that. They don't really _understand_ the workflows they run, so they can't for example serialize certain types of jobs. Like `terraform apply`, which introduces actual changes to your infrastructure. As far as your CI system is concerned, running those in parallel is fair game. But what it does to Terraform is nothing short of a disaster - your state is confused and no longer represents any kind of reality. Untangling this mess can take forever.

> But you can add manual approval steps

Yes, you can. But the whole point of your CI/CD system is to automate your work. First of all, becoming a human semaphore for a software tool isn't the best use of a highly skilled and motivated professional. Also, over-reliance on humans to oversee software processes will inevitably lead to costly mistakes because we, humans, are infinitely more fallible than well-programmed machines. It's ultimately much cheaper to use the right tool for the job than turn yourself into a part of a tool.

> But you can do [state locking](https://www.terraform.io/docs/state/locking.html){: rel="nofollow"}!

Yup, we hear you. In theory, it's a great feature. In practice, it has its limitations. First, it's a massive pain when working as a team. Your CI won't serialize jobs that can write state, and state locking means that all but one of the parallel jobs will simply fail. It's a safe default, that's for sure, but not a great developer experience. And the more people work on your infrastructure, the more frustrating the process will become.

And that's just _applying_ changes. By default, running `terraform plan` locks the state, too. So you can't really run multiple CI jobs in parallel, even if they're only meant to preview changes, because each of them will attempt to lock the state. Yes, you can work around this by explicitly _not_ locking state in CI jobs that you know won't make any state changes, but at this point, you've already put so much work into creating a pipeline that's fragile at best and requires you to manually synchronize it.

And we haven't even discussed security yet.

### Security

Terraform is used to manage infrastructure, which normally requires credentials. Usually, very powerful credentials. Administrative credentials, sometimes. And these can do _a lot of damage_. The thing with CIs is that you need to provide those credentials statically, and once you do, there's no way you can control how they're used.

And that's what makes CIs powerful - after all, they let you run arbitrary code, normally based on some configuration file that you have checked in with your Terraform code. So, what's exactly stopping a prankster from adding `terraform destroy -auto-approve` as an extra CI step? Or printing out those credentials and using them to mine their crypto of choice?

> There are better ways to get fired.

...you'll say and we hear you. Those jobs _are_ audited after all. No, if we were disgruntled employees we'd never do something as stupid. We'd get an SSH session and leak those precious credentials this way. Since it's unlikely you rotate them every day, we'd take our sweet time before using them for our nefarious purposes. Which wouldn't be possible with Spacelift BTW, which generates [one-off temporary credentials](integrations/cloud-providers/aws.md) for major cloud providers.

> But nobody does that!

Yes, you don't hear many of those stories. Most mistakes happen to well-meaning people. But in the world of infrastructure, even the tiniest of mistakes can cause major outages - like that typo we once made in our DNS config. That's why Spacelift adds an extra layer of [policy](concepts/policy/README.md) that allows you to control - separately from your infrastructure project! - [what code can be executed](concepts/policy/run-initialization-policy.md), [what changes can be made](concepts/policy/terraform-plan-policy.md), [when and by whom](concepts/policy/stack-access-policy.md). This isn't only useful to protect yourself from the baddies, but allows you to implement an [automated code review pipeline](concepts/policy/terraform-plan-policy.md#automated-code-review).
