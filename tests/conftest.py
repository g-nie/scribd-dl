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


@pytest.fixture(scope='module', autouse=True)
def browser():  # Add request as argument to access options

    # setUp
    args = argparse.Namespace(url='0000')
    driver = ScribdDL(args)
    yield driver.start_browser()

    # tearDown
    driver.close_browser()
