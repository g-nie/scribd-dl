#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylint: disable=C0413

import sys
import os
import unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scribd_dl import scribd_dl
from selenium import webdriver


class TestScribd_dl(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--log-level=3')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-infobars')
        options.add_argument("--window-size=1600,2020")
        self.driver = webdriver.Chrome(options=options)

    def tearDown(self):
        self.driver.delete_all_cookies()
        self.driver.quit()

    def test_1(self):
        self.driver.get('https://www.google.com')
        self.assertEqual(self.driver.title, 'Google')

    def test_2(self):
        self.driver.get('https://www.google.com')
        self.assertEqual(self.driver.title, 'Google')


if __name__ == '__main__':
    unittest.main()


# import pytest


# def test_default_1():
#     t1 = 'bla'
#     t2 = 'bla'
#     assert t1 == t2


# def test_default_2():
#     t1 = 'bla'
#     t2 = 'bla'
#     assert t1 == t2


# def test_default_3():
#     t1 = 'bla'
#     t2 = 'bla'
#     assert t1 == t2
