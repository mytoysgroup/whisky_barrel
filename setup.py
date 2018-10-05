import setuptools
import wb_version

import sys

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="whisky_barrel",
    version=wb_version.version,
    author="Henryk Trappmann",
    author_email="henryk.trappmann@mytoys.de",
    description="Tools for initialising and working with an AWS account",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mytoysgroup/whisky_barrel",
    entry_points={
        'console_scripts': ['pour = whisky_barrel.cert_lib:foo']
    },
    packages=setuptools.find_packages(),
    install_requires=['click','boto3'],
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
)
