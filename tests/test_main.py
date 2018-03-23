#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import scribd_dl


def test_main():
    # GreaterThanLastPageError
    URL = 'https://www.scribd.com/document/294632720/'
    args = argparse.Namespace(url=URL, pages='3', verbose=True, testing=True)
    scribd_dl.main(args)
