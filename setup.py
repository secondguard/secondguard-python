#!/usr/bin/env python3
from setuptools import setup, find_packages

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
    author='Michael Flaxman',
    author_email='python-library@secondguard.com',
    description='SecondGuard Python Library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/secondguard/secondguard-python/',
    version='2.5.1',
    install_requires=REQUIREMENTS,
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.3',
    include_package_data=True,
    package_data={"": ["LICENSE"]},
)

