#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from scribd_dl.utils import GreaterThanLastPageError


def test_16p_greater_than_last_page(scribd):
    URL = ['https://www.scribd.com/document/106884805/Nebraska-Wing-Sep-2012']
    PAGES = '15-22'

    with pytest.raises(GreaterThanLastPageError):
        scribd.download(URL, PAGES)
