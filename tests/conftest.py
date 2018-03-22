#!/usr/bin/env python

# pylint: disable=C0413

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from scribd_dl import ScribdDL

# def pytest_addoption(parser):
#     parser.addoption("--driver", action="store", default="chrome", help="Type in browser type")
#     parser.addoption("--url", action="store", default="https://.../", help="url")


@pytest.fixture(scope='session')  # Can be module, session, function, class
def scribd(request):
    options = {
        'verbose': True,
        'testing': True
    }
    sc = ScribdDL(options)
    sc.start_browser()

    def fin():
        sc.close()
    request.addfinalizer(fin)
    return sc  # provide the fixture value
