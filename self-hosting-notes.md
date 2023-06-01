# Self-Hosting Docs Proposal Notes

Just temporarily creating this page to note down how the self-hosting docs can integrate, and how the process would work.

## MkDocs Plugins

The suggested approach uses the following MkDocs plugins:

- [mkdocs-monorepo-plugin](https://github.com/backstage/mkdocs-monorepo-plugin) - allows us to combine multiple MkDocs sites into a single one.
- [mkdocs_macros_plugin](https://github.com/fralau/mkdocs_macros_plugin) - allows us to conditionally show certain blocks.

## Repo Structure

With this suggested solution, we'll create a new `self-hosting` folder within the repo. This folder will contain a subfolder for each version of self-hosting. The structure will look like this:

```text
docs/
  README.md
  ...
self-hosting/
  v0.0.6/
    docs/
    mkdocs.yaml
    nav.yaml
  v0.0.7/
  v0.0.8/
  ...
mkdocs.yaml
nav.yaml
```

When we want to create a new version of the self-hosting docs, we'll make a copy of the `docs` folder along with any other required file from the root of the repo, and create a new `self-hosting/vx.y.z` folder with these contents.

This means that:

- Changes to the docs will work exactly as they do just now. We'll make changes to the files in the `docs` folder, and ignore the `self-hosting` folder.
- The caveat to that is if we need to fix the docs in a previous version. In that case we'll make the fix in `self-hosting/vx.y.z`.
- It works locally with `mkdocs serve`.
- It should work with the same deployment process.

## Suggested Workflow

- We make changes to the docs as normal - fixing issues or documenting new features.
- When adding new features, if they are only applicable to SaaS, we either don't add the new page to the navigation for self-hosting, or we conditionally hide sections of the documentation using macros. See [conditional content](#conditional-content) for more details.
- When we want to create a new self-hosting release, we'll run a script (e.g. `create-self-hosting-release v0.0.9` which will create a new folder under the `self-hosting` directory).

## Conditional Content

### Pages



### Sections within Pages

To conditionally display content within pages, we can use [jinja templating](https://jinja.palletsprojects.com/en/3.1.x/templates). There are two macros defined in the [main.py](main.py) file that help us figure out whether the context of the page is self-hosting or SaaS:

- `is_self_hosting`
- `is_saas`

These macros check whether the current page being rendered is within the `self-hosting` directory or not.

The following shows an example of using them in a page:

```markdown
# Worker pools

{% if is_saas() %}

By default, Spacelift uses a managed worker pool hosted and operated by us. This is very convenient, but often you may have special requirements regarding infrastructure, security or compliance, which aren't served by the public worker pool. This is why Spacelift also supports private worker pools, which you can use to host the workers which execute Spacelift workflows on your end.

{% endif %}

In order to enjoy the maximum level of flexibility and security with a private worker pool, temporary run state is encrypted end-to-end, so only the workers in your worker pool can look inside it. We use asymmetric encryption to achieve this and only you ever have access to the private key.
```
