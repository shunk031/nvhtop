#!/usr/bin/env python3

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="nvhtop",
    version="0.1",
    packages=find_packages(),
    author="Shunsuke Kitada",
    author_email="shunsuke.kitada.0831@gmail.com",
    description="A tool for enriching the output of nvidia-smi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["termcolor"],
    entry_points={"console_scripts": ["nvhtop=nvhtop.run:run"]},
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
