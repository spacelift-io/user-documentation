# Organize stacks

Depending on the complexity of your infrastructure, the size of your team, your particular needs, and your preferred way of working, you may end up managing a lot of stacks. Spacelift offers several options for searching through your stacks, from basic [query-based searching](organizing-stacks.md#query-based-search-and-filter) to [filtering by status](organizing-stacks.md#label-based-folders) and' [label-based folders](organizing-stacks.md#label-based-folders).

## Video Walkthrough

<div style="padding:56.25% 0 0 0;position:relative;"><iframe src="https://player.vimeo.com/video/754795106?h=c4e1f101d8&amp;badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen style="position:absolute;top:0;left:0;width:100%;height:100%;" title="Organizing a Stack"></iframe></div><script src="https://player.vimeo.com/api/player.js"></script>

## Customize your table view

You can customize the table view to suit your needs. Click the **Customize list** gear icon at the top-right to open a customizing drawer.

![Customize list icon](<../../assets/screenshots/stack/list/customize-list-button.png>)
![Customize list drawer](<../../assets/screenshots/stack/list/customize-list-drawer.png>)

1. Drag and drop columns to rearrange or hide them from view. The _name_ column cannot be hidden.
      - Alternatively, outside the customize list drawer, hover over the column header and click **Hide**.
       ![Hide column](<../../assets/screenshots/stack/list/column-options-highlight.png>)
2. To reset your settings, click **Reset to default** at the bottom of the customization drawer.

You can also resize columns in the list by dragging the separator:
![Column resize separator](<../../assets/screenshots/stack/list/resize-column-highlight.png>)

## Query-based search and filter

![Stacks list search](../../assets/screenshots/stack/list/search-highlight.png)

You can search and filter by these stack properties in the search bar:

- name
- ID (slug)
- any of its [labels](stack-settings.md#labels)

## Filter by state

Filtering stacks by state is useful for identifying action items like plans pending confirmation ([unconfirmed](../run/tracked.md#unconfirmed) state) or [failed](../run/README.md#failed) jobs that require fixing. Use the _State_ section on the left-hand sidebar, which displays all states attached to your stacks. Click state checkboxes to filter the list of stacks.

![Filter stacks in the list by state](<../../assets/screenshots/stack/list/finished-filter.png>)

You can also use our predefined tabs to filter some specific group of states:
![Predefined tabs](<../../assets/screenshots/stack/list/tab-filters-highlight.png>)

| **Predefined Tab Label** | **State** |
| -----------------------  | --------- |
| Needs Attention          | _unconfirmed_ |
| Failed                   | _failed_ |
| On Hold                  | _none_, _confirmed_, or _replan-requested_ |
| In Progress              | _applying_, _destroying_, _initializing_, _planning_, _preparing-apply_, or _preparing-replan_ |
| Finished                 | _finished_ |

## Label-based folders

You can group stacks by attaching folder labels to them, which are [regular labels](./stack-settings.md#labels) prefixed with `folder:`. In the stacks list, the `folder:` prefix is replaced width a folder icon.

![Folder icon for prefix](<../../assets/screenshots/stack/list/labels-folders-highlight.png>)

Your folder labels will appear in the _Folders_ section of the _Filters_ sidebar menu, allowing you to use the checkboxes to filter the list by folder labels.

![Filter by folder labels](<../../assets/screenshots/stack/list/folder-section-highlight.png>)

### Nesting and multiple folder labels

Folder labels can be nested, allowing you to create hierarchies or arbitrary classifications of your stacks.

A single stack can have _any number of folder labels_ set, in which case it belongs to **all** the collections. If you use more than one folder label on a single stack, they act more like labels in e-mail inboxes rather than directories in your filesystem.

## Save filters in views

You can save filter views to easily apply filters to your stacks list.

![Create filter view](<../../assets/screenshots/stack/list/saved-view-create-highlight.png>)

1. Select all filters you would like to apply.
2. If desired, add a search query or sorting option in the top-right.
3. Click **New View**, then enter a descriptive name for the filter view.
4. Check the box to set the new view as your default, if desired.
     - If you want to edit your default view, click **Views**, click the three dots beside the view name you want to use as default, then click **Use as your default view**.
     ![Set filter view as default](<../../assets/screenshots/stack/filter-views-default.png>)
5. Click **Save**.

If you set a filter view as your default, the next time you log in or navigate to the _Stacks_ tab, your personal default view will be applied.

### Shared views

Filter views can be private (default for new views) or public to all users of the account. To share a filter view, if you are an admin user, click the three dots beside the view name and click **Share within the account**. The view will now be visible for all users within the account.

### Reset to default view

To quickly reset your default view to Spacelift's default (no active filters):

1. Click **Views** to see your available filter views.
2. Click the three dots beside the view name you're using as default.
3. Click **Reset to Spacelift default view**.
4. All sorting, search, and filter parameters will be cleared.

![Reset filter view](<../../assets/screenshots/stack/filter-views-reset.png>)

### Manage view

Manage existing views when you click the three dots next to _New view_.

- Click **Update** to update your current filter view with any new filters, searches, and/or sorting settings.
- Click **Edit name** to change the name of the current filter view.
- Click **Delete** to remove a private view. If the view has been shared with other users on the account, it cannot be deleted.

![Manage view menu](../../assets/screenshots/stack/list/saved-view-manage-highlight.png)
