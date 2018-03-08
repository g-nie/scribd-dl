import time
import re
import sys
import os
import traceback
import argparse
from ast import literal_eval
from io import BytesIO
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from PIL import Image
from PyPDF2 import PdfFileMerger
import img2pdf


def valid_url(u):
    check = re.match(r'https://www.scribd.com/(?:doc|document)/\d+/.*', url)
    if check:
        return url
    else:
        msg = f'Not a valid document url : {u}'
        raise argparse.ArgumentTypeError(msg)


def valid_range(pages):
    check = re.match(r'\d+-\d+', pages)
    error = False
    if not check:
        error = True
    elif int(pages.split('-')[0]) > int(pages.split('-')[1]):
        error = True
    if error:
        msg = f'Not a valid page range : {pages}'
        raise argparse.ArgumentTypeError(msg)
    else:
        return pages


parser = argparse.ArgumentParser(description='Scribd document downloader')
parser.add_argument('-u', '--url', help='Url of the document', required=True, type=valid_url)
parser.add_argument('-p', '--pages', help='Range of pages to be selected (e.g. 10-20)', type=valid_range)
args = parser.parse_args()

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


def excepthook(*exc_info):
    driver.quit()
    traceback.print_exception(*exc_info)  # ----------
    print('An unexpected error occured, please try again')


sys.excepthook = excepthook
print()

url = args.url
# url = 'https://www.scribd.com/document/106884805/Nebraska-Wing-Sep-2012'  # 16 pages
# url = 'https://www.scribd.com/doc/18587980/ARXAIA-G-Gymnasioy'  # 456 pages
# url = 'https://www.scribd.com/document/294632720/Connecticut-Wing-Apr-2014'  # 21 pages
# url = 'https://www.scribd.com/document/128090739/The-Bedan-Journal-of-Psychology-2013'
# url = 'https://www.scribd.com/document/90403141/Social-Media-Strategy'  # 22 pages

LOAD_TIME = 20
driver.set_page_load_timeout(LOAD_TIME)  # Stop loading the page after n seconds
try:
    driver.get(url)
except TimeoutException:
    pass

is_restricted = re.search(r"\"view_restricted\"\s*:\s*(?P<bool>true|false),", driver.page_source)
is_restricted = literal_eval(is_restricted.group('bool').title())
if is_restricted:
    print('This document is only a preview and not fully availabe for reading.')
    print('Please try another document.')
    sys.exit()

# body = driver.find_element_by_xpath("//div[@role='document']")  # ********** To Send Keys
total_pages = driver.find_element_by_xpath("//span[@class='total_pages']/span[2]")
total_pages = total_pages.text.split()[1]

title = driver.title
print(title)

if args.pages:
    first_page = int(args.pages.split('-')[0])
    last_page = int(args.pages.split('-')[1])
    if last_page > int(total_pages):
        print(f'Given page ({last_page}) cannot be greater than document\'s last page ({total_pages})')
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
if first_page > 80:
    print(f'Scrolling to page {first_page}...')
for counter in range(1, int(total_pages) + 1):
    if counter > last_page:
        break
    page = driver.find_element_by_xpath(f"//div[@id='outer_page_{counter}']")
    driver.execute_script("arguments[0].scrollIntoView();", page)
    if counter < first_page:
        continue
    processed += 1
    print(f'Processing page : {counter} of {last_page}')

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
        filename = f'tmp_{chunk_counter}.pdf'
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
path = f'{drive}Users\\{os.getlogin()}\\Desktop\\{title}.pdf'
merger.write(path)
# merger.write(f'{title}.pdf')
merger.close()
for pdf in Tmp_files:
    os.remove(pdf)

driver.quit()
