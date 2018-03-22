#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
from scribd_dl.utils import get_modified_time_diff


def test_90p_first_page(scribd):
    URL = ['https://www.scribd.com/document/352366744/Big-Data-A-Twenty-First-Century-Arms-Race']
    PAGES = '1'

    scribd.set_pages(PAGES)
    scribd.download(URL)
    doc_id = re.search(r'(?P<id>\d+)', URL[0]).group('id')
    saved_file = '{}-{}.pdf'.format(scribd.doc_title_edited, doc_id)
    if saved_file in os.listdir() and get_modified_time_diff(saved_file) < 10:
        assert True
    else:
        assert False


def test_16p_last_page(scribd):
    URL = ['https://www.scribd.com/document/106884805/Nebraska-Wing-Sep-2012']
    PAGES = '16'

    scribd.set_pages(PAGES)
    scribd.download(URL)
    doc_id = re.search(r'(?P<id>\d+)', URL[0]).group('id')
    saved_file = '{}-{}.pdf'.format(scribd.doc_title_edited, doc_id)
    if saved_file in os.listdir() and get_modified_time_diff(saved_file) < 10:
        assert True
    else:
        assert False


def test_6p_whole(scribd):
    URL = ['https://www.scribd.com/document/372746970/Nunes-to-Sessions-FBI-may-have'
           '-violated-criminal-statutes-in-Carter-Page-FISA-application']

    scribd.set_pages(None)
    scribd.download(URL)
    doc_id = re.search(r'(?P<id>\d+)', URL[0]).group('id')
    saved_file = '{}-{}.pdf'.format(scribd.doc_title_edited, doc_id)
    if saved_file in os.listdir() and get_modified_time_diff(saved_file) < 10:
        assert True
    else:
        assert False


def test_78p_long_title_first_page(scribd):
    URL = ['https://www.scribd.com/document/352506425/Hydroponic-Green-House-Farming-Detailed-Project-Report-'
           'Profile-Business-Plan-Industry-Trends-Market-Research-Survey-Raw-Materials-Feasibility-S']
    PAGES = '1'

    scribd.set_pages(PAGES)
    scribd.download(URL)
    doc_id = re.search(r'(?P<id>\d+)', URL[0]).group('id')
    saved_file = '{}-{}.pdf'.format(scribd.doc_title_edited, doc_id)
    if saved_file in os.listdir() and get_modified_time_diff(saved_file) < 10:
        assert True
    else:
        assert False


def test_22p_edited_title(scribd):
    URL = ['https://www.scribd.com/document/90403141/Social-Media-Strategy']
    PAGES = '1-2'

    scribd.set_pages(PAGES)
    scribd.doc_title_edited = 'Edited title'
    scribd.download(URL)
    doc_id = re.search(r'(?P<id>\d+)', URL[0]).group('id')
    saved_file = '{}-{}.pdf'.format(scribd.doc_title_edited, doc_id)
    if saved_file in os.listdir() and get_modified_time_diff(saved_file) < 10:
        assert True
    else:
        assert False
