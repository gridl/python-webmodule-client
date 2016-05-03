#!/usr/bin/env python

import os
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand

setup(
    name="webmodule-client",
    version="0.0.0",
    author='Ross Fenning',
    author_email='Ross.Fenning@bbc.co.uk',
    packages=['webmodule_client'],
    description='Python client for services following the Webmodule standard.',
    url='http://github.com/BBC/python-webmodule-client',
    install_requires=['PyLD', 'pystache'],
    tests_require=[],
)
