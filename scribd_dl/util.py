import argparse
import re
import os
import time
from datetime import datetime


# Make sure input url is of valid format
def valid_url(u):
    # check = re.match(r'(https://)?www.scribd.com/(?:doc|document)/\d+.*', u)
    check = re.match(r'(https://)?www.scribd.com/(?:doc|document)/\d+(?:/.*|$)', u)
    if check:
        return u
    else:
        msg = 'Not a valid document url : {}'.format(u)
        raise argparse.ArgumentTypeError(msg)


# Make sure input page range is of valid format
def valid_pages(pages):
    check = re.match(r'\d+-\d+', pages)
    error = False
    if not check:
        error = True
    elif int(pages.split('-')[0]) > int(pages.split('-')[1]):
        error = True
    elif int(pages.split('-')[0]) == 0:
        error = True
    if error:
        msg = 'Not a valid page range : {}'.format(pages)
        raise argparse.ArgumentTypeError(msg)
    else:
        return pages


# # Returns True when given valid combination of args
# def valid_args(args):
#     if args.url and args.pages and args.verbose in ('True', 'False'):
#         return True
#     return False


# Returns seconds past since the last file modification
def get_modified_time_diff(f):
    mod = time.ctime(os.path.getmtime(f))
    mod_time = datetime.strptime(mod, '%a %b %d %H:%M:%S %Y')
    return (datetime.now() - mod_time).total_seconds()
