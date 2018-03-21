#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
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

    doc_id = re.search(r'(?P<id>\d+)', URL).group('id')
    scribd.extra = {'doc_id': doc_id}
    scribd.args.url = URL
    scribd.args.pages = PAGES
    scribd.doc_title_edited = None
    assert valid_url(URL)
    assert valid_pages(PAGES)

    try:
        scribd.visit_page(URL)
    except RestrictedDocumentError:
        assert True
    else:
        saved_file = '{}-{}.pdf'.format(scribd.doc_title_edited, doc_id)
        if saved_file in os.listdir() and get_modified_time_diff(saved_file) < 10:
            assert True
        else:
            assert False


def test_1p_random_document_2(scribd):
    URL = generate_random_document()
    PAGES = '1-1'

    doc_id = re.search(r'(?P<id>\d+)', URL).group('id')
    scribd.extra = {'doc_id': doc_id}
    scribd.args.url = URL
    scribd.args.pages = PAGES
    scribd.doc_title_edited = None
    assert valid_url(URL)
    assert valid_pages(PAGES)

    try:
        scribd.visit_page(URL)
    except RestrictedDocumentError:
        assert True
    else:
        saved_file = '{}-{}.pdf'.format(scribd.doc_title_edited, doc_id)
        if saved_file in os.listdir() and get_modified_time_diff(saved_file) < 10:
            assert True
        else:
            assert False
