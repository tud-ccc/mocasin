from setuptools import setup, find_packages
from doc.build_doc import BuildDocCommand

project_name = "pykpn"
version = "0.1"

setup(
    name=project_name,
    version=version,
    packages=find_packages(),
    install_requires=[
        'argparse',
        'cvxpy<=1.0.0',
        'cvxopt',
        'scipy<=1.1.0',
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
    setup_requires=['pytest-runner', 'sphinx', 'numpy<1.16'],
    tests_require=['pytest', 'pytest_mock'],
    command_options={
        'build_sphinx': {
            'project': ('setup.py', project_name),
            'version': ('setup.py', version),
            'release': ('setup.py', version),
            'source_dir': ('setup.py', 'doc'),
            'build_dir': ('setup.py', 'doc/build'),}},
    cmdclass = {
        'doc': BuildDocCommand
    }
)
