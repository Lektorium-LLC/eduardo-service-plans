#!/usr/bin/env python
import os
from setuptools import setup, find_packages


def is_requirement(line):
    """
    Return True if the requirement line is a package requirement;
    that is, it is not blank, a comment, or editable.
    """
    # Remove whitespace at the start/end of the line
    line = line.strip()

    # Skip blank lines, comments, and editable installs
    return not (
        line == '' or
        line.startswith('-r') or
        line.startswith('#') or
        line.startswith('-e') or
        line.startswith('git+')
    )


def load_requirements(*requirements_paths):
    """
    Load all requirements from the specified requirements files.
    Returns a list of requirement strings.
    """
    requirements = set()
    for path in requirements_paths:
        requirements.update(
            line.strip() for line in open(path).readlines()
            if is_requirement(line)
        )
    return list(requirements)


setup(
    name='eduardo-service-plans',
    version='0.1.0',
    author='lektorium',
    author_email='info@lektorium.tv',
    url='https://github.com/lektorium-llc/eduardo-service-plans',
    description='Application handling service plans and service subscriptions for users',
    license='AGPL',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
        'Topic :: Internet :: WWW/HTTP',
    ],
    install_requires=['setuptools'],
    requires=[]
)
