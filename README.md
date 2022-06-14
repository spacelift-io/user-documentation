# Spacelift User Documentation

## Architecture Overview

The Spacelift User Documentation uses [MkDocs](https://www.mkdocs.org), a static website generated, with the [Material](https://squidfunk.github.io/mkdocs-material/) theme. The content is written as [Markdown](https://daringfireball.net/projects/markdown/).

The generated HTML files as well as the assets (images, CSS, Javascript, etc.) are hosted in an AWS S3 bucket. An AWS CloudFront distribution serves those files.

## Contributing

The following is a set of guidelines for contributing to the Spacelift User Documentation. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

### Editing Content

The content is stored in the `docs`folder as Markdown files. To edit content, just open the Markdown file in your favorite editor. If you need to add a new page, make sure to add it to the `nav.yaml` file.

Screenshots should be added to the `docs/assets/screenshots` folder.

### Editing Look and Feel

To tweak the look and feel of the user documentation, you can:

- Edit MkDocs settings in the `mkdocs.yaml` file.
- Edit the CSS selectors in the `docs/assets/css/extra.css` file.
- Edit the images in the `docs/assets/images` folder.
- Edit the theme templates in the `overrides`folder.

### Previewing Changes

You can preview changes locally by running MkDocs in a Docker container:

```bash
# Intel/AMD CPU
docker run --pull always --rm -it -p 8000:8000 -v ${PWD}:/docs squidfunk/mkdocs-material

# Arm CPU
docker run --pull always --rm -it -p 8000:8000 -v ${PWD}:/docs ghcr.io/afritzler/mkdocs-material
```

<!-- markdownlint-disable-next-line MD034 -->
This command will generate the documentation and serve it at http://localhost:8000/.

The documentation automatically reloads when changes to the source files are detected.

### Validating Changes

There are some tests to ensure the consistency and the quality of the user documentation.

You will need to install the git hook for  [pre-commit](https://pre-commit.com) on your local clone:

```bash
pre-commit install
```

From now on, when you create a new commit the tests will be run against the modified files.

You can also manually trigger the tests at any time by running:

```bash
pre-commit
```

### Submitting Changes

Once you are happy with your changes, just open a pull request and ask for a review.

### Deploying Changes

Changes are automatically deployed by GitHub Action when they are pushed to the `main` branch. It usually takes about a minute for changes to go live after the pull request has been merged.

## External Resources

- [Markdown Guide](https://www.markdownguide.org)
