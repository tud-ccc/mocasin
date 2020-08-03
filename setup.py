import distutils.cmd

from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop
from doc.build_doc import BuildDocCommand
import subprocess
import sys

project_name = "pykpn"
version = "0.1"

install_requirements = []
setup_requirements = []

if sys.version_info > (3, 8):
    install_requirements = [
        'argparse',
        'arpeggio',
        'cvxpy',
        'cvxopt',
        'scipy',
        'lxml',
        'numpy',
        'matplotlib',
        'pandas',
        'pint',
        'pydot',
        'pyxb',
        'simpy',
        'termcolor',
        'tqdm',
        'hydra-core<1.0',
        'deap',
        'networkx',
        'recordclass',
    ]
    setup_requirements = ['pytest-runner', 'sphinx', 'numpy']

else:
    install_requirements = [
        'argparse',
        'arpeggio',
        'cvxpy<=1.0.0',
        'cvxopt',
        'scipy<=1.1.0',
        'lxml',
        'numpy<1.16',
        'matplotlib<3.0',
        'pandas',
        'pint',
        'pydot',
        'pyxb',
        'simpy',
        'termcolor',
        'tqdm',
        'hydra-core<1.0',
        'deap',
        'networkx',
        'recordclass',
    ]
    setup_requirements = ['pytest-runner', 'sphinx', 'numpy<1.16']

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


class InstallTsneCommand(distutils.cmd.Command):
    """A custom command to install the tsne dependency"""

    description = "install the tsne dependency"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run the command.

        Run ``python setup.py install`` to install tsne.
        """
        subprocess.check_call(["python", "setup.py", "install"],
                              cwd="third_party_dependencies/tsne")


class InstallCommand(install):

    def run(self):
        self.run_command('pynauty')
        self.run_command('tsne')
        # XXX Actually install.run(self) should be used here. But there seems
        # to be a bug in setuptools that skips installing the required
        # packages... The line below seems to fix this.
        # See: https://cbuelter.wordpress.com/2015/10/25/extend-the-setuptools-install-command/comment-page-1/
        self.do_egg_install()


class DevelopCommand(develop):

    def run(self):
        develop.run(self)
        self.run_command('pynauty')
        self.run_command('tsne')

#All version restrictions stem from numpy causing issues, it seems with CI:
#see: https://github.com/numpy/numpy/issues/14012

setup(
    name=project_name,
    version=version,
    packages=find_packages(),
    install_requires=install_requirements,
    setup_requires=setup_requirements,
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
        'tsne': InstallTsneCommand,
        'install': InstallCommand,
        'develop': DevelopCommand,
    },
    entry_points={'console_scripts': ['pykpn=pykpn.__main__:main']},
    include_package_data=True,
)
