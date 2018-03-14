#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylint: disable=C0413,W0621

import sys
import os
import time
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from scribd_dl import ScribdDL
# import pytest


# Assertions about expected exceptions
# with pytest.raises(ValueError, match=r'.* 123 .*'):
#         myfunc()

def _get_modified_time_diff(f):
    mod = time.ctime(os.path.getmtime(f))
    mod_time = datetime.strptime(mod, '%a %b %d %H:%M:%S %Y')
    return (datetime.now() - mod_time).total_seconds()


def test_22p_whole_document(scribd):
    URL = 'https://www.scribd.com/document/90403141/Social-Media-Strategy'

    scribd.args.url = URL
    scribd.visit_page(URL)
    # scribd.merge()

    download = scribd.doc_title + '.pdf'
    if download in os.listdir() and _get_modified_time_diff(download) < 60:
        assert True
    else:
        assert False


def test_90p_one_page(scribd):
    URL = 'https://www.scribd.com/document/352366744/Big-Data-A-Twenty-First-Century-Arms-Race'
    PAGES = '24-24'
    # PAGES = '50-90'

    scribd.args.url = URL
    scribd.args.pages = PAGES
    scribd.visit_page(URL)
    # scribd.merge()

    download = scribd.doc_title + '.pdf'
    if download in os.listdir() and _get_modified_time_diff(download) < 60:
        assert True
    else:
        assert False
