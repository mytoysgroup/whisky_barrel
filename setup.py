import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="whisky_barrel",
    version="0.0.3",
    author="Henryk Trappmann",
    author_email="henryk.trappmann@mytoys.de",
    description="Tools for initialising and working with an AWS account",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mytoysgroup/whisky_barrel",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
)
