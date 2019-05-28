from setuptools import setup, find_packages

project_name="pykpn"
version="0.1"

setup(
    name=project_name,
    version=version,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'slx_kpn_to_dot=pykpn.slx.scripts.kpn_to_dot:main',
            'slx_platform_to_dot=pykpn.slx.scripts.platform_to_dot:main',
            'slx_mapping_to_dot=pykpn.slx.scripts.mapping_to_dot:main',
            'slx_mapping_to_autgrp=pykpn.slx.scripts.mapping_to_autgrp:main',
            'slx_random_walk=pykpn.slx.scripts.random_walk:main',
            'slx_simulate=pykpn.slx.scripts.simulate:main',
        ],
    },
    install_requires=[
        'argparse',
        'cvxpy',
        'lxml',
        'numpy',
        'matplotlib',
        'pint',
        'pydot',
        'pyxb',
        'simpy',
        'termcolor',
        'tqdm',
    ],
    setup_requires=['pytest-runner', 'sphinx'],
    tests_require=['pytest'],
    command_options={
        'build_sphinx': {
            'project': ('setup.py', project_name),
            'version': ('setup.py', version),
            'release': ('setup.py', version),
            'source_dir': ('setup.py', 'doc'),
            'build_dir': ('setup.py', 'doc/build'),}},
)
