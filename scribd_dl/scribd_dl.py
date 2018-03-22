# -*- coding: utf-8 -*-

import re
import sys
import os
import time
import logging
from datetime import datetime
from ast import literal_eval
from io import BytesIO
from PIL import Image
import img2pdf
from selenium import webdriver
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    WebDriverException
)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scribd_dl.utils import GreaterThanLastPageError, RestrictedDocumentError  # pylint: disable=C0413


class ScribdDL(object):

    file_path = os.path.abspath(os.path.dirname(__file__))
    assets_dir = os.path.join(file_path, 'assets')

    DRIVER_PATH = None
    for f in os.listdir(assets_dir):
        if 'chromedriver' in f:
            DRIVER_PATH = f
    LOAD_TIME = 20  # Stop loading the page after 20 seconds
    START = datetime.now()

    def __init__(self, args):
        self._args = args
        doc_id = re.search(r'(?P<id>\d+)', args.url).group('id')
        self._extra = {'doc_id': doc_id}  # Use the document id for logging
        self._logger = self._get_logger()
        self._driver = None
        self._doc_title = None
        self._doc_title_edited = None

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

    @property
    def doc_title_edited(self):
        return self._doc_title_edited

    @logger.setter
    def logger(self, logger):
        self._logger = logger

    @extra.setter
    def extra(self, extra):
        self._extra = extra

    @doc_title_edited.setter
    def doc_title_edited(self, doc_title_edited):
        self._doc_title_edited = doc_title_edited

    def _get_logger(self):
        # Initialize and configure the logging system
        console_level = logging.DEBUG if self._args.verbose else logging.INFO
        logging.basicConfig(
            level=console_level,
            format='[%(doc_id)s]  %(message)s',
            datefmt='%d-%m-%Y %H:%M:%S'
        )
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

        if self.DRIVER_PATH:  # search for chromedriver in assets
            self._driver = webdriver.Chrome(executable_path=self.DRIVER_PATH, options=options)
        else:  # search for chromedriver in PATH
            try:
                self._driver = webdriver.Chrome(options=options)
            except ConnectionResetError as e:
                self.logger.error('Failed to start webdriver: %s', str(e))
                sys.exit(1)
            except WebDriverException:
                self.logger.error('Chromedriver needs to be in assets directory or in PATH')
                sys.exit(1)
        self.driver.set_page_load_timeout(self.LOAD_TIME)

    def _cclose_browser(self):  # Exit chromedriver
        try:  # Don't close the driver if called by tests
            t = self._args.testing  # noqa: F841 pylint: disable=W0612
        except AttributeError:
            self.driver.quit()

    def close_browser(self):  # Exit chromedriver without checking
        self.driver.quit()

    def _edit_title(self):
        # Make document title safe for saving in the file system
        edited = re.sub('[^\w\-_\.\,\!\(\)\[\]\{\}\;\'\΄ ]', '_', self.doc_title)
        if ' ' in edited.strip() and len(edited.split(' ')) >= 4:
            edited = ' '.join(edited.split(' ')[:4])
        else:
            edited = edited[:30]
        return edited

    def visit_page(self, url):
        self.logger.info('Visiting requested url', extra=self.extra)
        retries = 0
        total_pages = None
        while retries < 2:
            try:
                self.driver.get(url)  # Visit the requested url without waiting more than LOAD_TIME seconds
            except TimeoutException:
                pass
            # Figure out whether the document can be fully accessed
            is_restricted = re.search(r"\"view_restricted\"\s*:\s*(?P<bool>true|false),", self.driver.page_source)
            try:
                is_restricted = literal_eval(is_restricted.group('bool').title())
            except AttributeError:
                is_restricted = False
            if is_restricted:
                self._cclose_browser()
                raise RestrictedDocumentError
            try:  # Refresh the page in case it could not retrieve the total_pages element
                total_pages = self.driver.find_element_by_xpath("//span[@class='total_pages']/span[2]")
                total_pages = total_pages.text.split()[1]
                break
            except NoSuchElementException:  # total_pages element not available, try again
                retries += 1
                time.sleep(2)
        if total_pages is None:
            self._cclose_browser()
            raise NoSuchElementException
        total_pages = int(total_pages.replace(',', '').replace('.', ''))

        self._doc_title = self.driver.title
        if self._args.pages:  # If user inserted page range
            try:
                first_page = int(self._args.pages.split('-')[0])
                last_page = int(self._args.pages.split('-')[1])
            except IndexError:  # user inserted only 1 page
                first_page = last_page = int(self._args.pages)
            if last_page > total_pages:
                self._cclose_browser()
                raise GreaterThanLastPageError
        else:  # Use the whole document
            first_page = 1
            last_page = total_pages
        self._scroll_pages(first_page, last_page, total_pages)

    def _scroll_pages(self, first_page, last_page, total_pages):
        # Enter full screen mode
        fullscreen_xpath = "//button[@aria-label='Fullscreen']"
        self.driver.find_element_by_xpath(fullscreen_xpath).click()
        Pages = []  # Holds the actual image bytes of each page
        Sizes = []  # Holds the size in bytes (an integer) of each page
        to_process = last_page - first_page + 1  # Total pages to process
        processed = 0
        self.logger.info('Processing pages : %s-%s...', first_page, last_page, extra=self.extra)
        if first_page > 80:  # Inform the user that scrolling may take a while
            self.logger.info('Scrolling to page %s...', first_page, extra=self.extra)
        sleep_time = 1.2
        current_mean = 0
        for counter in range(1, total_pages + 1):
            if counter > last_page:
                break
            # Generate WebElement of the next page
            page = self.driver.find_element_by_xpath("//div[@id='outer_page_{}']".format(counter))
            self.driver.execute_script("arguments[0].scrollIntoView();", page)  # Scroll to it
            if counter < first_page:  # Keep scrolling if it hasn't reached the first_page
                continue
            processed += 1
            self.logger.debug('Processing page : %s of %s', counter, last_page, extra=self.extra)

            time.sleep(sleep_time)
            img = Image.open(BytesIO(self.driver.get_screenshot_as_png()))  # Save screenshot in memory

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

            if processed == to_process:  # If on the last page
                # Merge the images into a temporary pdf file
                logging.disable(logging.CRITICAL)  # Disable img2pdf logging messages
                pdf_bytes = img2pdf.convert(Pages)
                logging.disable(logging.NOTSET)

                if not self.doc_title_edited:  # calculate filename if not previously set
                    self.doc_title_edited = self._edit_title()
                filename = '{}-{}.pdf'.format(self.doc_title_edited, self.extra['doc_id'])
                with open(filename, 'wb') as file:
                    file.write(pdf_bytes)
                self.logger.info('Destination: %s', filename, extra=self.extra)
            else:
                # Calculate sleep time based on the size of the images already visited
                img_size = imgByteArr.tell()  # The size of the image in bytes (an integer)
                Sizes.append(img_size)
                current_mean = sum(Sizes) / len(Sizes)
                sleep_time = round(0.2 + (current_mean / 1000000), 5)


if __name__ == '__main__':
    import scribd_dl  # use __init__ main()
    scribd_dl.main()


# TODO : Restructure for API use
# TODO : Mute "DEVTOOLS Listening..."
