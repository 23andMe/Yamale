#!/usr/bin/env python
from setuptools import setup, find_packages, Command
from subprocess import call

VERSION = (1, 0, 0, 'beta', 2)


# Dynamically calculate the version based on VERSION.
def get_version():
    "Returns a PEP 386-compliant version number from VERSION."
    version = VERSION
    assert len(version) == 5
    assert version[3] in ('alpha', 'beta', 'rc', 'final')

    # Now build the two parts of the version number:
    # main = X.Y[.Z]
    # sub = .devN - for pre-alpha releases
    #     | {a|b|c}N - for alpha, beta and rc releases

    parts = 2 if version[2] == 0 else 3
    main = '.'.join(str(x) for x in version[:parts])

    sub = ''

    if version[3] != 'final':
        mapping = {'alpha': 'a', 'beta': 'b', 'rc': 'c'}
        sub = mapping[version[3]] + str(version[4])

    return str(main + sub)


class Tag(Command):
    """Commits a tag with the current version."""

    description = "commit a tag with the current version"

    user_options = []

    def initialize_options(self): pass

    def finalize_options(self): pass

    def run(self):
        cmd = ['git', 'tag', get_version()]
        call(cmd)


with open('README.md') as f:
    readme = f.read()
with open('HISTORY.md') as f:
    history = f.read()
with open('LICENSE') as f:
    license = f.read()

setup(
    name='Yamale',
    version=get_version(),
    url='https://github.com/23andMe/Yamale',
    author='Bo Lopker',
    author_email='bo@k23andme.com',
    description='A schema and validator for YAML.',
    long_description=readme + '\n\n' + history,
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    install_requires=['pyyaml'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    cmdclass={
        'tag': Tag,
    },
)
