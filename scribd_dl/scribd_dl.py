# -*- coding: utf-8 -*-
# pylint: disable=C0413

import re
import sys
import os
import time
import argparse
import logging
import traceback
from datetime import datetime
from ast import literal_eval
from io import BytesIO
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from PIL import Image
import img2pdf
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scribd_dl.utils import (
    valid_url,
    valid_pages,
    GreaterThanLastPageError,
    RestrictedDocumentError
)


class ScribdDL(object):

    # Replace with path to your chromedriver executable
    DRIVER_PATH = None  # Leave it as it is only if chromedriver is in PATH
    LOAD_TIME = 20  # Stop loading page after 20 seconds
    START = datetime.now()

    def __init__(self, args):
        self._args = args
        # LOG_FOLDER = os.path.join(os.path.expanduser("~"), 'scribd_logs')
        LOG_FOLDER = 'scribd_logs/'
        if not os.path.exists(LOG_FOLDER):
            os.makedirs(LOG_FOLDER)
        LOG_FILE = 'scribd.log'

        doc_id = re.search(r'(?P<id>\d+)', args.url).group('id')  # Use the document id for logging
        self._extra = {'doc_id': doc_id}
        self._logger = self._get_logger(LOG_FOLDER, LOG_FILE)
        self._driver = None
        self._doc_title = None

    @property
    def logger(self):
        return self._logger

    @property
    def driver(self):
        return self._driver

    @property
    def args(self):
        return self._args

    @property
    def doc_title(self):
        return self._doc_title

    @property
    def extra(self):
        return self._extra

    @logger.setter
    def logger(self, logger):
        self._logger = logger

    @args.setter
    def args(self, args):
        self._args = args

    @extra.setter
    def extra(self, extra):
        self._extra = extra

    def _get_logger(self, LOG_FOLDER, LOG_FILE):
        # Initialize and configure the logging system
        logging.basicConfig(level=logging.DEBUG,
                            format='(%(module)s) %(levelname)s [%(asctime)s] [%(doc_id)s]  %(message)s',
                            datefmt='%d-%m-%Y %H:%M:%S',
                            filename=os.path.join(LOG_FOLDER, LOG_FILE),
                            filemode='w')
        console_handler = logging.StreamHandler()
        # Use DEBUG logging level in console, if user selected --verbose
        console_level = logging.DEBUG if self._args.verbose else logging.INFO
        console_handler.setLevel(console_level)
        # -- To change console output format
        # console_formatter = logging.Formatter('%(levelname)s - %(message)s')
        # console_handler.setFormatter(console_formatter)
        logging.getLogger().addHandler(console_handler)
        logger = logging.getLogger(__name__)

        # Silence unnecessary third party debug messages
        logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.INFO)
        logging.getLogger('PIL.PngImagePlugin').setLevel(logging.INFO)
        logging.getLogger('PIL.Image').setLevel(logging.INFO)
        return logger

    def start_browser(self):
        # Initialize chromedriver and configure its options
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--log-level=3')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-infobars')
        options.add_argument("--window-size=1600,2020")
        logging.disable(logging.CRITICAL)
        if self.DRIVER_PATH:
            self._driver = webdriver.Chrome(self.DRIVER_PATH, options=options)
        else:
            self._driver = webdriver.Chrome(options=options)
        logging.disable(logging.NOTSET)

    def close_browser(self):  # Exit chromedriver
        self._driver.quit()

    def visit_page(self, url):
        self._logger.info('Visiting requested url', extra=self._extra)
        # Visit the requested url without waiting more than LOAD_TIME seconds
        self._driver.set_page_load_timeout(self.LOAD_TIME)
        try:
            self._driver.get(url)
        except TimeoutException:
            pass
        # Figure out whether the document can be fully accessed
        is_restricted = re.search(r"\"view_restricted\"\s*:\s*(?P<bool>true|false),", self._driver.page_source)
        try:
            is_restricted = literal_eval(is_restricted.group('bool').title())
        except AttributeError:
            is_restricted = False
        if is_restricted:
            raise RestrictedDocumentError

        retries = 0
        total_pages = None
        while retries < 3:  # try up to 3 times to get the total_pages element
            try:
                self._driver.get(url)
            except TimeoutException:
                pass
            try:
                total_pages = self._driver.find_element_by_xpath("//span[@class='total_pages']/span[2]")
                total_pages = total_pages.text.split()[1]
                break
            except NoSuchElementException:  # total_pages element not available, try again
                retries += 1
                time.sleep(2)
        if total_pages is None:
            raise NoSuchElementException

        self._doc_title = self._driver.title
        # Make document title safe for saving in the file system
        self._doc_title = re.sub('[^\w\-_\.\,\!\(\)\[\]\{\}\;\'\΄ ]', '_', self._doc_title)
        if self._args.pages:  # If user inserted page range
            try:
                first_page = int(self._args.pages.split('-')[0])
                last_page = int(self._args.pages.split('-')[1])
            except IndexError:  # user inserted only 1 page
                first_page = last_page = int(self._args.pages)
            if last_page > int(total_pages):
                self.close_browser()
                raise GreaterThanLastPageError
        else:  # Use the whole document
            first_page = 1
            last_page = int(total_pages)
        self._scroll_pages(first_page, last_page, total_pages)

    def _scroll_pages(self, first_page, last_page, total_pages):
        # Enter full screen mode
        self._driver.find_element_by_xpath("//button[@aria-label='Fullscreen']").click()
        Pages = []  # Holds the actual image bytes of each page
        to_process = last_page - first_page + 1  # Total pages to process
        processed = 0
        self._logger.info('Processing pages : %s-%s...', first_page, last_page, extra=self._extra)
        if first_page > 80:  # Inform the user that scrolling may take a while
            self._logger.info('Scrolling to page %s...', first_page, extra=self._extra)
        for counter in range(1, int(total_pages) + 1):
            if counter > last_page:
                break
            # Generate WebElement of the next page
            page = self._driver.find_element_by_xpath("//div[@id='outer_page_{}']".format(counter))
            self._driver.execute_script("arguments[0].scrollIntoView();", page)  # Scroll to it
            if counter < first_page:  # Keep scrolling if it hasn't reached the first_page
                continue
            processed += 1
            self._logger.debug('Processing page : %s of %s', counter, last_page, extra=self._extra)

            time.sleep(0.2)  # Sleep 0.2s in each scroll to fully load the page content
            img = Image.open(BytesIO(self._driver.get_screenshot_as_png()))  # Load screenshot in memory
            # Crop the image to the speified size
            img = img.crop((
                page.location['x'],
                page.location['y'],
                page.location['x'] + page.size['width'],
                page.location['y'] + page.size['height']
            ))
            # Append the byte array to List
            imgByteArr = BytesIO()
            img.save(imgByteArr, format='PNG')
            Pages.append(imgByteArr.getvalue())

            # Use this every <chunk> pages or in the last page
            if processed == to_process:
                # Merge the images into a temporary pdf file
                logging.disable(logging.CRITICAL)  # Disable img2pdf logging messages
                pdf_bytes = img2pdf.convert(Pages)
                logging.disable(logging.NOTSET)

                filename = '{}.pdf'.format(self._doc_title)
                with open(filename, 'wb') as file:
                    file.write(pdf_bytes)


