#!/bin/bash

rm -rf site
mkdir -p site/self-hosted

# Build the SaaS version of the site
mkdocs build

# Build the self-hosting version of the site
NAV_FILE=./nav.self-hosted.yaml SPACELIFT_DISTRIBUTION=SELF_HOSTED mkdocs build -d site/self-hosted/latest
