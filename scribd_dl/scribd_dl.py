# -*- coding: utf-8 -*-

import re
import sys
import os
import argparse
import logging
import traceback
from datetime import datetime
from ast import literal_eval
from io import BytesIO
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from PIL import Image
from PyPDF2 import PdfFileMerger
import img2pdf


class ScribdDL(object):

    def __init__(self, args):
        self.START = datetime.now()
        self._args = args

        LOG_FOLDER = os.path.join(os.path.expanduser("~"), 'scribd_logs')
        if not os.path.exists(LOG_FOLDER):
            os.makedirs(LOG_FOLDER)
        LOG_FILE = 'scribd.log'

        doc_id = re.search(r'(?P<id>\d+)', args.url).group('id')
        extra = {'doc_id': doc_id}
        self._logger = self._get_logger(LOG_FOLDER, LOG_FILE, extra)

        self._driver = None
        # Replace with path to your chromedriver executable
        self.DRIVER_PATH = None  # Leave it as it is only if chromedriver is in PATH
        self.LOAD_TIME = 20  # Stop loading page after 20 seconds
        self._doc_title = None
        self._Temporary = None
        self._chunk = 10  # After N pages, transfer images from menory to temporary pdfs in the disk

    @property
    def logger(self):
        return self._logger

    @property
    def driver(self):
        return self._driver

    @property
    def Temporary(self):
        return self._Temporary

    @property
    def args(self):
        return self._args

    @property
    def chunk(self):
        return self._chunk

    @property
    def doc_title(self):
        return self._doc_title

    @args.setter
    def args(self, args):
        self._args = args

    @chunk.setter
    def chunk(self, chunk):
        self._chunk = chunk

    # @doc_title.setter
    # def doc_title(self, doc_title):
    #     self._doc_title = doc_title

    def _get_logger(self, LOG_FOLDER, LOG_FILE, extra):
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
        logger = logging.LoggerAdapter(logger, extra)
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
        # options.add_argument('--disable-logging')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-infobars')
        options.add_argument("--window-size=1600,2020")
        if self.DRIVER_PATH:
            self._driver = webdriver.Chrome(self.DRIVER_PATH, options=options)
        else:
            self._driver = webdriver.Chrome(options=options)

    def close_browser(self):  # Exit chromedriver
        self._driver.delete_all_cookies()
        self._driver.quit()

    def visit_page(self, url):
        self._logger.info('Visiting requested url')
        # Visit the requested url without waiting more than LOAD_TIME seconds
        self._driver.set_page_load_timeout(self.LOAD_TIME)
        try:
            self._driver.get(url)
        except TimeoutException:
            pass
        # Figure out whether the document can be fully accessed
        is_restricted = re.search(r"\"view_restricted\"\s*:\s*(?P<bool>true|false),", self._driver.page_source)
        is_restricted = literal_eval(is_restricted.group('bool').title())
        if is_restricted:
            self._logger.warning('This document is only a preview and not fully availabe for reading.')
            self._logger.warning('Please try another document.')
            self.close_browser()
            sys.exit(1)
        # body = self._driver.find_element_by_xpath("//div[@role='document']")  # --- Send Keys here
        total_pages = self._driver.find_element_by_xpath("//span[@class='total_pages']/span[2]")
        total_pages = total_pages.text.split()[1]
        self._doc_title = self._driver.title
        # Make document title safe for saving in the file system
        self._doc_title = re.sub('[^\w\-_\.\,\!\(\)\[\]\{\}\;\'\΄ ]', '_', self._doc_title)
        if self._args.pages:  # If user inserted page range
            first_page = int(self._args.pages.split('-')[0])
            last_page = int(self._args.pages.split('-')[1])
            if last_page > int(total_pages):
                self._logger.warning('Given page (%s) cannot be greater than document\'s last page (%s)',
                                     last_page, total_pages)
                self.close_browser()
                sys.exit(1)
        else:
            first_page = 1
            last_page = int(total_pages)
        self._scroll_pages(first_page, last_page, total_pages)

    def _scroll_pages(self, first_page, last_page, total_pages):
        # Enter full screen mode
        self._driver.find_element_by_xpath("//button[@aria-label='Fullscreen']").click()
        Pages = []  # Holds the actual image bytes of each page
        self._Temporary = []  # Holds the temporary pdfs. Will be used if selected page range >= chunk
        to_process = last_page - first_page + 1  # Total pages to process
        chunk_counter = 1
        processed = 0
        self._logger.info('Processing pages : %s-%s...', first_page, last_page)
        if first_page > 80:  # Inform the user that scrolling may take a while
            self._logger.info('Scrolling to page %s...', first_page)
        for counter in range(1, int(total_pages) + 1):
            if counter > last_page:
                break
            # Generate WebElement of the next page
            page = self._driver.find_element_by_xpath("//div[@id='outer_page_{}']".format(counter))
            self._driver.execute_script("arguments[0].scrollIntoView();", page)  # Scroll to it
            if counter < first_page:  # Keep scrolling if it hasn't reached the first_page
                continue
            processed += 1
            self._logger.debug('Processing page : %s of %s', counter, last_page)

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
            if (processed % self._chunk == 0) or (processed == to_process):
                # Merge the images into a temporary pdf file
                logging.disable(logging.CRITICAL)  # Disable img2pdf logging messages
                pdf_bytes = img2pdf.convert(Pages)
                logging.disable(logging.NOTSET)

                filename = 'tmp_{}.pdf'.format(chunk_counter)
                with open(filename, 'wb') as file:
                    file.write(pdf_bytes)
                self._Temporary.append(filename)
                Pages.clear()  # Release memory used for image storing
                chunk_counter += 1

    # Merge all the temporary pdfs into one
    def merge(self):
        merger = PdfFileMerger()
        for pdf in self._Temporary:
            merger.append(pdf)
        path = '{}.pdf'.format(self._doc_title)
        merger.write('{}.pdf'.format(self._doc_title))
        merger.close()
        print()
        self._logger.info('Successfully downloaded : %s', path)
        for pdf in self._Temporary:  # Delete remained pdfs
            os.remove(pdf)


