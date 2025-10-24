# Spacelift User Documentation Contributing Guide

In this guide you will get an overview of the contribution workflow from opening an issue, creating a pull request, to having it reviewed, merged and deployed.

We welcome all contributions, no matter the size or complexity. Every contribution helps and is appreciated.

The following is a set of guidelines for contributing to the Spacelift User Documentation. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## Reporting an Issue

If you spot a problem with the documentation (typo, missing or outdated information, broken example, etc.), [search if an issue already exists](https://github.com/spacelift-io/user-documentation/issues). If a related issue doesn't exist, please open a new issue using [the issue form](https://github.com/spacelift-io/user-documentation/issues/new).

## Making Changes

The Spacelift User Documentation uses [MkDocs](https://www.mkdocs.org/), a static website generator, with the [Material](https://squidfunk.github.io/mkdocs-material/) theme. The content is written as [Markdown](https://www.markdownguide.org/).

### Editing the Content

The content is stored in the `docs`folder as Markdown files. To edit content, just open the Markdown file in your favorite editor. If you need to add a new page, make sure to add it to the `nav.yaml` file.

Screenshots should be added to the `docs/assets/screenshots` folder.

### Modifying the Look and Feel

To tweak the look and feel of the user documentation, you can:

- Edit [MkDocs](https://www.mkdocs.org/user-guide/configuration/) and [Material](https://squidfunk.github.io/mkdocs-material/setup/changing-the-colors/) settings in the `mkdocs.yaml` file.
- Edit the CSS selectors in the `docs/assets/css/custom.css` file.
- Edit the images in the `docs/assets/images` folder.
- Edit the [theme templates](https://squidfunk.github.io/mkdocs-material/customization/#extending-the-theme) in the `overrides`folder.

## Previewing Changes

You can preview changes locally by running `mkdocs serve`. You can use the following command to run this inside a Docker container:

```shell
make run
```

> 💡 These commands are [set up](.vscode/tasks.json) as [VS Code tasks](https://code.visualstudio.com/docs/editor/tasks), so you can just run them from the VS Code command palette. Or even better: download the [Task Explorer](https://marketplace.visualstudio.com/items?itemName=spmeesseman.vscode-taskexplorer) extension and you can run them from the sidebar.

<!-- markdownlint-disable-next-line MD034 -->
This command will generate the documentation and serve it at http://localhost:8000/ for SaaS and http://localhost:8001/ for Self-Hosted. The documentation automatically reloads when changes to the source files are detected.

## Validating Changes

There are [some tests to ensure the consistency and the quality](https://github.com/spacelift-io/user-documentation/blob/main/.pre-commit-config.yaml) of the user documentation.

You will need to install the git hook for [pre-commit](https://pre-commit.com/) on your local clone:

```shell
pre-commit install
```

From now on, when you create a new commit the tests will be run against the modified files.

You can also manually trigger the tests at any time by running:

```shell
pre-commit
```

> Tip: one of our precommit checks is `oxipng` which optimizes PNG images. If you don't want to use `pre-commit` locally, you can optimize your PNG images with `docker run --rm -it -v $(PWD):/workdir -w /workdir ghcr.io/shssoichiro/oxipng:v9.1.5 docs/assets/screenshots/<filename.png|jpg> --opt=4 --preserve --strip=safe`.

## Self-Hosted

Our self-hosted docs are built using a tool called [Mike](https://github.com/jimporter/mike). Mike allows us to snapshot multiple versions of the documentation in a separate Git branch. In our case this branch is called `self-hosted-releases-prod`.

You can mostly ignore this while editing the docs, although there are a few things worth understanding.

### Mike Version

Please use the development version of Mike. If you need to install Mike locally, you can use `pip install git+https://github.com/jimporter/mike.git`.

### Adding Pages to the Navigation

We have two navigation config files:

- [nav.yaml](nav.yaml) - contains the SaaS navigation.
- [nav.self-hosted.yaml](nav.self-hosted.yaml) - contains the Self-Hosted navigation.

In general you should make changes to both files, unless either of the following is true:

1. A page should only be displayed in the SaaS version - in that case just edit _nav.yaml_.
2. A page should only be displayed in the self-hosted version - in that case just edit _nav.self-hosted.yaml_.

### Conditional Content

To conditionally display content within pages, we can use [jinja templating](https://jinja.palletsprojects.com/en/3.1.x/templates). There are two macros defined in the [main.py](main.py) file that help us figure out whether the context of the page is self-hosted or SaaS:

- `is_self_hosted`
- `is_saas`

These macros use an environment variable called `SPACELIFT_DISTRIBUTION`, and if the site is built with this set to `SELF_HOSTED` the docs will be in "self-hosted mode".

The following shows an example of using them in a page:

```markdown
# Worker pools

{% if is_saas() %}

By default, Spacelift uses a managed worker pool hosted and operated by us. This is very convenient, but often you may have special requirements regarding infrastructure, security or compliance, which aren't served by the public worker pool. This is why Spacelift also supports private worker pools, which you can use to host the workers which execute Spacelift workflows on your end.

{% endif %}

In order to enjoy the maximum level of flexibility and security with a private worker pool, temporary run state is encrypted end-to-end, so only the workers in your worker pool can look inside it. We use asymmetric encryption to achieve this and only you ever have access to the private key.
```

### Marking Blocks as Raw

The jinja templating used by the macros plugin sometimes thinks that parts of our documentation are template expressions when they should just be treated as normal text. To fix this we just need to wrap the section in a `{% raw %}` block. Here's an example:

````markdown
{% raw %}

```yaml
inputs:
  - id: stack_name
    name: Stack name
stack:
  # Jinja would normally interpret the {{ inputs.stack_name }} block as a template.
  name: ${{ inputs.stack_name }}
  space: root
  vcs:
    branch: main
    repository: my-repository
    provider: GITHUB
  vendor:
    terraform:
      manage_state: true
      version: "1.3.0"
```

{% endraw %}
````

### Previewing Changes

When you open a PR against the repo, a Render preview will automatically be generated. This preview also includes the latest version of the self-hosted docs. This allows you to preview any changes you are making to the self-hosted docs.

If you would like to preview the self-hosted site locally, first fetch the `self-hosted-releases-prod` branch, which Mike uses to serve its content:

```shell
git fetch origin self-hosted-releases-prod
```

Next, use `mike serve` to preview the site:

```shell
mike serve --branch self-hosted-releases-prod
```

Or via Docker:

```shell
docker run --pull always --rm -it -p 8000:8000 -v ${PWD}:/docs python:$(cat .python-version | tr -d '\n')-alpine sh -c "apk add git && git config --global --add safe.directory /docs && pip install mkdocs && pip install -r /docs/requirements.txt && cd /docs && mike serve --branch self-hosted-releases-prod -a '0.0.0.0:8000'"
```

Once it is ready, you will need to go to '0.0.0.0:8000/latest/' instead of just '0.0.0.0:8000'.

## Submitting Changes

Once you are happy with your changes, just open a pull request and ask for a review from `@KiraLempereur-Spacelift` and `spacelift-io/solutions-engineering`.

By submitting a pull request for this project, you agree to license your contribution under the [MIT license](./LICENSE) to Spacelift.

## Deploying Changes

Changes are automatically deployed by GitHub Action when they are pushed to the `main` branch. It usually takes about a minute for changes to go live after the pull request has been merged.
