#!/bin/bash -e

script_dir=$(cd "$(dirname "$BASH_SOURCE")"; pwd)

function cleanup() {
  rm -rf $temp_dir
  echo "INFO: Removed $temp_dir"
}

trap cleanup EXIT

temp_dir=$(mktemp -d)
echo "INFO: Created $temp_dir"

cd "$temp_dir"

git clone https://github.com/OpenVPN/easy-rsa.git

rsync -a easy-rsa/* "$script_dir"/whisky_barrel/3rdparty/easy-rsa


