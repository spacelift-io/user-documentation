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
- Edit the CSS selectors in the `docs/assets/css/extra.css` file.
- Edit the images in the `docs/assets/images` folder.
- Edit the [theme templates](https://squidfunk.github.io/mkdocs-material/customization/#extending-the-theme) in the `overrides`folder.

## Previewing Changes

You can preview changes locally by running MkDocs in a Docker container:

```shell
# Intel/AMD CPU
docker run --pull always --rm -it -p 8000:8000 -v ${PWD}:/docs squidfunk/mkdocs-material:$(awk -F '==' '/mkdocs-material/{print $NF}' requirements.txt)

# Arm CPU
docker run --pull always --rm -it -p 8000:8000 -v ${PWD}:/docs ghcr.io/afritzler/mkdocs-material:$(awk -F '==' '/mkdocs-material/{print $NF}' requirements.txt)
```

<!-- markdownlint-disable-next-line MD034 -->
This command will generate the documentation and serve it at http://localhost:8000/. The documentation automatically reloads when changes to the source files are detected.

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

## Submitting Changes

Once you are happy with your changes, just open a pull request and ask for a review from `@spacelift-io/solutions-engineering`.

By submitting a pull request for this project, you agree to license your contribution under the [MIT license](./LICENSE) to Spacelift.

## Deploying Changes

Changes are automatically deployed by GitHub Action when they are pushed to the `main` branch. It usually takes about a minute for changes to go live after the pull request has been merged.
