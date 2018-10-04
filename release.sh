#!/bin/bash -e

script_dir=$(cd "$(dirname "$BASH_SOURCE")"; pwd)
cd "$script_dir"

rm -r dist

python setup.py sdist bdist_wheel

if ! twine --version
then
  echo "You need to install twine first, e.g. by:"
  echo "python -m pip install --user --upgrade twine"
fi

twine check dist/*

twine upload --repository-url https://test.pypi.org/legacy/ dist/*

python -m pip install --index-url https://test.pypi.org/simple/ whisky_barrel


