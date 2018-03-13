#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylint: disable=C0413

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scribd_dl import scribd_dl
from selenium import webdriver


def test_t1(browser):
    browser.get('https://www.google.com')
    assert browser.title == 'Google'
