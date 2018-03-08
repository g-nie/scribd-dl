import io
import os
from setuptools import find_packages, setup


__version__ = '0.0.1'
__author__ = 'Giannis Terzopoulos'

requires = [
    'selenium==3.9.0',
    'Pillow>=4.3.0',
    'img2pdf>=0.2.4',
    'PyPDF2>=1.26.0'
]

here = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()


setup(
    name='scridb-dl',
    version=__version__,
    description='Scribd document downloader',
    long_description=long_description,
    author=__author__,
    author_email='terzo.giannis@gmail.com',
    url='https://github.com/giannisterzopoulos/scribd-dl',
    packages=find_packages(exclude=("tests", "tests.*")),
    install_requires=requires,
    license='MIT',
    classifiers=[
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
    ]
)
