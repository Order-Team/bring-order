from setuptools import setup, find_packages

from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

# This call to setup() does all the work
setup(
    name="testbringorder",
    version="0.1.8",
    description="test library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Order-Team/bring-order/tree/main",
    author="Bring-Order team",
    author_email="example@email.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ],
    packages=["bring_order"],
    include_package_data=True,
    install_requires=requirements
)
