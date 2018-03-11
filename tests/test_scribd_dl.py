#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import sys
# import os
# import unittest
# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from scribd_dl import scribd_dl


# class TestScribd_dl(unittest.TestCase):
#     """Tests for `scribd_dl` package."""

#     def setUp(self):
#         """Set up test fixtures, if any."""

#     def tearDown(self):
#         """Tear down test fixtures, if any."""

#     def test_000_something(self):
#         """Test something."""

# if __name__ == '__main__':
#     unittest.main()


import unittest

import re
import sys
import os
import argparse
import logging
from datetime import datetime
from ast import literal_eval
from io import BytesIO
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from PIL import Image
from PyPDF2 import PdfFileMerger
import img2pdf


class TestScribd_dl(unittest.TestCase):

    def setUp(self):
        # Replace with path to your chromedriver executable
        self.DRIVER_PATH = None  # Leave it as it is only if chromedriver is in PATH
        self.LOAD_TIME = 20  # Stop loading page after 20 seconds
        self.LOG_FOLDER = '../logs/'
        if not os.path.exists(LOG_FOLDER):
            os.makedirs(LOG_FOLDER)
        self.LOG_FILE = 'scribd.log'
        self.START = datetime.now()
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--log-level=3')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-infobars')
        options.add_argument("--window-size=1600,2020")
        if DRIVER_PATH:
            driver = webdriver.Chrome(DRIVER_PATH, chrome_options=options)
        else:
            self.driver = webdriver.Chrome(chrome_options=options)

        # Initialize and configure the logging system
        logging.basicConfig(level=logging.INFO,
                            format='(%(module)s) %(levelname)s [%(asctime)s]  %(message)s',
                            datefmt='%d-%m-%Y %H:%M:%S')
        self.logger = logging.getLogger('scribd')
        # Silence unnecessary third party debug messages
        logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.INFO)
        logging.getLogger('PIL.PngImagePlugin').setLevel(logging.INFO)
        logging.getLogger('PIL.Image').setLevel(logging.INFO)
        # logging.getLogger('img2pdf').setLevel(logging.INFO)  # --------

    def tearDown(self):
        self.driver.delete_all_cookies()
        self.driver.quit()
        logger.info('Execution time : %s seconds', (datetime.now() - self.START).seconds)

    def visit(self, url):

    parser = argparse.ArgumentParser(description='Scribd document downloader')
    parser.add_argument('url', help='Url of the document')  # Required positional argument
    parser.add_argument('-p', '--pages', help='Range of pages to be selected (e.g. 10-20)', type=valid_range)
    parser.add_argument('-v', '--verbose', help='Show verbose output in terminal', action='store_true')

    URLS = [
        'https://www.scribd.com/document/352366744/Big-Data-A-Twenty-First-Century-Arms-Race',
        'https://www.scribd.com/document/106884805/Nebraska-Wing-Sep-2012',
        'https://www.scribd.com/doc/18587980/ARXAIA-G-Gymnasioy',
        'https://www.scribd.com/document/294632720/Connecticut-Wing-Apr-2014',
        'https://www.scribd.com/document/128090739/The-Bedan-Journal-of-Psychology-2013,
        'https://www.scribd.com/document/90403141/Social-Media-Strategy'
    ]
    URLS = URLS[:1]  # --------

    for url in URLS:
        self.visit(url)

    # Initialize chromedriver and configure its options
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--log-level=3')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-infobars')
    options.add_argument("--window-size=1600,2020")
    if DRIVER_PATH:
        driver = webdriver.Chrome(DRIVER_PATH, chrome_options=options)
    else:
        driver = webdriver.Chrome(chrome_options=options)

    logger.info('Visiting requested url')
    # Visit the requested url without waiting more than LOAD_TIME seconds
    driver.set_page_load_timeout(LOAD_TIME)
    try:
        driver.get(url)
    except TimeoutException:
        pass

    # Figure out whether the document can be fully accessed
    is_restricted = re.search(r"\"view_restricted\"\s*:\s*(?P<bool>true|false),", driver.page_source)
    is_restricted = literal_eval(is_restricted.group('bool').title())
    if is_restricted:
        logger.warning('This document is only a preview and not fully availabe for reading.')
        logger.warning('Please try another document.')
        sys.exit()

    # body = driver.find_element_by_xpath("//div[@role='document']")  # --- Send Keys here
    total_pages = driver.find_element_by_xpath("//span[@class='total_pages']/span[2]")
    total_pages = total_pages.text.split()[1]
    title = driver.title
    # Make document title safe for saving in the file system
    title = re.sub('[^\w\-_\.\,\!\(\)\[\]\{\}\;\'\΄ ]', '_', title)

    if args.pages:  # If user inserted page range
        first_page = int(args.pages.split('-')[0])
        last_page = int(args.pages.split('-')[1])
        if last_page > int(total_pages):
            logger.warning('Given page (%s) cannot be greater than document\'s last page (%s)',
                           last_page, total_pages)
            sys.exit()
    else:
        first_page = 1
        last_page = int(total_pages)

    # Enter full screen mode
    driver.find_element_by_xpath("//button[@aria-label='Fullscreen']").click()

    Pages = []  # Holds the actual image bytes of each page
    chunk = 10  # After N pages, save them from memnory to temporary pdfs in the disk
    Temporary = []  # Holds the temporary pdfs. Will be used if selected page range >= chunk
    to_process = last_page - first_page + 1  # Total pages to process
    chunk_counter = 1
    processed = 0
    logger.info('Processing pages : %s-%s...', first_page, last_page)
    if first_page > 80:  # Inform the user that scrolling may take a while
        logger.info('Scrolling to page %s...', first_page)
    for counter in range(1, int(total_pages) + 1):
        if counter > last_page:
            break
        # Generate WebElement of the next page
        page = driver.find_element_by_xpath(f"//div[@id='outer_page_{counter}']")
        driver.execute_script("arguments[0].scrollIntoView();", page)  # Scroll to it
        if counter < first_page:  # Keep scrolling if it hasn't reached the first_page
            continue
        processed += 1
        logger.debug('Processing page : %s of %s', counter, last_page)

        # Extract information about the dimensions of the page
        location = page.location
        size = page.size
        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']
        img = Image.open(BytesIO(driver.get_screenshot_as_png()))  # Load screenshot in memory
        img = img.crop((left, top, right, bottom))  # Crop the image to the speified size
        # Append the byte array to List
        imgByteArr = BytesIO()
        img.save(imgByteArr, format='PNG')
        Pages.append(imgByteArr.getvalue())

        # Use this every <chunk> pages or in the last page
        if (processed % chunk == 0) or (processed == to_process):
            # Merge the images into a temporary pdf file
            pdf_bytes = img2pdf.convert(Pages)
            filename = 'tmp_{}.pdf'.format(chunk_counter)
            with open(filename, 'wb') as file:
                file.write(pdf_bytes)
            Temporary.append(filename)
            Pages.clear()  # Release memory used for image storing
            chunk_counter += 1

    # Merge all the temporary pdfs into one
    merger = PdfFileMerger()
    for pdf in Temporary:
        merger.append(pdf)
    drive = os.path.abspath(os.sep)
    path = '{}.pdf'.format(title)
    merger.write(f'{title}.pdf')
    merger.close()

    logger.info('Successfully downloaded : %s', path)
    for pdf in Temporary:  # Delete remained pdfs
        os.remove(pdf)

    # ---------- USE FOR DEBUGGING UNCAUGHT EXCEPTIONS
    # def excepthook(*exc_info):
    #     driver.quit()
    #     traceback.print_exception(*exc_info)
    #     print('An unexpected error occured, please try again')
    # sys.excepthook = excepthook

    # TODO : Mute DEVTOOLS Listening
    # TODO : Quit driver if exception occurs
    # TODO : logging.getLogger('img2pdf').setLevel(logging.INFO) not working