def main():
    try:
        # Make sure input url is of valid format
        def valid_url(u):
            check = re.match(r'https://www.scribd.com/(?:doc|document)/\d+/.*', u)
            if check:
                return u
            else:
                msg = 'Not a valid document url : {}'.format(u)
                raise argparse.ArgumentTypeError(msg)

        # Make sure input page range is of valid format
        def valid_range(pages):
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

        parser = argparse.ArgumentParser(description='Scribd document downloader')
        parser.add_argument('url', help='Url of the document', type=valid_url)  # Required positional argument
        parser.add_argument('-p', '--pages', help='Range of pages to be selected (e.g. 10-20)', type=valid_range)
        parser.add_argument('-v', '--verbose', help='Show verbose output in terminal', action='store_true')
        args = parser.parse_args()
        url = args.url
        # doc_id = re.search(r'(?P<id>\d+)', url).group('id')  # Use the document id for logging

        # scribd = ScribdDL(args, {'doc_id': doc_id})
        scribd = ScribdDL(args)
        logger = scribd.logger

        scribd.start_browser()
        driver = scribd.driver

        def _excepthook(*exc_info):  # Handle uncaught exceptions
            driver.quit()  # Close chromedriver when something unexpected occurs
            if scribd.Temporary:
                for t in scribd.Temporary:  # Remove temp pdf files
                    os.remove(t)
            traceback.print_exception(*exc_info)
            # logger.error('An unexpected error occured. Exiting')  # --- Use this***
            sys.exit(1)
        sys.excepthook = _excepthook

        scribd.visit_page(url)
        scribd.merge()
        scribd.close_browser()
        logger.info('Execution time : %s seconds', (datetime.now() - scribd.START).seconds)

    except KeyboardInterrupt:
        logger.warning('Interrupted.')
        try:
            driver.quit()
        except NameError:
            pass
        try:
            for t in scribd.Temporary:  # Remove temp pdf files
                os.remove(t)
        except (NameError, TypeError):
            pass
        sys.exit(0)


if __name__ == '__main__':
    main()


# TODO : Mute DEVTOOLS Listening
# TODO : Reduce instance attributes
