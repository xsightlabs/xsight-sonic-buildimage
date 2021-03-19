#!/usr/bin/env python

import os
import sys
from setuptools import setup
os.listdir

setup(
   name='es9632xx_0420_xse',
   version='1.0',
   description='Module to initialize Accton ES9632XX-0420-XSE platforms',

   packages=['es9632xx_0420_xse'],
   package_dir={'es9632xx_0420_xse': 'es9632xx-0420-xse/classes'},
)

