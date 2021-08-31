# Copyright (C) 2017 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Christian Menard

import sys

from setuptools import setup, find_packages, find_namespace_packages

project_name = "mocasin"
version = "0.1.0"

install_requirements = [
    "arpeggio",
    "cloudpickle",
    "cvxopt",
    "cvxpy!=1.1.8,<1.2" if sys.version_info < (3, 7) else "cvxpy!=1.1.8",
    "deap",
    "h5py",
    "hydra-core",
    "scipy<1.6.0" if sys.version_info < (3, 7) else "scipy",
    "lxml",
    "matplotlib",
    "more_itertools",
    "mpsym",
    "numba>=0.53.0rc1",
    "numpy<1.22",
    "pint",
    "pydot",
    "pynauty@https://files.pythonhosted.org/packages/fa/b1/87b0cb000fe6bf0201428c068659e02638f2c9583f205465fd14a1977a95/pynauty-1.0.2.tar.gz",
    "pyxb",
    "simpy",
    "sortedcontainers",
    "termcolor",
    "tqdm",
]
setup_requirements = ["pip", "pytest-runner", "sphinx"]


if sys.version_info < (3, 7):
    install_requirements.append("dataclasses")


setup(
    name=project_name,
    version=version,
    packages=find_packages(exclude=["test", "*.test"])
    + find_namespace_packages(include=["hydra_plugins.*"]),
    install_requires=install_requirements,
    setup_requires=setup_requirements,
    tests_require=["pytest", "pytest_mock", "pytest_raises"],
    command_options={
        "build_sphinx": {
            "project": ("setup.py", project_name),
            "version": ("setup.py", version),
            "release": ("setup.py", version),
            "source_dir": ("setup.py", "doc"),
            "build_dir": ("setup.py", "doc/build"),
        }
    },
    entry_points={
        "console_scripts": [
            "mocasin=mocasin.__main__:main",
        ]
    },
    include_package_data=True,
)