def main():
    try:
        parser = argparse.ArgumentParser(description='Scribd document downloader')
        parser.add_argument('url', help='Url of the document', type=valid_url)  # Required positional argument
        parser.add_argument('-p', '--pages', help='Range of pages to be selected (e.g. 10-20)', type=valid_pages)
        parser.add_argument('-v', '--verbose', help='Show verbose output in terminal', action='store_true')
        args = parser.parse_args()
        url = args.url

        scribd = ScribdDL(args)
        logger = scribd.logger

        scribd.start_browser()
        driver = scribd.driver

        def _excepthook(*exc_info):  # Handle uncaught exceptions
            driver.quit()  # Close chromedriver when something unexpected occurs
            traceback.print_exception(*exc_info)
            # logger.error('An unexpected error occured. Exiting')  # --- Use this***
            sys.exit(1)
        sys.excepthook = _excepthook

        scribd.visit_page(url)
        scribd.close_browser()
        logger.info('Execution time : %s seconds', (datetime.now() - scribd.START).seconds, extra=scribd.extra)

    except KeyboardInterrupt:
        logger.warning('Interrupted.', extra=scribd.extra)
        try:
            driver.quit()
        except NameError:
            pass
        sys.exit(0)


if __name__ == '__main__':
    main()


# TODO : Mute "DEVTOOLS Listening..."
# TODO : Use _excepthook message in production
