#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylint: disable=C0413,W0621

import sys
import os
from argparse import ArgumentTypeError
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from scribd_dl import ScribdDL
import pytest
from scribd_dl.util import valid_url, valid_pages, get_modified_time_diff, GreaterThanLastPageError


def test_valid_args():
    URL = 'https://www.scribd.com/doc/90403141/Social-Media-Strategy'
    assert valid_url(URL)
    URL = 'www.scribd.com/document/90403141/'
    assert valid_url(URL)
    URL = 'www.scribd.com/document/90403141'
    assert valid_url(URL)
    URL = 'https://www.scribd.com/doc/90403141'
    assert valid_url(URL)

    PAGES = '1-10'
    assert valid_pages(PAGES)
    PAGES = '6-6'
    assert valid_pages(PAGES)
    PAGES = '10-50'
    assert valid_pages(PAGES)


def test_invalid_args():
    URL = 'https://www.scribd.com/docLLL/90403141/Social-Media-Strategy'
    with pytest.raises(ArgumentTypeError):
        valid_url(URL)
    URL = 'scribd.com/document/90403141/'
    with pytest.raises(ArgumentTypeError):
        valid_url(URL)
    URL = 'https://www.scribd.com/doc/90403141-aaa/'
    with pytest.raises(ArgumentTypeError):
        valid_url(URL)

    PAGES = '1-'
    with pytest.raises(ArgumentTypeError):
        valid_pages(PAGES)
    PAGES = '-6'
    with pytest.raises(ArgumentTypeError):
        valid_pages(PAGES)
    PAGES = '1 - 5'
    with pytest.raises(ArgumentTypeError):
        valid_pages(PAGES)
    PAGES = '0-10'
    with pytest.raises(ArgumentTypeError):
        valid_pages(PAGES)
    PAGES = '10-8'
    with pytest.raises(ArgumentTypeError):
        valid_pages(PAGES)


def test_22p_whole(scribd):
    URL = 'https://www.scribd.com/document/90403141/Social-Media-Strategy'

    scribd.args.url = URL
    assert valid_url(URL)

    scribd.visit_page(URL)

    download = scribd.doc_title + '.pdf'
    if download in os.listdir() and get_modified_time_diff(download) < 60:
        assert True
    else:
        assert False


def test_90p_first_page(scribd):
    URL = 'https://www.scribd.com/document/352366744/Big-Data-A-Twenty-First-Century-Arms-Race'
    PAGES = '1-1'

    scribd.args.url = URL
    scribd.args.pages = PAGES
    assert valid_url(URL)
    assert valid_pages(PAGES)

    scribd.visit_page(URL)

    download = scribd.doc_title + '.pdf'
    if download in os.listdir() and get_modified_time_diff(download) < 60:
        assert True
    else:
        assert False


def test_16p_last_page(scribd):
    URL = 'https://www.scribd.com/document/106884805/Nebraska-Wing-Sep-2012'
    PAGES = '16-16'

    scribd.args.url = URL
    scribd.args.pages = PAGES
    assert valid_url(URL)
    assert valid_pages(PAGES)

    scribd.visit_page(URL)

    download = scribd.doc_title + '.pdf'
    if download in os.listdir() and get_modified_time_diff(download) < 60:
        assert True
    else:
        assert False


def test_greater_than_last_page(scribd):
    URL = 'https://www.scribd.com/document/106884805/Nebraska-Wing-Sep-2012'
    PAGES = '15-22'

    scribd.args.url = URL
    scribd.args.pages = PAGES
    assert valid_url(URL)
    assert valid_pages(PAGES)

    with pytest.raises(GreaterThanLastPageError):
        scribd.visit_page(URL)
