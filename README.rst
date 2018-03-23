
=========
scribd-dl
=========

.. image:: https://img.shields.io/pypi/pyversions/scribd-dl.svg
        :target: https://pypi.python.org/pypi/scribd-dl/
        :alt: Python versions


.. image:: https://travis-ci.org/giannisterzopoulos/scribd-dl.svg?branch=master
        :target: https://travis-ci.org/giannisterzopoulos/scribd-dl
        :alt: Build Status


.. image:: https://badge.fury.io/py/scribd-dl.svg
        :target: https://pypi.python.org/pypi/scribd-dl/
        :alt: PyPI Version


.. image:: https://img.shields.io/badge/built%20with-Selenium-yellow.svg
        :target: https://github.com/SeleniumHQ/selenium
        :alt: Built with Selenium


.. image:: https://codecov.io/gh/giannisterzopoulos/scribd-dl/branch/master/graph/badge.svg
        :target: https://codecov.io/gh/giannisterzopoulos/scribd-dl
        :alt: Coverage


|
| **Download documents from Scribd in pdf format**
|
| Scribd-dl uses selenium and headless Chrome to take high resolutions screenshots of the document pages, and eventually merges them into a pdf file.

Usage
------------

.. code-block:: shell

    $ scribd-dl (https://www.)scribd.com/(doc|document|presentation)/(document_id)/* [-p PAGES] [-v]

Examples ::

    $ scribd-dl https://www.scribd.com/document/90403141/Social-Media-Strategy
    $ scribd-dl scribd.com/document/351688288 scribd.com/document/90403141 -p 1-3
    $ scribd-dl https://www.scribd.com/document/352366744 --pages 10-16
    $ scribd-dl scribd.com/document/351688288 -p 20 --verbose

you can embed scribd-dl, using a context manager like this:

.. code-block:: python

    import scribd_dl

    options = {
        'pages': '4-8',
        'log-level': '2'  # info
    }
    with scribd_dl.ScribdDL(options) as session:
        session.download(['https://www.scribd.com/document/351688288/'])


Installation
------------
Clone it ::

    $ git clone https://github.com/giannisterzopoulos/scribd-dl.git
    $ cd scribd-dl
    $ pip install .

or install from PyPI ::

    $ pip install scribd-dl

Requirements
-------------
| Chromedriver is required in order to work. See all available chromedriver downloads `here`_.
| Put the chromedriver executable in the assets folder or in your system PATH variable.
| Tested to work with chromedriver v2.37 and Chrome v65.0.
| Scribd-dl supports **Python 3.4-3.6**

.. _`here`: https://sites.google.com/a/chromium.org/chromedriver/downloads
