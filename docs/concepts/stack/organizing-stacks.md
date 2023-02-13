# Organizing stacks

Depending on the complexity of your infrastructure, the size of your team, your particular needs and your preferred way of working you may end up managing a lot of stacks. This obviously makes it harder to quickly find what you're looking for. As practitioners ourselves, we're providing you a few tools to make this process more manageable - from the basic [query-based searching](organizing-stacks.md#query-based-searching-and-filtering) to [filtering by status](organizing-stacks.md#label-based-folders) and the coolest of all, [label-based folders](organizing-stacks.md#label-based-folders).

## Video Walkthrough

<div style="padding:56.25% 0 0 0;position:relative;"><iframe src="https://player.vimeo.com/video/754795106?h=c4e1f101d8&amp;badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen style="position:absolute;top:0;left:0;width:100%;height:100%;" title="Organizing a Stack"></iframe></div><script src="https://player.vimeo.com/api/player.js"></script>

## Query-based searching and filtering

Historically the first tool we offered was the search bar:

![](../../assets/screenshots/Screen Shot 2022-06-29 at 3.06.42 PM.png)

The search bar allows you to search and filter by the following stack properties:

- name;
- ID (slug);
- any of its [labels](stack-settings.md#labels);

Note how the search phrase is highlighted, and irrelevant stacks are filtered out:

![](<../../assets/screenshots/Screen Shot 2022-06-29 at 3.07.29 PM.png>)

## Filtering by status

Filtering stacks by status is a very useful mechanism for identifying action items like plans pending confirmation ([unconfirmed](../run/tracked.md#unconfirmed) state) or [failed](../run/README.md#failed) jobs that require fixing. For that, use the _Filter stacks by status_ section on the sidebar to the left. If you click on any of the statuses, the list of stacks will be filtered to only include stacks with a given status:

![](<../../assets/screenshots/Screen Shot 2022-06-29 at 3.09.29 PM.png>)

Note that if no stacks in the account have a particular status at the moment, that status is missing from the list.

## Label-based folders

Probably the most useful way of grouping stacks is by attaching folder labels to them. You can read more about [labels](stack-settings.md#labels) here, including how to set them, and folder labels are just regular labels, prefixed with `folder:`. In order to make it more obvious in the GUI and save some screen real estate, we replace the `folder:` prefix by the folder icon...

![](<../../assets/screenshots/Screen Shot 2022-06-29 at 5.21.20 PM.png>)

...but once you start editing labels, the magic is gone:

![](../../assets/screenshots/Screen Shot 2022-06-29 at 5.22.51 PM.png)

For every folder label, a sidebar section is included in the _Folders_ menu, allowing you to search by that label. The number to the right hand side indicates that number of stacks with that label:

![](<../../assets/screenshots/Screen Shot 2022-06-29 at 5.24.06 PM.png>)

### Nesting and multiple folder labels

Perhaps worth mentioning is the fact that folder labels can be nested, allowing you to create either hierarchies, or arbitrary classifications of your stacks.

Also, a single stack can have any number of folder labels set, in which case it belongs to all the collections. In that, folder labels are like labels in Gmail rather than directories in your filesystem.

## Saving filters in views

It is possible to save your filters with a Views Tab. In the Filters Tab, you can select all the filters that you would like to apply, go to the Views Tab, enter the name of the view and click Save. This view is now saved for this account. Next time you login, it is possible to quickly navigate to the saved view.

![](<../../assets/screenshots/saved-filters.png>)

Views can be shared or private. While first creating the view, it is available only for your user. You can make it public for all the users of the account by hovering over the saved view and clicking small eye icon "Share within account". This way all the users within this application can see the saved view and who created it.

If you want to quickly reset the filter to the default state, click "Default" view that is pinned on top of the views created by you. It is also possible to delete the saved view by hovering it and then clicking small red bin icon "Delete filter".