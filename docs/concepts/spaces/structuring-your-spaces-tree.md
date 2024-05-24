# Structuring your Spaces Tree

Based on experience with other tools, a first intuition might be to structure your spaces team-first or service-first. Something akin to the following picture:

![](../../assets/screenshots/spaces_tree_structure_1.png)

However, there are likely Spacelift resources you will want to reuse across all development environment services, not across all environments for a single service. For example, a [Worker Pool](../worker-pools). That is because resources like Worker Pools are usually shared across security domains, not logical domains.

Due to this an architecture akin to the following is more advisable:

![](../../assets/screenshots/spaces_tree_structure_2.png)

This way you can create your Worker Pools, Contexts and Policies in the `dev`, `preprod`, and `prod` spaces, and then reuse them in all spaces below those.
