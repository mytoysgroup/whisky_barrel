#!/bin/bash -e

script_dir=$(cd "$(dirname "$BASH_SOURCE")"; pwd)
cd "$script_dir"

version="${1:?}"

echo "version='$version'" > wb_version.py

if [ -d dist ]; then rm -r dist; fi
python setup.py clean sdist bdist_wheel

if ! twine --version
then
  echo "You need to install twine first, e.g. by:"
  echo "python -m pip install --user --upgrade twine"
fi

twine check dist/*

twine upload --repository-url https://test.pypi.org/legacy/ dist/*

python -m pip install --index-url https://test.pypi.org/simple/ whisky_barrel


