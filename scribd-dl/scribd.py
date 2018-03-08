import time
import re
import sys
import os
import traceback
import argparse
import logging
from ast import literal_eval
from io import BytesIO
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from PIL import Image
from PyPDF2 import PdfFileMerger
import img2pdf


logging_file_level = logging.DEBUG
LOAD_TIME = 20  # Stop loading page after 20 page
logfolder = './logs/'
if not os.path.exists(logfolder):
    os.makedirs(logfolder)


def valid_url(u):
    check = re.match(r'https://www.scribd.com/(?:doc|document)/\d+/.*', u)
    if check:
        return u
    else:
        msg = 'Not a valid document url : {}'.format(u)
        raise argparse.ArgumentTypeError(msg)


def valid_range(pages):
    check = re.match(r'\d+-\d+', pages)
    error = False
    if not check:
        error = True
    elif int(pages.split('-')[0]) > int(pages.split('-')[1]):
        error = True
    if error:
        msg = 'Not a valid page range : {}'.format(pages)
        raise argparse.ArgumentTypeError(msg)
    else:
        return pages


parser = argparse.ArgumentParser(description='Scribd document downloader')
parser.add_argument('-u', '--url', help='Url of the document', required=True, type=valid_url)
parser.add_argument('-p', '--pages', help='Range of pages to be selected (e.g. 10-20)', type=valid_range)
parser.add_argument('-v', '--verbose', help='Show verbose output in terminal', action='store_true')

args = parser.parse_args()
url = args.url
log_level = logging.DEBUG if args.verbose else logging.INFO

# WORS BUT WITH ROOT DEBUG OUTPUT IN .LOG + DEVTOOLS...

# Initialize and set up the logging system
url_id = re.search(r'(?P<id>\d+)', url).group('id')
logging.basicConfig(level=logging.DEBUG,
                    # format='%(levelname)s [%(asctime)s] [{}]  %(message)s'.format(url_id),
                    format='%(name)s %(levelname)s [%(asctime)s] [{}]  %(message)s'.format(url_id),
                    datefmt='%d-%m-%Y %H:%M:%S',
                    filename='{}scribd.log'.format(logfolder),
                    filemode='w')
console_handler = logging.StreamHandler()
console_handler.setLevel(log_level)
# console_formatter = logging.Formatter('%(levelname)s - %(message)s')
# console_handler.setFormatter(console_formatter)
logging.getLogger('').addHandler(console_handler)
logger = logging.getLogger('scribd')

# Silence unnecessary third party debug messages
logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.INFO)
logging.getLogger('PIL.PngImagePlugin').setLevel(logging.INFO)
logging.getLogger('PIL.Image').setLevel(logging.INFO)


# user_agent = "Mozilla/5.0 (Linux; Android 4.4.2; ASUS_T00J Build/KVT49L) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Safari/537.36"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"
options = webdriver.ChromeOptions()
options.add_argument('--user-agent={}'.format(user_agent))
options.add_argument('--headless')
options.add_argument('--log-level=3')
options.add_argument('--disable-logging')
options.add_argument('--disable-gpu')
options.add_argument('--disable-infobars')
# options.add_argument("--start-maximized")  # OXI STO HEADLESS
options.add_argument("--window-size=1600,2020")  # STO HEADLESS
driver = webdriver.Chrome(options=options, service_args=["--log-path=chromedriver.log"])


# ---------- FOR DEBUG
def excepthook(*exc_info):
    driver.quit()
    traceback.print_exception(*exc_info)
    print('An unexpected error occured, please try again')


sys.excepthook = excepthook
# print()

# url = 'https://www.scribd.com/document/106884805/Nebraska-Wing-Sep-2012'  # 16 pages
# url = 'https://www.scribd.com/doc/18587980/ARXAIA-G-Gymnasioy'  # 456 pages
# url = 'https://www.scribd.com/document/294632720/Connecticut-Wing-Apr-2014'  # 21 pages
# url = 'https://www.scribd.com/document/128090739/The-Bedan-Journal-of-Psychology-2013'
# url = 'https://www.scribd.com/document/90403141/Social-Media-Strategy'  # 22 pages

driver.set_page_load_timeout(LOAD_TIME)
try:
    driver.get(url)
except TimeoutException:
    pass

is_restricted = re.search(r"\"view_restricted\"\s*:\s*(?P<bool>true|false),", driver.page_source)
is_restricted = literal_eval(is_restricted.group('bool').title())
if is_restricted:
    logger.warning('This document is only a preview and not fully availabe for reading.')
    logger.warning('Please try another document.')
    sys.exit()

# body = driver.find_element_by_xpath("//div[@role='document']")  # ** Send Keys here
total_pages = driver.find_element_by_xpath("//span[@class='total_pages']/span[2]")
total_pages = total_pages.text.split()[1]

title = driver.title
logger.info('Document tile : %s', title)

if args.pages:
    first_page = int(args.pages.split('-')[0])
    last_page = int(args.pages.split('-')[1])
    if last_page > int(total_pages):
        logger.warning('Given page (%s) cannot be greater than document\'s last page (%s)',
                       last_page, total_pages)
        sys.exit()
else:
    first_page = 1
    last_page = int(total_pages)

driver.find_element_by_xpath("//button[@aria-label='Fullscreen']").click()

Pages = []
Tmp_files = []
to_process = last_page - first_page + 1
chunk = 10
chunk_counter = 1
processed = 0
logger.info('Processing pages : %s-%s...', first_page, last_page)
if first_page > 80:
    logger.info('Scrolling to page %s...', first_page)
for counter in range(1, int(total_pages) + 1):
    if counter > last_page:
        break
    page = driver.find_element_by_xpath(f"//div[@id='outer_page_{counter}']")
    driver.execute_script("arguments[0].scrollIntoView();", page)
    if counter < first_page:
        continue
    processed += 1
    # print('Processing page : {} of {}'.format(counter, last_page), end='\r')
    logger.debug('Processing page : %s of %s', counter, last_page)

    location = page.location
    size = page.size
    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']
    img = Image.open(BytesIO(driver.get_screenshot_as_png()))  # load screenshot in memory
    img = img.crop((left, top, right, bottom))  # defines crop points
    # Append the byte array to List
    imgByteArr = BytesIO()
    img.save(imgByteArr, format='PNG')
    Pages.append(imgByteArr.getvalue())

    if (processed % chunk == 0) or (processed == to_process):
        # Merge the images into a pdf file
        pdf_bytes = img2pdf.convert(Pages)
        filename = 'tmp_{}.pdf'.format(chunk_counter)
        with open(filename, 'wb') as file:
            file.write(pdf_bytes)
        Tmp_files.append(filename)
        Pages.clear()
        chunk_counter += 1

merger = PdfFileMerger()
for pdf in Tmp_files:
    merger.append(pdf)
title = re.sub('[^\w\-_\.\,\!\(\)\[\]\{\}\;\'\΄ ]', '_', title)
drive = os.path.abspath(os.sep)
path = '{}Users\\{}\\Desktop\\{}.pdf'.format(drive, os.getlogin(), title)  # Change -----
# path = '{}.pdf'.format(title)
merger.write(path)
# merger.write(f'{title}.pdf')
merger.close()
logger.debug('Sucessfully downloaded : %s', path)
for pdf in Tmp_files:
    os.remove(pdf)

driver.quit()
