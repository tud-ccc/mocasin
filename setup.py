# Copyright (C) 2017 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Christian Menard

import distutils.cmd
import os
import urllib.request
import sys
import tarfile
import tempfile

from setuptools import setup, find_packages, find_namespace_packages
from setuptools.command.install import install
from setuptools.command.develop import develop
from doc.build_doc import BuildDocCommand
import subprocess

project_name = "mocasin"
version = "0.1.0"

install_requirements = [
    "arpeggio",
    "cvxopt",
    "cvxpy!=1.1.8,<1.2" if sys.version_info < (3, 7) else "cvxpy!=1.1.8",
    "deap",
    "h5py",
    "hydra-core>=1.0.3,<1.1.0",
    "scipy<1.6.0" if sys.version_info < (3, 7) else "scipy",
    "lxml",
    "matplotlib",
    "numba>=0.53.0rc1",
    "numpy",
    "pint",
    "pydot",
    "pympsym>=0.5",
    "pyxb",
    "simpy",
    "sortedcontainers",
    "termcolor",
    "tqdm",
]
setup_requirements = ["pip", "pytest-runner", "sphinx"]


if sys.version_info < (3, 7):
    install_requirements.append("dataclasses")


class InstallPynautyCommand(distutils.cmd.Command):
    """A custom command to install the pynauty dependency"""

    description = "install the pynauty dependency"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run the command.

        First, run ``make pynauty`` to build the c library. Then, run ``python
        setup.py install`` to install pynauty.
        """
        cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            print("Downloading nauty")
            urllib.request.urlretrieve(
                "http://users.cecs.anu.edu.au/~bdm/nauty/nauty27r1.tar.gz",
                "nauty27r1.tar.gz",
            )
            print("Downloading pynauty")
            urllib.request.urlretrieve(
                "https://web.cs.dal.ca/~peter/software/pynauty/pynauty-0.6.0.tar.gz",
                "pynauty-0.6.0.tar.gz",
            )
            print("Extracting pynauty")
            with tarfile.open("pynauty-0.6.0.tar.gz") as tar:
                tar.extractall(".")
            print("Extracting nauty")
            with tarfile.open("nauty27r1.tar.gz") as tar:
                tar.extractall("pynauty-0.6.0/")
            os.rename("pynauty-0.6.0/nauty27r1", "pynauty-0.6.0/nauty")
            print("Build pynauty")
            subprocess.check_call(
                ["make", "pynauty"], cwd=f"{tmpdir}/pynauty-0.6.0"
            )
            print("Install pynauty")
            subprocess.check_call(
                ["pip", "install", "."], cwd=f"{tmpdir}/pynauty-0.6.0"
            )
        os.chdir(cwd)


def install_pynauty(cmd):
    # If the environment variable NO_PYNAUTY is set to any value, we skip
    # pynauty installation
    if "NO_PYNAUTY" not in os.environ:
        # also skip installation if already installed
        try:
            import pynauty
        except ImportError:
            cmd.run_command("pynauty")


class InstallCommand(install):
    def run(self):
        install_pynauty(self)
        install.run(self)


class DevelopCommand(develop):
    def run(self):
        install_pynauty(self)
        develop.run(self)


setup(
    name=project_name,
    version=version,
    packages=find_packages(exclude=["test", "*.test"])
    + find_namespace_packages(include=["hydra_plugins.*"]),
    install_requires=install_requirements,
    setup_requires=setup_requirements,
    tests_require=["pytest", "pytest_mock"],
    command_options={
        "build_sphinx": {
            "project": ("setup.py", project_name),
            "version": ("setup.py", version),
            "release": ("setup.py", version),
            "source_dir": ("setup.py", "doc"),
            "build_dir": ("setup.py", "doc/build"),
        }
    },
    cmdclass={
        "doc": BuildDocCommand,
        "pynauty": InstallPynautyCommand,
        "install": InstallCommand,
        "develop": DevelopCommand,
    },
    entry_points={
        "console_scripts": [
            "mocasin=mocasin.__main__:main",
        ]
    },
    include_package_data=True,
)
