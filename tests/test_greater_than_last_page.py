#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import pytest
from scribd_dl.utils import (
    valid_url,
    valid_pages,
    GreaterThanLastPageError
)


def test_16p_greater_than_last_page(scribd):
    URL = 'https://www.scribd.com/document/106884805/Nebraska-Wing-Sep-2012'
    PAGES = '15-22'

    doc_id = re.search(r'(?P<id>\d+)', URL).group('id')
    scribd.extra = {'doc_id': doc_id}
    scribd.args.url = URL
    scribd.args.pages = PAGES
    scribd.doc_title_edited = None
    assert valid_url(URL)
    assert valid_pages(PAGES)

    with pytest.raises(GreaterThanLastPageError):
        scribd.visit_page(URL)
