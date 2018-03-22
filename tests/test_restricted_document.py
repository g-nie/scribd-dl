#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from scribd_dl.utils import RestrictedDocumentError


def test_16p_restricted_document(scribd):
    URL = ['https://www.scribd.com/doc/240863282']
    PAGES = '1-3'

    scribd.set_pages(PAGES)
    with pytest.raises(RestrictedDocumentError):
        scribd.download(URL)
