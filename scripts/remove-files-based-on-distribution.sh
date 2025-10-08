#!/bin/bash

if [[ "$SPACELIFT_DISTRIBUTION" == "SELF_HOSTED" ]]; then
  # Remove any SaaS-only pages
  rm docs/self-hosted.md
  rm docs/integrations/cloud-providers/azure.md
  rm docs/integrations/cloud-providers/gcp.md
  rm docs/product/billing/aws-marketplace.md
  rm docs/product/billing/stripe.md
  rm docs/product/changelog.md # SaaS-only changelog
else
  # Remove any Self-Hosted-only pages
  rm -rf docs/installing-spacelift
fi
