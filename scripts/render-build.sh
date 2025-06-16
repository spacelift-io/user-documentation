#!/bin/bash

rm -rf site
mkdir -p site/self-hosted

# Generate llms.txt
python3 scripts/generate_llms_txt.py

# Build the SaaS version of the site
SPACELIFT_DISTRIBUTION=SAAS ./scripts/remove-files-based-on-distribution.sh
mkdocs build

# Copy llms.txt to the built site
cp llms.txt site/

# Re-create the files before building the Self-Hosted version
git checkout docs

# Build the self-hosting version of the site
SPACELIFT_DISTRIBUTION=SELF_HOSTED ./scripts/remove-files-based-on-distribution.sh
NAV_FILE=./nav.self-hosted.yaml SPACELIFT_DISTRIBUTION=SELF_HOSTED DOC_ENV=preprod LOGO=assets/images/logo-selfhosted.svg SITE_URL=https://docs.spacelift.dev/self-hosted mkdocs build -d site/self-hosted/latest

# Copy llms.txt to the self-hosted site as well
cp llms.txt site/self-hosted/latest/
