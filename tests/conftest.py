import pytest
from selenium import webdriver


# def pytest_addoption(parser):
#     parser.addoption("--driver", action="store", default="chrome", help="Type in browser type")
#     parser.addoption("--url", action="store", default="https://qa.moodle.net/", help="url")
#     parser.addoption("--username", action="store", default="manager", help="username")
#     parser.addoption("--password", action="store", default="test", help="password")


@pytest.fixture(scope='module', autouse=True)
# def browser(request):
def browser():
    # driver = request.config.getoption("--driver")
    # if driver == 'chrome':
    #     driver = webdriver.Chrome()
    #     driver.get("about:blank")
    #     driver.implicitly_wait(10)
    #     driver.maximize_window()
    # else:
    #     print('only chrome is supported at the moment')
    #     return driver

    # setUp
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--log-level=3')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-infobars')
    options.add_argument("--window-size=1600,2020")
    driver = webdriver.Chrome(options=options)
    yield driver

    # tearDown
    driver.delete_all_cookies()
    driver.quit()
