from setuptools import setup, find_packages

setup(
    name="pykpn",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': ['simulate_slx=pykpn.simulate.simulate_slx:main'],
    },
    install_requires=[
          'argparse',
          'numpy',
          'pydot',
          'simpy',
          'pyvcd',
      ],
)
