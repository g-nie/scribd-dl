#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylint: disable=C0413,W0621,W0212

import re
# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from scribd_dl import ScribdDL
import pytest
from scribd_dl.utils import (
    valid_url,
    valid_pages,
    RestrictedDocumentError
)


def test_16p_restricted_document(scribd):
    URL = 'https://www.scribd.com/doc/240863282'
    PAGES = '1-3'

    doc_id = re.search(r'(?P<id>\d+)', URL).group('id')
    scribd.extra = {'doc_id': doc_id}
    scribd.args.url = URL
    scribd.args.pages = PAGES
    assert valid_url(URL)
    assert valid_pages(PAGES)

    with pytest.raises(RestrictedDocumentError):
        scribd.visit_page(URL)