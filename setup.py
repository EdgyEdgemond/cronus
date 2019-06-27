#!/usr/bin/env python
import codecs
import os

import setuptools


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding="utf-8").read()


setuptools.setup(
    name="cronus",
    version="0.0.1",
    author="Daniel Edgecombe",
    author_email="edgy.edgemond@gmail.com",
    maintainer="Daniel Edgecombe",
    maintainer_email="edgy.edgemond@gmail.com",
    license="Apache Software License 2.0",
    url="https://github.com/EdgyEdgemond/cronus",
    description="A crontab parser",
    long_description=read("README.md"),
    packages=setuptools.find_packages(include=("cronus*",)),
    python_requires=">=3.6",
    install_requires=[],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Apache Software License",
    ],
    entry_points={
        "console_scripts": [
            "cronparse=cronus.cmd:main",
        ],
    },
    extras_require={
        "dev": (
            "flake8",
            "flake8-commas",
            "flake8-isort",
            "flake8-quotes",
            "isort>=4.3.15",
        ),
        "test": (
            "pytest-cov",
            "pytest-random-order",
            "pytest-xdist",
        ),
    },
)
