#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylint: disable=C0413,W0621

import sys
import os
import pytest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scribd_dl import ScribdDL


def test_22p_whole_document(scribd):
    URL = 'https://www.scribd.com/document/90403141/Social-Media-Strategy'
    PAGES = '1-3'

    scribd.args.url = URL
    scribd.args.pages = PAGES

    scribd.visit_page(URL)

    assert True

def test_XXp_whole_document(scribd):
    URL = 'https://www.scribd.com/document/90403141/Social-Media-Strategy'
    PAGES = '1-3'

    scribd.args.url = URL
    scribd.args.pages = PAGES

    scribd.visit_page(URL)

    assert True