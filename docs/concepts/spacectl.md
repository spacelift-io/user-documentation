# `spacectl`, the Spacelift CLI

`spacectl` is a utility wrapping Spacelift's [GraphQL API](../integrations/api.md) for easy programmatic access in command-line contexts, either in manual interactive mode (in your local shell) or a predefined CI pipeline (GitHub actions, CircleCI, Jenkins, etc.).

Its primary purpose is to help you explore and execute actions inside Spacelift. It provides limited functionality for creating or editing resources. To do that programmatically, you can use the [Spacelift Terraform Provider](https://github.com/spacelift-io/terraform-provider-spacelift){: rel="nofollow"}.

## Installation

Official Spacelift-supported packages are maintained by [Spacelift](https://spacelift.io/){: rel="nofollow"} and are the preferred ways to install `spacectl`. We support:
<!-- markdownlint-disable MD051 -->
- [Homebrew](#homebrew)
- [Windows](#windows)
- [Docker image](#docker-image)
- [asdf](#asdf)
- [GitHub Release](#github-release)
- [GitHub Actions usage](#github-actions-usage)
<!-- markdownlint-enable MD051 -->
### Spacelift-supported packages

=== "Homebrew"
      You can install `spacectl` using Homebrew on MacOS or Linux:

      ```bash
      brew install spacelift-io/spacelift/spacectl
      ```

=== "Windows"
      You can install `spacectl` using winget:

      ```shell
      winget install spacectl
      ```

      or

      ```shell
      winget install --id spacelift-io.spacectl
      ```

=== "Docker image"
      `spacectl` is distributed as a Docker image, which can be used as follows:

      ```bash
      docker run -it --rm ghcr.io/spacelift-io/spacectl stack deploy --id my-infra-stack
      ```

      Add the [required environment variables](#authenticating-using-environment-variables) to authenticate.

=== "asdf"
      ```bash
      asdf plugin add spacectl
      asdf install spacectl latest
      asdf global spacectl latest
      ```

=== "GitHub Release"
      `spacectl` is distributed through GitHub Releases as a zip file containing a self-contained statically linked executable built from the source in this repository.

      Download binaries directly from the [Releases page](https://github.com/spacelift-io/spacectl/releases){: rel="nofollow"}.

=== "GitHub Actions usage"
      The [setup-spacectl](https://github.com/spacelift-io/setup-spacectl){: rel="nofollow"} GitHub Action can be used to install `spacectl`:

      {% raw %}

      ```yaml
      steps:
      - name: Install spacectl
         uses: spacelift-io/setup-spacectl@main

      - name: Deploy infrastructure
         env:
            SPACELIFT_API_KEY_ENDPOINT: https://mycorp.app.spacelift.io
            SPACELIFT_API_KEY_ID: ${{ secrets.SPACELIFT_API_KEY_ID }}
            SPACELIFT_API_KEY_SECRET: ${{ secrets.SPACELIFT_API_KEY_SECRET }}
         run: spacectl stack deploy --id my-infra-stack
      ```

      {% endraw %}

### Community-supported packages

Some packages are community-maintained and supported. Always verify package integrity yourself before using them to install or update `spacectl`. Community-supported packages include:
<!-- markdownlint-disable MD051 -->
- [Arch linux](#arch-linux)
- [Alpine linux](#alpine-linux)
<!-- markdownlint-enable MD051 -->
=== "Arch linux"
      Install [`spacectl-bin`](https://aur.archlinux.org/packages/spacectl-bin){: rel="nofollow"}: from the Arch User Repository ([AUR](https://aur.archlinux.org/){: rel="nofollow"}):

      ```bash
      yay -S spacectl-bin
      ```

      Verify the [`PKGBUILD`](https://aur.archlinux.org/cgit/aur.git/tree/PKGBUILD?h=spacectl-bin){: rel="nofollow"} before installing or updating.

=== "Alpine linux"
      Install [`spacectl`](https://pkgs.alpinelinux.org/packages?name=spacectl&branch=edge&repo=&arch=&maintainer=){: rel="nofollow"} from the Alpine Repository ([alpine packages](https://pkgs.alpinelinux.org/packages){: rel="nofollow"}):

      ```bash
      apk add spacectl --repository=https://dl-cdn.alpinelinux.org/alpine/edge/testing
      ```

      Verify the [`APKBUILD`](https://git.alpinelinux.org/aports/tree/testing/spacectl/APKBUILD){: rel="nofollow"} before installing or updating.

## Quick Start

1. Authenticate using `spacectl profile login` (option 3):

      ```bash
      > spacectl profile login my-account
      Enter Spacelift endpoint (eg. https://unicorn.app.spacelift.io/): http://my-account.app.spacelift.tf
      Select authentication flow:
      1) for API key,
      2) for GitHub access token,
      3) for login with a web browser
      Option: 3
      ```

2. Use spacectl:

      ```bash
      > spacectl stack list
      Name                          | Commit   | Author        | State     | Worker Pool | Locked By
      stack-1                       | 1aa0ef62 | Adam Connelly | NONE      |             |
      stack-2                       | 1aa0ef62 | Adam Connelly | DISCARDED |             |
      ```

## Getting help

To list all the commands available, use `spacectl help`:

```bash
> spacectl help
NAME:
   spacectl - Programmatic access to Spacelift GraphQL API.

USAGE:
   spacectl [global options] command [command options] [arguments...]

VERSION:
   0.26.0

COMMANDS:
   module                   Manage a Spacelift module
   profile                  Manage Spacelift profiles
   provider                 Manage a Terraform provider
   run-external-dependency  Manage Spacelift Run external dependencies
   stack                    Manage a Spacelift stack
   whoami                   Print out logged-in users information
   version                  Print out CLI version
   workerpool               Manages workerpools and their workers
   help, h                  Shows a list of commands or help for one command

GLOBAL OPTIONS:
   --help, -h     show help
   --version, -v  print the version
```

To get help about a particular command or subcommand, use the `-h` flag:

```bash
> spacectl profile -h
NAME:
   spacectl profile - Manage Spacelift profiles

USAGE:
   spacectl profile command [command options] [arguments...]

COMMANDS:
     current       Outputs your currently selected profile
     export-token  Prints the current token to stdout. In order not to leak, we suggest piping it to your OS pastebin
     list          List all your Spacelift account profiles
     login         Create a profile for a Spacelift account
     logout        Remove Spacelift credentials for an existing profile
     select        Select one of your Spacelift account profiles
     help, h       Shows a list of commands or help for one command

OPTIONS:
   --help, -h  show help (default: false)
```

## Usage example

In this example, `spacectl` runs a one-off task in Spacelift:

[![asciicast](https://asciinema.org/a/pYm8lqM5XTUoG1UsDo7OL6t8B.svg)](https://asciinema.org/a/pYm8lqM5XTUoG1UsDo7OL6t8B)

## Authentication

`spacectl` is designed to work in two different contexts:

- A non-interactive scripting mode (eg. external CI/CD pipeline).
- A local interactive mode, where you type commands into your shell.

Because of this, it supports two types of credentials: environment variables and user profiles.

### Authenticating using environment variables

The CLI supports the following authentication methods via the environment:

- [Spacelift API tokens](#spacelift-api-tokens).
- [GitHub tokens](#github-tokens).
- [Spacelift API keys](#spacelift-api-keys).

`spacectl` looks for authentication configurations in the order specified above, and will stop as soon as it finds a valid configuration. For example, if a Spacelift API token is specified, GitHub tokens and Spacelift API keys will be ignored, even if their environment variables are specified.

#### Spacelift API tokens

Spacelift API tokens can be specified using the `SPACELIFT_API_TOKEN` environment variable and contains all information needed to authenticate.

API tokens are generally short-lived and will need to be re-created often.

#### GitHub tokens

GitHub tokens are only available to accounts that use GitHub as their identity provider, but are very convenient for use in GitHub Actions. To use a GitHub token, set the following environment variables:

- `SPACELIFT_API_KEY_ENDPOINT`: The URL to your Spacelift account, for example `https://mycorp.app.spacelift.io`.
- `SPACELIFT_API_GITHUB_TOKEN`: A GitHub personal access token.

#### Spacelift API keys

To use a Spacelift API key, set the following environment variables:

- `SPACELIFT_API_KEY_ENDPOINT`: The URL to your Spacelift account, for example `https://mycorp.app.spacelift.io`.
- `SPACELIFT_API_KEY_ID`: The ID of your Spacelift API key. Available via the Spacelift application.
- `SPACELIFT_API_KEY_SECRET`: The secret for your API key. Only available when the secret is created.

More information about API authentication can be found at [our GraphQL API documentation](../integrations/api.md).

### Authenticating using account profiles

In order to make working with multiple Spacelift accounts easy in interactive scenarios, Spacelift supports account management through the `profile` family of commands:

```bash
❯ spacectl profile
NAME:
   spacectl profile - Manage Spacelift profiles

USAGE:
   spacectl profile command [command options] [arguments...]

COMMANDS:
     current       Outputs your currently selected profile
     export-token  Prints the current token to stdout. In order not to leak, we suggest piping it to your OS pastebin
     list          List all your Spacelift account profiles
     login         Create a profile for a Spacelift account
     logout        Remove Spacelift credentials for an existing profile
     select        Select one of your Spacelift account profiles
     help, h       Shows a list of commands or help for one command

OPTIONS:
   --help, -h  show help (default: false)
```

Each of the subcommands requires an account **alias**, which is a short, user-friendly name for each set of credentials (account profiles). Profiles don't need to be unique; you can have multiple sets of credentials for a single account too.

Account profiles support three authentication methods:

- GitHub access tokens.
- API keys.
- Login with a browser (API token).

Enter the following to authenticate to your first profile, replacing `${MY_ALIAS}` with the actual profile alias:

```bash
❯ spacectl profile login ${MY_ALIAS}
Enter Spacelift endpoint (eg. https://unicorn.app.spacelift.io/):
```

In the next step, you will be asked to choose which authentication method you are going to use. If your account is using [SAML-based SSO authentication](../integrations/single-sign-on/README.md), then API keys and login with a browser are your only options.

After you enter your credentials, the CLI will validate them against the server and, assuming they're valid, persist them in a credentials file in `.spacelift/${MY_ALIAS}`. It will also create a symlink in `${HOME}/.spacelift/current` pointing to the current profile.

By default the login process is interactive. If that does not fit your workflow, the steps can be predefined using flags, for example:

```bash
❯ spacectl profile login --method browser --endpoint https://unicorn.app.spacelift.io local-test
```

You can switch between account profiles by using `spacectl profile select ${MY_ALIAS}`. What this does behind the scenes is point `${HOME}/.spacelift/current` to the new location. You can also delete stored credentials for a given profile by using the `spacectl profile logout ${MY_ALIAS}` command.
