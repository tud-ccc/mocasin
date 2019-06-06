from setuptools import setup, find_packages

setup(
    name="pykpn",
    version="0.1",
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
        'cvxopt',
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
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
