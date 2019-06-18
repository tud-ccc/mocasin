import distutils.cmd

from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop
from doc.build_doc import BuildDocCommand
import subprocess

project_name = "pykpn"
version = "0.1"


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
        subprocess.check_call(["make", "pynauty"],
                              cwd="third_party_dependencies/pynauty-0.6")
        subprocess.check_call(["python", "setup.py", "install"],
                              cwd="third_party_dependencies/pynauty-0.6")


class InstallCommand(install):

    def run(self):
        self.run_command('pynauty')
        # XXX Actually install.run(self) should be used here. But there seems
        # to be a bug in setuptools that skips installing the required
        # packages... The line below seems to fix this.
        # See: https://cbuelter.wordpress.com/2015/10/25/extend-the-setuptools-install-command/comment-page-1/
        self.do_egg_install()


class DevelopCommand(develop):

    def run(self):
        self.run_command('pynauty')
        develop.run(self)


setup(
    name=project_name,
    version=version,
    packages=find_packages(),
    install_requires=[
        'argparse',
        'cvxpy',
        'lxml',
        'numpy<1.16',
        'matplotlib<3.0',
        'pint',
        'pydot',
        'pyxb',
        'simpy',
        'termcolor',
        'tqdm',
    ],
    setup_requires=['pytest-runner', 'sphinx'],
    tests_require=['pytest', 'pytest_mock'],
    command_options={
        'build_sphinx': {
            'project': ('setup.py', project_name),
            'version': ('setup.py', version),
            'release': ('setup.py', version),
            'source_dir': ('setup.py', 'doc'),
            'build_dir': ('setup.py', 'doc/build'),
        }
    },
    cmdclass={
        'doc': BuildDocCommand,
        'pynauty': InstallPynautyCommand,
        'install': InstallCommand,
        'develop': DevelopCommand,
    },
)
