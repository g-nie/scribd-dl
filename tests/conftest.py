#!/usr/bin/env python

# pylint: disable=C0413

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from scribd_dl import ScribdDL
from selenium import webdriver


# def pytest_addoption(parser):
#     parser.addoption("--driver", action="store", default="chrome", help="Type in browser type")
#     parser.addoption("--url", action="store", default="https://.../", help="url")

@pytest.fixture(scope='module', autouse=True)
def browser():  # Add request as argument to access options
    # setUp
    # options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # options.add_argument('--log-level=3')
    # options.add_argument('--disable-gpu')
    # options.add_argument('--disable-infobars')
    # options.add_argument("--window-size=1600,2020")
    # driver = webdriver.Chrome(options=options)

    driver = ScribdDL.start_browser()
    yield driver

    # tearDown
    driver.delete_all_cookies()
    driver.quit()

    # # tearDown
    # driver.delete_all_cookies()
    # driver.quit()
