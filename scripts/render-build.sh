#!/bin/bash

rm -rf site
mkdir -p site/self-hosted

# Build the SaaS version of the site
SPACELIFT_DISTRIBUTION=SAAS ./scripts/remove-files-based-on-distribution.sh
mkdocs build

# Re-create the files before building the Self-Hosted version
git checkout docs

# Build the self-hosting version of the site
SPACELIFT_DISTRIBUTION=SELF_HOSTED ./scripts/remove-files-based-on-distribution.sh
NAV_FILE=./nav.self-hosted.yaml SPACELIFT_DISTRIBUTION=SELF_HOSTED DOC_ENV=preprod LOGO=assets/images/logo-selfhosted.svg mkdocs build -d site/self-hosted/latest
