#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylint: disable=W0212

import os
import re
import sys
# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from scribd_dl import ScribdDL
from scribd_dl.utils import (
    valid_url,
    valid_pages,
    get_modified_time_diff,
    generate_random_document,
    RestrictedDocumentError
)


def test_1p_random_document_1(scribd):
    URL = generate_random_document()
    PAGES = '1-1'

    func_name = sys._getframe().f_code.co_name
    doc_id = re.search(r'(?P<id>\d+)', URL).group('id')
    scribd.extra = {'doc_id': '{} - {}'.format(func_name, doc_id)}
    scribd.args.url = URL
    scribd.args.pages = PAGES
    assert valid_url(URL)
    assert valid_pages(PAGES)

    try:
        scribd.visit_page(URL)
    except RestrictedDocumentError:
        assert True
    else:
        if scribd.doc_title_edited in os.listdir() and get_modified_time_diff(scribd.doc_title_edited) < 10:
            assert True
        else:
            assert False


def test_1p_random_document_2(scribd):
    URL = generate_random_document()
    PAGES = '1-1'

    func_name = sys._getframe().f_code.co_name
    doc_id = re.search(r'(?P<id>\d+)', URL).group('id')
    scribd.extra = {'doc_id': '{} - {}'.format(func_name, doc_id)}
    scribd.args.url = URL
    scribd.args.pages = PAGES
    assert valid_url(URL)
    assert valid_pages(PAGES)

    try:
        scribd.visit_page(URL)
    except RestrictedDocumentError:
        assert True
    else:
        if scribd.doc_title_edited in os.listdir() and get_modified_time_diff(scribd.doc_title_edited) < 10:
            assert True
        else:
            assert False
