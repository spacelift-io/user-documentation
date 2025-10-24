# Onboarding Best Practices

There are many ways to onboard new groups of users into Spacelift. Below are three different approaches you might take to help you get started.

!!! info "About Management Stacks"
    This guide uses the term "management stacks" to refer to stacks that create and configure other Spacelift resources. These stacks use [stack role attachments](../concepts/authorization/assigning-roles-stacks.md) to gain elevated permissions.

    Previously, these were called "administrative stacks" and used the now-deprecated [administrative](../concepts/stack/stack-settings.md#administrative) flag. If you're migrating from the administrative flag, see the [migration guide](../concepts/authorization/assigning-roles-stacks.md#migration-from-administrative-flag).

## The Onboarding and Stack Modules

Spacelift is API first, which means everything in Spacelift is able to be terraformed.
All the suggested approaches we list here will involve creating a module that will create the necessary resources for a group to be onboarded into Spacelift and a module that will create stacks inside the Space(s) that the group will be assigned to.

The module should, minimally, create the following resources:

- [Space(s)](../concepts/spaces/README.md) in Spacelift for the group to be assigned into.
    - It should also have an input to make the Space a child of another Space, if necessary.
- A [Login Policy](../concepts/policy/login-policy.md) that allows the group to log into the Space.
    - You may need to [enable the login policy strategy](../concepts/user-management/admin.md#select-your-management-strategy) in your organization settings.
- A [Cloud Integration](../integrations/cloud-providers/README.md) that allows the group to connect to their cloud provider, in their specific cloud account.
- Global [Plan Policies](../concepts/policy/terraform-plan-policy.md) to enforce organization-wide policies.
- A [Management stack with Space admin role](../concepts/authorization/assigning-roles-stacks.md) at the top level of the Space(s) to be created
    - This stack should have the Space admin role attached to its own space
    - It potentially could create a code path in git for the group to use, that the management stack is pointed at.
    - See [Stack Role Attachments](../concepts/authorization/assigning-roles-stacks.md#assign-roles-to-stacks) for setup instructions

## Approach 1: Segregated Management Stacks

This approach involves creating a separate Spacelift management stack for each group of users.
When a group is ready to be onboarded, they will add a reference to the "Onboarding Module" in their parents stack, commit it to git, and allow Spacelift to create all the necessary resources.

Imagine you currently have a structure like this:

```text
root
├── Management (Stack)
├── Team A (Space)
└── Team B (Space)
    ├── Management (Stack)
    └── Cloud Operations (Space)
        ├── Management (Stack)
        ├── Dev (Space)
        ├── Test (Space)
        └── Prod (Space)
```

Now, imagine, you're onboarding an application team, under `Team B`, called `App Team` that is a sibling of `Cloud Operations`.
This is a two-step process, the first step is to call the "Onboarding Module" in the `root` Administrative stack.
You do this in the root, because Spaces _must_ be created at the root level.
After that point, the spaces would look like this:

```text
root
├── Management (Stack)
├── Team A (Space)
└── Team B (Space)
    ├── Management (Stack)
    ├── Cloud Operations (Space)
    │   ├── Management (Stack)
    │   ├── Dev (Space)
    │   ├── Test (Space)
    │   └── Prod (Space)
    └── App Team (Space)
        ├── Management (Stack)
        ├── Dev (Space)
        ├── Test (Space)
        └── Prod (Space)
```

From here step 2 of the process is the App team can use the management stack with [Space dmin role](../concepts/authorization/assigning-roles-stacks.md) in their space to create their own stacks using the stack module, and manage their own resources.
Note that the App team's management stack can also be used to create additional cloud integrations, contexts, etc.
Your organization could also have dedicated modules for these resources.

!!! info "Setting up role attachments"
    For each management stack in this approach, attach the Space admin role to the stack using its own space as the binding space.

    ```hcl
    data "spacelift_role" "space_admin" {
      slug = "space-admin"
    }

    resource "spacelift_role_attachment" "management_stack" {
      stack_id = spacelift_stack.management.id
      space_id = spacelift_stack.management.space_id
      role_id  = data.spacelift_role.space_admin.id
    }
    ```

## Approach 2: Universal Management Stack

This approach is similar to the Segregated Management Stacks approach, but instead of creating a separate management stack for each group, you create a single management stack that can be used by all groups.
This generally works better for smaller organizations that may not need to have a separate management stack for each group.
The benefit of this approach is that Spacelift's configuration all lives in one place.
Your "Onboarding" and "Stack" modules could even be one and the same.

Imagine you currently have a structure like this:

```text
root
├── Management (Stack)
├── Team A (Space)
└── Team B (Space)
    └── Cloud Operations (Space)
        ├── Dev (Space)
        ├── Test (Space)
        └── Prod (Space)
```

Now, imagine, you're onboarding an application team, under `Team B`, called `App Team` that is a sibling of `Cloud Operations`.
To do this, someone in your organization could call the "Onboarding Module" in the `root` Administrative stack to create all the resources necessary.
Once the commit in git is called, your organization would have a structure like this:

```text
root
├── Management (Stack)
├── Team A (Space)
└── Team B (Space)
    ├── Cloud Operations (Space)
    │   ├── Dev (Space)
    │   ├── Test (Space)
    │   └── Prod (Space)
    └── App Team (Space)
        ├── Dev (Space)
        ├── Test (Space)
        └── Prod (Space)
```

Moving forward, all teams would work out of the management stack with Space admin role in the `root` space.

!!! info "Setting up role attachments"
    For the universal management stack, attach the Space admin role to the root space (or the highest-level space your organization uses). This allows the stack to manage resources across all child spaces.

    ```hcl
    data "spacelift_role" "space_admin" {
      slug = "space-admin"
    }

    resource "spacelift_role_attachment" "universal_management" {
      stack_id = spacelift_stack.universal_management.id
      space_id = "root"  # or your organization's top-level space
      role_id  = data.spacelift_role.space_admin.id
    }
    ```

!!! warning
    Attaching roles to the root space affects **all spaces** in your account. Use this approach with caution and ensure proper security reviews.

## Approach 3: Blueprints

Spacelift will always suggest keeping your organization's Spacelift configuration in code at all times.
This is the most flexible and scalable way to manage your Spacelift configuration.
This means, when you use the Blueprints approach, we suggest your organization chooses between Approach 1 or Approach 2, and then creates a blueprint for the onboarding process.
The blueprint would then create commits in git adding terraform code to repositories controlled via Approach 1/2.

The process of this would be as follows (for simplicity, we will choose approach 2):

1. A team in your organization wants to be onboarded to use Spacelift
2. And administrator in your organization would go to the blueprint, fill out details similar to: `team_name`, `team_email`, `team_github_repo`, `space_path` etc.
3. The blueprint would then create a commit in the root management stack's code, creating a new `.tf` file that would call the "Onboarding Module" with the details filled out in the blueprint.
4. The management stack would then trigger a run, creating all the necessary resources for the team to be onboarded.
5. The team is now onboarded and can begin using Spacelift.

You can also add a `delete` schedule to the blueprint with `delete_resources` set to `false` so the resulting blueprint stack is cleaned up after the onboarding process is complete and management of the space can happen in the management stack moving forward.
