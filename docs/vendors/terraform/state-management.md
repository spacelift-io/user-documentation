# State management

For those of you who don't want to manage Terraform state, Spacelift offers an optional sophisticated state backend synchronized with the rest of the application to maximize security and convenience. The ability to have Spacelift manage the state for you is only available during [stack creation](../../concepts/stack/creating-a-stack.md#terraform).

As you can see, it's also possible to import an existing Terraform state at this point, which is useful for users who want to upgrade their previous Terraform workflow.

!!! info
    If you're using Spacelift to manage your stack, do not specify any [Terraform backend](https://www.terraform.io/docs/backends/index.html) whatsoever. The one-off config will be dynamically injected into every [run](../../concepts/run/) and [task](../../concepts/run/task.md).

## Do. Or do not. There is no try.

In this section we'd like to give you a few reasons why it could be useful to trust Spacelift to take care of your Terraform state. To keep things level, we'll also give you a few reasons no to.

### Do

1. It's **super simple** - just two clicks during stack setup. Otherwise there's nothing to set up on your end, so one fewer sensitive thing to worry about. Feel free to refer to [how it works on our end](state-management.md#how-it-works), but overall we believe it to be a rather sensible and secure setup, at least on par with anything you could set up on your end.\
   \

2. It's **protected against accidental or malicious access**. Again, you can refer to the more technical section on the inner workings of the state server, but the gist is that we're able to map state access and state changes to legitimate Spacelift runs, thus automatically blocking all other unauthorized traffic. As far as we know, no other backend is capable of that, which is one more reason to give us a go.

### Don't

1. Unless you explicitly export it using a Spacelift [task](../../concepts/run/task.md), the **state can't be accessed outside** authorized [runs](../../concepts/run/) and [tasks](../../concepts/run/task.md). In particular, this makes sharing the state between stacks impossible using the Terraform mechanism of [remote state](https://www.terraform.io/docs/providers/terraform/d/remote_state.html). This is by design, and we believe that remote state is usually an anti-pattern, but hey, anti-patterns are sometimes super useful too. We offer an attractive alternative with [contexts](../../concepts/configuration/context.md) but if you **can't avoid accessing remote state**, you're better off managing the state on your end.\

2. We'll let you in on a little secret now - behind the pixie dust it's still S3 all the way down, and at this stage [we store all our data in Ireland](../../product/security.md). If you're not OK with that, you're better off managing the state on your end.\

3. If you want to **frequently access your state offline** for analytical or compliance purposes and aren't happy doing it using Spacelift [tasks](../../concepts/run/task.md) (BTW, let us know why) then again you're better off managing the state on your end.

## How it works

S3, like half of the Internet. The pixie dust we're adding on top of it involves generating one-off credentials for every [run](../../concepts/run/) and [task](../../concepts/run/task.md) and injecting them directly into the root of your Terraform project as a `.tf` file.

!!! warning
    If you have some Terraform state backend already specified in your code, the initialization phase will keep failing until you remove it.

The state server is an HTTP endpoint implementing the Terraform [standard state management protocol](https://www.terraform.io/docs/backends/types/http.html). Our backend always ensures that the credentials belong to one of the runs or tasks that are currently marked as active on our end, and their state indicates that they should be accessing or modifying the state. Once this is established, we just pass the request to S3 with the right parameters.

## Importing resources into your Terraform State

So you have an existing resource that was created by other means and would like that resource to be reflected in your terraform state. This is an excellent use case for the [terraform import](https://www.terraform.io/cli/import) command. When you're managing your own terraform state, you would typically run this command locally to import said resource(s) to your state file, but what do I do when I'm using Spacelift-managed state you might ask? Spacelift [Task](https://docs.spacelift.io/concepts/run/task) to the rescue!

To do this, use the following steps:

- Select the Spacelift Stack to which you would like to import state for.
- Within the navigation, select "Tasks"

![](<../../assets/screenshots/Screen Shot 2022-02-15 at 10.25.20 AM.png>)

- Run the `terraform import` command needed to import your state file to the Spacelift-managed state by typing the command into the text input and clicking the perform button. Note: If you are using Terragrunt on Spacelift, you will need to run `terragrunt import`

![](<../../assets/screenshots/Screen Shot 2022-02-15 at 1.05.23 PM.png>)

- Follow the status of your task's execution to ensure it was executed successfully. When completed, you should see an output similar to the following within the "Performing" step of your task.

![](<../../assets/screenshots/Screen Shot 2022-02-15 at 1.31.29 PM.png>)
