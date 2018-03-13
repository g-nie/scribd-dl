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


# @pytest.fixture(scope='module', autouse=True)
# @pytest.fixture
# def initialize_22p():  # Add request as argument to access options
#     # setUp
#     # options = webdriver.ChromeOptions()
#     # options.add_argument('--headless')
#     # options.add_argument('--log-level=3')
#     # options.add_argument('--disable-gpu')
#     # options.add_argument('--disable-infobars')
#     # options.add_argument("--window-size=1600,2020")
#     # driver = webdriver.Chrome(options=options)

#     # print('STARTING')
#     args = argparse.Namespace(url='')
#     driver = ScribdDL(args)
#     yield driver.start_browser()

#     # tearDown
#     # print('FINISHING')
#     driver.close_browser()
#     # driver.delete_all_cookies()
#     # driver.quit()

#     # # tearDown
#     # driver.delete_all_cookies()
#     # driver.quit()


def test_t1(browser):
    browser.get('https://www.google.com')
    print(browser.title)  # ----
    assert browser.title == 'Google'
