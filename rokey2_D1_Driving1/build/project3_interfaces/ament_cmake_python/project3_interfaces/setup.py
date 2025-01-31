from setuptools import find_packages
from setuptools import setup

setup(
    name='project3_interfaces',
    version='0.0.0',
    packages=find_packages(
        include=('project3_interfaces', 'project3_interfaces.*')),
)
