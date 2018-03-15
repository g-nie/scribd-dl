# -*- coding: utf-8 -*-

import argparse
import re
import os
import time
from datetime import datetime


class GreaterThanLastPageError(Exception):
    def __init__(self):
        Exception.__init__(self, "Given page cannot be greater than document\'s last page")


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


# Returns seconds past since the last file modification
def get_modified_time_diff(f):
    mod = time.ctime(os.path.getmtime(f))
    mod_time = datetime.strptime(mod, '%a %b %d %H:%M:%S %Y')
    return (datetime.now() - mod_time).total_seconds()
