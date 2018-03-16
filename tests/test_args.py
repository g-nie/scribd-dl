#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylint: disable=C0413,W0621

from argparse import ArgumentTypeError
# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from scribd_dl import ScribdDL
import pytest
from scribd_dl.utilities import (
    valid_url,
    valid_pages,
)


def test_valid_args():
    URL = 'https://www.scribd.com/doc/90403141/Social-Media-Strategy'
    assert valid_url(URL)
    URL = 'www.scribd.com/document/90403141/'
    assert valid_url(URL)
    URL = 'www.scribd.com/document/90403141'
    assert valid_url(URL)
    URL = 'https://www.scribd.com/doc/90403141'
    assert valid_url(URL)

    PAGES = '5'
    assert valid_pages(PAGES)
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
