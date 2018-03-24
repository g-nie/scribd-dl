#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0212

import os
import re
from scribd_dl import ScribdDL
from scribd_dl.utils import get_modified_time_diff


def test_context_manager():
    URL = ['https://www.scribd.com/document/352366744/']
    PAGES = '1'

    options = {
        'pages': PAGES,
        'verbose': True
    }
    with ScribdDL(options) as session:
        print(session.logger)
        session.download(URL)
        doc_id = re.search(r'(?P<id>\d+)', URL[0]).group('id')
        saved_file = '{}-{}.pdf'.format(session._edit_title(session.doc_titles[-1]), doc_id)

    if saved_file in os.listdir() and get_modified_time_diff(saved_file) < 10:
        assert True
    else:
        assert False
