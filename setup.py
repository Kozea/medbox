#!/usr/bin/env python

import os.path
from setuptools import setup

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python :: Implementation :: PyPy',
]

setup(
    name='medbox',
    version='0.0.1',
    provides=['medbox'],
    packages=['medbox'],
    author='Guillaume Ayoub',
    author_email='guillaume.ayoub@kozea.fr',
    url='https://github.com/Kozea/medbox',
    description='A single box for your medicine',
    long_description=open(
        os.path.join(os.path.dirname(__file__), 'README')).read(),
    classifiers=classifiers,
)
