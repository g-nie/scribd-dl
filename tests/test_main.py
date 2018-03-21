#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import scribd_dl


def test_main():
    URL = 'https://www.scribd.com/doc/18587980/ARXAIA-G-Gymnasioy'
    args = argparse.Namespace(url=URL, pages='3', verbose=True, testing=True)
    scribd_dl.main(args)
