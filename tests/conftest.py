#!/usr/bin/env python

# pylint: disable=C0413

import sys
import os
import argparse
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from scribd_dl import ScribdDL

# def pytest_addoption(parser):
#     parser.addoption("--driver", action="store", default="chrome", help="Type in browser type")
#     parser.addoption("--url", action="store", default="https://.../", help="url")


# Run the fixture at the first test and run the finalizer after the last test has run.
# (available across multiple test functions, classes, and modules)
@pytest.fixture(scope='session')
def scribd(request):
    args = argparse.Namespace(url='0000', pages='', verbose=False)
    sc = ScribdDL(args)
    sc.start_browser()

    def fin():
        sc.close_browser()
    request.addfinalizer(fin)
    return sc  # provide the fixture value
