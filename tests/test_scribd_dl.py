#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylint: disable=C0413,W0621,W0212

import os
import re
import sys
# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from scribd_dl import ScribdDL
import pytest
from scribd_dl.utilities import (
    valid_url,
    valid_pages,
    get_modified_time_diff,
    GreaterThanLastPageError,
    RestrictedDocumentError
)


def test_90p_first_page(scribd):
    URL = 'https://www.scribd.com/document/352366744/Big-Data-A-Twenty-First-Century-Arms-Race'
    PAGES = '1'

    func_name = sys._getframe().f_code.co_name
    doc_id = re.search(r'(?P<id>\d+)', URL).group('id')
    scribd.extra = {'doc_id': '({}) {}'.format(func_name, doc_id)}
    scribd.args.url = URL
    scribd.args.pages = PAGES
    assert valid_url(URL)
    assert valid_pages(PAGES)
    scribd.visit_page(URL)

    download = scribd.doc_title + '.pdf'
    if download in os.listdir() and get_modified_time_diff(download) < 10:
        assert True
    else:
        assert False


def test_16p_last_page(scribd):
    URL = 'https://www.scribd.com/document/106884805/Nebraska-Wing-Sep-2012'
    PAGES = '16'

    func_name = sys._getframe().f_code.co_name
    doc_id = re.search(r'(?P<id>\d+)', URL).group('id')
    scribd.extra = {'doc_id': '({}) {}'.format(func_name, doc_id)}
    scribd.args.url = URL
    scribd.args.pages = PAGES
    assert valid_url(URL)
    assert valid_pages(PAGES)
    scribd.visit_page(URL)

    download = scribd.doc_title + '.pdf'
    if download in os.listdir() and get_modified_time_diff(download) < 10:
        assert True
    else:
        assert False


def test_22p_whole(scribd):
    URL = 'https://www.scribd.com/document/90403141/Social-Media-Strategy'

    # PAGES = '4'  # -------------------
    # scribd.args.pages = PAGES

    func_name = sys._getframe().f_code.co_name
    doc_id = re.search(r'(?P<id>\d+)', URL).group('id')
    scribd.extra = {'doc_id': '{}-{}'.format(func_name, doc_id)}
    scribd.args.url = URL
    assert valid_url(URL)
    scribd.visit_page(URL)

    download = scribd.doc_title + '.pdf'
    if download in os.listdir() and get_modified_time_diff(download) < 10:
        assert True
    else:
        assert False
