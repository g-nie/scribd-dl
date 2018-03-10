=========
scribd_dl
=========


.. image:: https://img.shields.io/travis/giannisterzopoulos/scribd_dl.svg
        :target: https://travis-ci.org/giannisterzopoulos/scribd_dl

.. image:: https://img.shields.io/pypi/v/scribd_dl.svg
        :target: https://pypi.python.org/pypi/scribd_dl


|
| **Download documents from Scribd in pdf format**
|
| Scribd_dl uses selenium and headless Chrome to take high resolutions screenshots of the document pages, and eventually merges them into a pdf file.

Installation
------------

Clone it ::

   >> git clone https://github.com/giannisterzopoulos/scribd_dl.git
   >> cd scribd_dl
   >> pip install .


Requirements
-------------
| Scribd_dl requires chromedriver to work as expected. It is tested to work with chromedriver v2.35 and Chrome v65.0.
| See all available chromedriver downloads `here`_.

.. _`here`: https://sites.google.com/a/chromium.org/chromedriver/downloads
