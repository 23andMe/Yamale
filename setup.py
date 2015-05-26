#!/usr/bin/env python
import sys

from setuptools import setup, find_packages, Command
from subprocess import call

import yamale

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3


class Tag(Command):
    """Commits a tag with the current version."""

    description = 'commit a tag with the current version'

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        cmd = ['git', 'tag', yamale.__version__]
        call(cmd)

if PY2:
    readme = open('README.md').read()
    license = open('LICENSE').read()
elif PY3:
    readme = open('README.md', encoding='utf-8').read()
    license = open('LICENSE', encoding='utf-8').read()

setup(
    name='yamale',
    version=yamale.__version__,
    url='https://github.com/23andMe/Yamale',
    author='Bo Lopker',
    author_email='blopker@23andme.com',
    description='A schema and validator for YAML.',
    long_description=readme,
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['pyyaml'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4'
    ],
    cmdclass={
        'tag': Tag,
    },
)
