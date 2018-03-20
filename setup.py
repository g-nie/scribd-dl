#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst', encoding='utf-8') as readme_file:
    long_description = '\n' + readme_file.read()

requirements = [
    'selenium>=3.9.0',
    'Pillow>=4.3.0',
    'img2pdf>=0.2.4',
    'requests>=2.18.4'
]

setup_requirements = []

test_requirements = []

setup(
    author="Giannis Terzopoulos",
    author_email='terzo.giannis@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description="Command-line program to download Scribd documents in pdf format",
    install_requires=requirements,
    license="MIT license",
    long_description=long_description,
    packages=find_packages(include=['scribd_dl']),
    package_data={
        'scribd_dl': ['assets/README.txt']
    },
    include_package_data=True,
    entry_points={
        'console_scripts': ['scribd-dl = scribd_dl.scribd_dl:main']
    },
    keywords='scribd_dl',
    name='scribd_dl',
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/giannisterzopoulos/scribd-dl',
    version='0.3.0',
    zip_safe=False,
)
