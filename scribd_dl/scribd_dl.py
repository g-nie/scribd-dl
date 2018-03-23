# -*- coding: utf-8 -*-
# pylint: disable=C0413

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
from scribd_dl.utils import (
    valid_url,
    valid_pages,
    GreaterThanLastPageError,
    RestrictedDocumentError
)


class ScribdDL(object):

    file_path = os.path.abspath(os.path.dirname(__file__))
    assets_dir = os.path.join(file_path, 'assets')

    DRIVER_PATH = None
    for f in os.listdir(assets_dir):
        if 'chromedriver' in f:
            DRIVER_PATH = f
    LOAD_TIME = 20  # Stop loading the page after 20 seconds
    START = datetime.now()

    def __init__(self, options):
        self.options = options
        self.url = None
        if options.get('pages'):
            self.pages = valid_pages(options['pages'])
        else:
            self.pages = None
        self.extra = None
        self.logger = self._get_logger()
        self.driver = None
        self.doc_title = None

    def set_pages(self, pages=None):
        if not pages:  # Select the whole document
            self.pages = None
        else:
            self.pages = valid_pages(pages)

    def _get_logger(self):
        # Initialize and configure the logging system
        if self.options.get('verbose') or self.options.get('log-level') == '1':
            console_level = logging.DEBUG
        elif self.options.get('log-level') == '2':
            console_level = logging.INFO
        elif self.options.get('log-level') == '3':
            console_level = logging.WARNING
        elif self.options.get('log-level') == '4':
            console_level = logging.ERROR
        elif self.options.get('log-level') == '5':
            console_level = logging.CRITICAL
        else:
            console_level = logging.INFO
        logging.basicConfig(
            stream=sys.stdout,
            level=console_level,
            format='[%(label)s]  %(message)s',
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
            self.driver = webdriver.Chrome(executable_path=self.DRIVER_PATH, options=options)
        else:  # search for chromedriver in PATH
            try:
                self.driver = webdriver.Chrome(options=options)
            except ConnectionResetError as e:
                self.logger.error('Failed to start webdriver: %s', str(e), extra={'label': 'error'})
                # sys.exit(1)
            except WebDriverException:
                self.logger.error('Chromedriver needs to be in assets directory or in PATH', extra={'label': 'error'})
                # sys.exit(1)
        self.driver.set_page_load_timeout(self.LOAD_TIME)

    def _cclose_browser(self):  # Exit chromedriver
        if not self.options.get('testing'):  # Don't close the driver if called by tests
            self.driver.quit()

    def close(self):  # Exit chromedriver without checking
        self.driver.quit()

    @staticmethod
    def _edit_title(title):
        # Make document title safe for saving in the file system
        edited = re.sub('[^\w\-_\.\,\!\(\)\[\]\{\}\;\'\΄ ]', '_', title)
        if ' ' in edited.strip() and len(edited.split(' ')) >= 4:
            edited = ' '.join(edited.split(' ')[:4])
        else:
            edited = edited[:30]
        return edited

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def download(self, url_list):
        if not isinstance(url_list, list):
            raise ValueError('url has to be of type list, not %s', type(url_list))
        if not self.driver:
            self.start_browser()
        for url in url_list:
            self._process_url(url)

    def _process_url(self, url):
        self.url = valid_url(url)
        doc_id = re.search(r'(?P<id>\d+)', url).group('id') if self.url else None
        self.extra = {'label': doc_id}

        self.logger.info('Visiting requested url', extra=self.extra)
        retries = 0
        total_pages = None
        while retries < 2:  # Retry up to 2 times to extract the total_pages element
            try:
                self.driver.get(self.url)  # Visit the requested url without waiting more than LOAD_TIME seconds
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

        self.doc_title = self.driver.title
        if self.pages:  # If user inserted page range
            try:
                first_page = int(self.pages.split('-')[0])
                last_page = int(self.pages.split('-')[1])
            except IndexError:  # user inserted only 1 page
                first_page = last_page = int(self.pages)
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
        sleep_time = 1.0
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

                doc_title_edited = self._edit_title(self.doc_title)
                filename = '{}-{}.pdf'.format(doc_title_edited, self.extra['label'])
                with open(filename, 'wb') as file:
                    file.write(pdf_bytes)
                self.logger.info('Destination: %s', filename, extra=self.extra)
            else:
                # Calculate sleep time based on the size of the images already visited
                img_size = imgByteArr.tell()  # The size of the image in bytes (an integer)
                Sizes.append(img_size)
                current_mean = sum(Sizes) / len(Sizes)
                sleep_time = round(0.2 + (current_mean / 2000000), 5)  # --- Tweak it?
                sleep_time = 1.2 if sleep_time > 1.2 else sleep_time


if __name__ == '__main__':
    import scribd_dl  # use __init__ main()
    scribd_dl.main()


# TODO : Mute "DEVTOOLS Listening..."
