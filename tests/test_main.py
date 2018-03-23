#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import scribd_dl


def test_main():
    URLS = ['https://www.scribd.com/document/294632720/']
    args = argparse.Namespace(urls=URLS, pages='3', verbose=True, testing=True)
    scribd_dl.main(args)
