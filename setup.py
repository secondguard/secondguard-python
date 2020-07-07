#!/usr/bin/env python3
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# read the contents of your README file
from os import path
from io import open
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# https://stackoverflow.com/a/15341042/1754586
REQUIREMENTS = [i.strip() for i in open("requirements.in").readlines()]

setup(
    name='secondguard',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.8',
    description='SecondGuard Python Library',
    author='Michael Flaxman',
    author_email='python-library@secondguard.com',
    url='https://github.com/secondguard/secondguard-python/',
    install_requires=REQUIREMENTS,
    # FIXME: update once on PyPi
    # packages=['secondguard-python'],
    include_package_data=True,
    package_data={"": ["LICENSE"]}
)

