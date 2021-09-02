#!/usr/bin/env python
# Install script 

import os
from os.path import join as pjoin
from setuptools import setup
from setuptools.command.install import install


#
longdescription = """

# sbx2imagej

 ``pip install sbx2imagej``

Source code is in [the repository](https://github.com/orena1/sbx2imagej.git)

"""

setup(
    name = 'sbx2imagej',
    version = '0.0.6',
    author = 'Oren Amsalem',
    author_email = 'oren.a4@gmail.com',
    description = "...",
    long_description = longdescription,
    long_description_content_type='text/markdown',
    license = 'GPL',
    install_requires = ['scipy', 'sbxreader', 'pyimagej', 'PyQt5'],
    url = "https://github.com/orena1/sbx2imagej",
    packages = ['sbx2imagej'],
    entry_points = {
        'console_scripts': [
            'sbx2imagej = sbx2imagej.sbx2imagej:main',
        ]
    },
)
