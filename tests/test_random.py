#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylint: disable=W0212

import os
import re
import sys
# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from scribd_dl import ScribdDL
from scribd_dl.utilities import (
    valid_url,
    valid_pages,
    get_modified_time_diff,
    generate_random_document,
    RestrictedDocumentError
)


def test_2p_random_document_1(scribd):
    URL = generate_random_document()
    print('-- Random document : {}'.format(URL))
    PAGES = '1-2'

    func_name = sys._getframe().f_code.co_name
    doc_id = re.search(r'(?P<id>\d+)', URL).group('id')
    scribd.extra = {'doc_id': '{}-{}'.format(func_name, doc_id)}
    scribd.args.url = URL
    scribd.args.pages = PAGES
    assert valid_url(URL)
    assert valid_pages(PAGES)

    try:
        scribd.visit_page(URL)
    except RestrictedDocumentError:
        assert True
    else:
        download = scribd.doc_title + '.pdf'
        if download in os.listdir() and get_modified_time_diff(download) < 10:
            assert True
        else:
            assert False


def test_2p_random_document_2(scribd):
    URL = generate_random_document()
    print('-- Random document : {}'.format(URL))
    PAGES = '1-2'

    func_name = sys._getframe().f_code.co_name
    doc_id = re.search(r'(?P<id>\d+)', URL).group('id')
    scribd.extra = {'doc_id': '{}-{}'.format(func_name, doc_id)}
    scribd.args.url = URL
    scribd.args.pages = PAGES
    assert valid_url(URL)
    assert valid_pages(PAGES)

    try:
        scribd.visit_page(URL)
    except RestrictedDocumentError:
        assert True
    else:
        download = scribd.doc_title + '.pdf'
        if download in os.listdir() and get_modified_time_diff(download) < 10:
            assert True
        else:
            assert False
