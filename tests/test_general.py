#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0212

import os
import re
from scribd_dl.utils import get_modified_time_diff


def test_16p_last_page(scribd):
    URL = 'https://www.scribd.com/document/106884805/Nebraska-Wing-Sep-2012'
    PAGES = '16'

    scribd.download(URL, pages=PAGES)
    doc_id = re.search(r'(?P<id>\d+)', URL).group('id')
    saved_file = '{}-{}.pdf'.format(scribd._edit_title(scribd.doc_titles[-1]), doc_id)
    if saved_file in os.listdir() and get_modified_time_diff(saved_file) < 10:
        assert True
    else:
        assert False


def test_6p_whole(scribd):
    URL = 'https://www.scribd.com/document/374470199/INVITATION-pdf'

    scribd._set_pages(None)
    scribd.download(URL)
    doc_id = re.search(r'(?P<id>\d+)', URL).group('id')
    saved_file = '{}-{}.pdf'.format(scribd._edit_title(scribd.doc_titles[-1]), doc_id)
    if saved_file in os.listdir() and get_modified_time_diff(saved_file) < 10:
        assert True
    else:
        assert False


def test_78p_long_title_first_page(scribd):
    URL = 'https://www.scribd.com/document/352506425/Hydroponic-Green-House-Farming-Detailed-Project-Report-' \
        'Profile-Business-Plan-Industry-Trends-Market-Research-Survey-Raw-Materials-Feasibility-S'
    PAGES = '1'

    scribd.download(URL, PAGES)
    doc_id = re.search(r'(?P<id>\d+)', URL).group('id')
    saved_file = '{}-{}.pdf'.format(scribd._edit_title(scribd.doc_titles[-1]), doc_id)
    if saved_file in os.listdir() and get_modified_time_diff(saved_file) < 10:
        assert True
    else:
        assert False
