#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0212

import os
import re
from scribd_dl import ScribdDL
from scribd_dl.utils import get_modified_time_diff


def test_context_manager():
    URLS = ['https://www.scribd.com/document/352366744/', 'https://www.scribd.com/document/351688288/']

    with ScribdDL() as session:
        session.download(URLS[0], pages='1-3')
        session.download(URLS[1], pages='3-5')

    saved_files = []
    doc_id = re.search(r'(?P<id>\d+)', URLS[0]).group('id')
    saved_files.append('{}-{}.pdf'.format(session._edit_title(session.doc_titles[0]), doc_id))

    doc_id = re.search(r'(?P<id>\d+)', URLS[1]).group('id')
    saved_files.append('{}-{}.pdf'.format(session._edit_title(session.doc_titles[1]), doc_id))

    for f in saved_files:
        if f in os.listdir() and get_modified_time_diff(f) < 60:
            assert True
        else:
            assert False
