# Copyright (C) 2021 TU Dresden
# All rights reserved
#
# Authors: Christian Menard

from setuptools import setup, find_namespace_packages, find_packages

project_name = "mocasin-example-plugin"
version = "0.1.0"

setup(
    name=project_name,
    version=version,
    packages=find_packages(exclude=["test", "*.test"])
    + find_namespace_packages(include=["hydra_plugins.*"]),
    install_requires=["mocasin", "hydra-core<1.1.0"],
    include_package_data=True,
)
