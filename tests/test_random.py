#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
from scribd_dl.utils import (
    get_modified_time_diff,
    generate_random_document,
    RestrictedDocumentError
)


def test_1p_random_document(scribd):
    URL = [generate_random_document()]
    PAGES = '1'
    scribd.set_pages(PAGES)
    try:
        scribd.download(URL)
    except RestrictedDocumentError:
        assert True
    else:
        doc_id = re.search(r'(?P<id>\d+)', URL[0]).group('id')
        saved_file = '{}-{}.pdf'.format(scribd.doc_title_edited, doc_id)
        if saved_file in os.listdir() and get_modified_time_diff(saved_file) < 10:
            assert True
        else:
            assert False
