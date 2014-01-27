#!/usr/bin/env python

from setuptools import setup, find_packages

# Dynamically calculate the version based on schemata.VERSION.
version = __import__('schemata').get_version()

with open('README.md') as f:
    readme = f.read()
with open('HISTORY.md') as f:
    history = f.read()
with open('LICENSE') as f:
    license = f.read()

setup(
    name='Schemata',
    version=version,
    url='',
    author='Bo Lopker',
    author_email='bo@kbl.io',
    description='A schema validator for YAML, JSON and other static data.',
    long_description=readme + '\n\n' + history,
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    scripts=['bin/schemata'],
    zip_safe=False,
    test_suite='nose.collector',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
)
