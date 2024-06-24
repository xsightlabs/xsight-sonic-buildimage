#!/usr/bin/env python

import os
import sys
from setuptools import setup
os.listdir

setup(
   name='x2evb',
   version='1.0',
   description='Module to initialize Xsight X2EVB platforms',

   packages=['x2evb'],
   package_dir={'x2evb': 'x2evb/classes'},
)

