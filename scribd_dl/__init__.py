#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
from datetime import datetime
from selenium.common.exceptions import WebDriverException
from .scribd_dl import ScribdDL  # noqa: F401
from .version import AUTHOR, EMAIL, STATUS, VERSION, DATE
from .utils import (
    valid_url,
    valid_pages,
    GreaterThanLastPageError,
    RestrictedDocumentError
)

__author__ = AUTHOR
__email__ = EMAIL
__status__ = STATUS
__version__ = VERSION
__date__ = DATE


def main(args=None):
    try:
        if not args:
            parser = argparse.ArgumentParser(description='Scribd document downloader', prog='scribd-dl')
            parser.add_argument('urls', help='Url of the document', type=valid_url, nargs='+')  # Required positional argument
            parser.add_argument('-p', '--pages', help='Range of pages to be selected (e.g. 10-20)', type=valid_pages)
            parser.add_argument('-v', '--verbose', help='Show verbose output in terminal', action='store_true')
            parser.add_argument('--version', action='version', version='%(prog)s {}'.format(__version__))
            args = parser.parse_args()

        options = {
            'pages': args.pages,
            'verbose': args.verbose
        }
        URLS = args.urls
        scribd = ScribdDL(options)
        logger = scribd.logger
        scribd.download(URLS)
        scribd.close()
        logger.debug('Execution time : %s seconds', (datetime.now() - scribd.START).seconds, extra=scribd.extra)

    except GreaterThanLastPageError:
        logger.error("Error: given page cannot be greater than document\'s last page", extra=scribd.extra)
        scribd.close()
        sys.exit(1)

    except RestrictedDocumentError:
        logger.error("Error: this document is only a preview and not fully availabe for reading", extra=scribd.extra)
        scribd.close()
        sys.exit(1)

    except WebDriverException:
        logger.error('Error: cannot establish a connection.', extra=scribd.extra)
        sys.exit(1)

    except KeyboardInterrupt:
        logger.warning('Interrupted.', extra=scribd.extra)
        try:
            scribd.close()
        except NameError:
            pass
        sys.exit()
