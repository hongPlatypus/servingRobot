from setuptools import find_packages
from setuptools import setup

setup(
    name='driving1_interfaces',
    version='0.0.0',
    packages=find_packages(
        include=('driving1_interfaces', 'driving1_interfaces.*')),
)
