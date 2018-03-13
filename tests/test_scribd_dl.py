#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylint: disable=C0413,W0621

import sys
import os
import argparse
import pytest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scribd_dl import ScribdDL
from selenium import webdriver


def test_t1(browser):
    browser.get('https://www.google.com')
    print(browser.title)  # ----
    assert browser.title == 'Google'
