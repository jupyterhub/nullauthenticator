#!/usr/bin/env python3
# coding: utf-8

# Copyright (c) Juptyer Development Team.
# Distributed under the terms of the Modified BSD License.

from __future__ import print_function

import os
import shutil
import sys

name = 'nullauthenticator'
v = sys.version_info
if v[:2] < (3, 4):
    error = "ERROR: %s requires Python version 3.4 or above."
    print(error % name, file=sys.stderr)
    sys.exit(1)

# At least we're on the python version we need, move on.

import os
from glob import glob

from setuptools import setup
from setuptools.command.bdist_egg import bdist_egg

pjoin = os.path.join

#---------------------------------------------------------------------------
# Build basic package data, etc.
#---------------------------------------------------------------------------

ns = {}
with open('nullauthenticator.py') as f:
    for line in f:
        if line.startswith('__version__'):
            exec(line, {}, ns)
            break


class bdist_egg_disabled(bdist_egg):
    """Disabled version of bdist_egg

    Prevents setup.py install from performing setuptools' default easy_install,
    which it should never ever do.
    """

    def run(self):
        sys.exit("Aborting implicit building of eggs. Use `pip install .` to install from source.")


setup_args = dict(
    name='nullauthenticator',
    py_modules=['nullauthenticator'],
    version=ns['__version__'],
    description="JupyterHub: A multi-user server for Jupyter notebooks",
    long_description="See https://jupyterhub.readthedocs.io for more info.",
    author="Jupyter Development Team",
    author_email="jupyter@googlegroups.com",
    url="https://github.com/jupyterhub/nullauthenticator",
    license="BSD",
    platforms="Linux, Mac OS X",
    keywords=[
        'Interactive',
        'Jupyter',
        'JupyterHub',
        'Authentication',
    ],
    python_requires=">=3.4",
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    cmdclass={
        'bdist_egg': bdist_egg if 'bdist_egg' in sys.argv else bdist_egg_disabled,
    }
)

setup_args['install_requires'] = install_requires = []

with open('requirements.txt') as f:
    for line in f.readlines():
        req = line.strip()
        if not req or req.startswith('#') or '://' in req:
            continue
        install_requires.append(req)


def main():
    setup(**setup_args)


if __name__ == '__main__':
    main()
