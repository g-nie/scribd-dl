#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
from datetime import datetime
from selenium.common.exceptions import WebDriverException
from .scribd_dl import ScribdDL  # noqa: F401
from .version import AUTHOR, EMAIL, STATUS, VERSION, DATE
from .utils import valid_url, valid_pages

__author__ = AUTHOR
__email__ = EMAIL
__status__ = STATUS
__version__ = VERSION
__date__ = DATE


def main(args=None):
    try:
        if not args:
            parser = argparse.ArgumentParser(description='Scribd document downloader')
            parser.add_argument('url', help='Url of the document', type=valid_url)  # Required positional argument
            parser.add_argument('-p', '--pages', help='Range of pages to be selected (e.g. 10-20)', type=valid_pages)
            parser.add_argument('-v', '--verbose', help='Show verbose output in terminal', action='store_true')
            args = parser.parse_args()
        url = args.url

        scribd = ScribdDL(args)
        logger = scribd.logger

        scribd.start_browser()
        driver = scribd.driver

        scribd.visit_page(url)
        scribd.close_browser()
        logger.debug('Execution time : %s seconds', (datetime.now() - scribd.START).seconds, extra=scribd.extra)

    except KeyboardInterrupt:
        logger.warning('Interrupted.', extra=scribd.extra)
        try:
            driver.quit()
        except NameError:
            pass
        sys.exit()

    except WebDriverException:
        logger.error('Cannot establish a connection.', extra=scribd.extra)
