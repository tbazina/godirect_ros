## ! DO NOT MANUALLY INVOKE THIS setup.py, USE CATKIN INSTEAD

from setuptools import setup
from catkin_pkg.python_setup import generate_distutils_setup

setup_args = generate_distutils_setup(
    packages=['godirect_api', 'godirect_api.nodes'],
    package_dir={'': 'src'}
)

setup(**setup_args)