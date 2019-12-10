#!/usr/bin/env python3

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="nvhtop",
    version="0.1",
    packages=find_packages(),
    description="A tool for enriching the output of nvidia-smi",
    long_description=long_description,
    install_requires=["termcolor"],
    entry_points={"console_scripts": ["nvhtop=nvhtop.run:run"]},
)
