#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentTypeError
import pytest
from scribd_dl import ScribdDL
from scribd_dl.utils import (
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
    s = ScribdDL(options={})
    with pytest.raises(ValueError):  # Has to be of list type
        s.download('https://www.scribd.com/doc/90403141')

    URL = 'https://www.scribd.com/docLLL/90403141/Social-Media-Strategy'
    with pytest.raises(ArgumentTypeError):
        valid_url(URL)
    URL = 'scribd.com/document/90403141/'
    with pytest.raises(ArgumentTypeError):
        valid_url(URL)
    URL = 'https://www.scribd.com/doc/90403141-aaa/'
    with pytest.raises(ArgumentTypeError):
        valid_url(URL)

    PAGES = '0'
    with pytest.raises(ArgumentTypeError):
        valid_pages(PAGES)
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
