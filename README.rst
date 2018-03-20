
.. image:: https://img.shields.io/travis/giannisterzopoulos/scribd_dl.svg
        :target: https://travis-ci.org/giannisterzopoulos/scribd_dl

.. image:: https://img.shields.io/pypi/v/scribd_dl.svg
        :target: https://pypi.python.org/pypi/scribd_dl


=========
scribd-dl
=========
|
| **Download documents from Scribd in pdf format**
|
| Scribd_dl uses selenium and headless Chrome to take high resolutions screenshots of the document pages, and eventually merges them into a pdf file.

Installation
------------
Clone it ::

   >> git clone https://github.com/giannisterzopoulos/scribd-dl.git
   >> cd scribd-dl
   >> pip install .


Requirements
-------------
| Scribd_dl requires chromedriver in order to work. See all available chromedriver downloads `here`_.
| Put the chromedriver executable in the assets folder or in your system PATH variable.
| Tested to work with chromedriver v2.37 and Chrome v65.0.

.. _`here`: https://sites.google.com/a/chromium.org/chromedriver/downloads

