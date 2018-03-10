=========
scribd-dl
=========


.. image:: https://img.shields.io/pypi/v/scribd_dl.svg
        :target: https://pypi.python.org/pypi/scribd_dl

.. image:: https://img.shields.io/travis/giannisterzopoulos/scribd_dl.svg
        :target: https://travis-ci.org/giannisterzopoulos/scribd_dl

.. image:: https://readthedocs.org/projects/scribd-dl/badge/?version=latest
        :target: https://scribd-dl.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


| **Download documents from Scribd in pdf format**
|
| Scribd-dl uses selenium and headless Chrome to take high resolutions screenshots of the document pages, and eventually merges them into a pdf file.

Installation
------------

Clone it ::

   >> git clone https://github.com/giannisterzopoulos/scribd-dl.git
   >> cd scribd-dl
   >> pip install .


Requirements
-------------
| Scribd-dl requires chromedriver to work as expected. It is tested to work with chromedriver v2.35 and Chrome v65.0.
| See all available chromedriver downloads `here`_.

.. _`here`: https://sites.google.com/a/chromium.org/chromedriver/downloads
