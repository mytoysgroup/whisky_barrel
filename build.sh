#!/bin/bash -e

script_dir=$(cd "$(dirname "$BASH_SOURCE")"; pwd)
cd "$script_dir"

python setup.py clean build install

