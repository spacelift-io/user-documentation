# Spacelift User Documentation

## Usage

- Amd64: `docker run --pull always --rm -it -p 8000:8000 -v ${PWD}:/docs squidfunk/mkdocs-material`
- Arm64: `docker run --pull always --rm -it -p 8000:8000 -v ${PWD}:/docs ghcr.io/afritzler/mkdocs-material`

## Checks

- Install [pre-commit](https://pre-commit.com/#installation)
- Install the git hook scripts: `pre-commit install`
