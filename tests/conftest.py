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


# Runs once at the beggining (setUp) and once when all tests have ended (tearDown)
@pytest.fixture(scope='function', autouse=True)
def scribd():  # Add request argument to access options

    # setUp
    args = argparse.Namespace(url='0000', pages='', verbose=False)  # PAGES ??
    sc = ScribdDL(args)
    sc.start_browser()
    yield sc

    # tearDown
    sc.close_browser()
