# -*- coding: utf-8 -*-

import argparse
import re
import os
import time
import random
import logging
from datetime import datetime
import requests


class GreaterThanLastPageError(Exception):
    def __init__(self):
        Exception.__init__(self, "Given page cannot be greater than document\'s last page")


class RestrictedDocumentError(Exception):
    def __init__(self):
        Exception.__init__(self, "This document is only a preview and not fully availabe for reading")


# Make sure input url is of valid format
def valid_url(u):
    check = re.match(r'(https://)?www.scribd.com/(?:doc|document|presentation)/\d+(?:/.*|$)', u)
    if check:
        return u
    else:
        msg = 'Not a valid document url : {}'.format(u)
        raise argparse.ArgumentTypeError(msg)


# Make sure input page range is of valid format
def valid_pages(pages):
    check = re.fullmatch(r'(?:\d+-\d+|\d+)', pages)
    error = False
    if not check:
        error = True
    else:
        try:
            pages_int = int(pages)  # user selected a single page
            if pages_int == 0:
                error = True
        except ValueError:
            if int(pages.split('-')[0]) > int(pages.split('-')[1]) or int(pages.split('-')[0]) == 0:
                error = True
    if error:
        msg = 'Not a valid page range : {}'.format(pages)
        raise argparse.ArgumentTypeError(msg)
    else:
        return pages


def get_modified_time_diff(f):
    mod = time.ctime(os.path.getmtime(f))
    mod_time = datetime.strptime(mod, '%a %b %d %H:%M:%S %Y')
    return (datetime.now() - mod_time).total_seconds()


# Generated a document url from scribd's explore page
def generate_random_document():
    logging.getLogger('requests').setLevel(logging.ERROR)
    logging.getLogger('urllib3').setLevel(logging.ERROR)

    Categories = [
        'https://www.scribd.com/docs/Science-Tech/Tech',
        'https://www.scribd.com/docs/Career-Money/Entrepreneurship',
        'https://www.scribd.com/docs/Career-Money/Leadership-Mentoring'
    ]

    resp = requests.get(random.choice(Categories))
    urls = re.findall(r'https://www.scribd.com/(?:doc|document|presentation)/\d+', resp.text)
    return random.choice(list(set(urls)))
