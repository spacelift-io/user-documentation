#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

############################################################
# help                                                     #
############################################################
help() {
   # Display Help
   echo "Creates a new version of the self-hosting documentation."
   echo
   echo "Syntax: create-self-hosting-release.sh [-v <version>]"
   echo "options:"
   echo "-v     The version number (e.g. v0.0.6)."
   echo "-h     Print this Help."
   echo
}

version=""

while getopts ":v:h" option; do
    case $option in
        h) # display Help
            help
            exit;;

        v) # The configuration file
            version=$OPTARG;;

        \?) # Invalid option
            error "invalid option was provided"
            help
            exit;;
    esac
done

if [[ -z "${version}" ]]; then
  echo "Please specify a version number using the '-v' flag"
  exit 1
fi

if [[ "${version}" != v* ]]; then
  echo "The version number must be in the format 'vx.x.x'"
  exit 1
fi

target_dir="self-hosting/${version}"

if [[ -d "${target_dir}" ]]; then
  echo "Version ${version} of self-hosting already found in '${target_dir}'. Please specify a different version number or delete the '${target_dir}' directory and try again"
  exit 1
fi

echo "Creating ${target_dir}"

mkdir -p "${target_dir}"
cp -r "docs" "${target_dir}"
cp "nav.self-hosting.yaml" "${target_dir}/nav.yaml"

mkdocs_config=$(cat <<EOF
INHERIT: ./nav.yaml
copyright: © 2023 Spacelift, Inc. All rights reserved
site_author: Spacelift
site_description: Collaborative Infrastructure For Modern Software Teams
site_name: Self-Hosting ${version}
site_url: https://docs.spacelift.io/self-hosting-${version}
EOF
)

echo "${mkdocs_config}" > "${target_dir}/mkdocs.yaml"

echo "New version of self-hosting docs created!"
