# import pytest
# from selenium import webdriver


# def pytest_addoption(parser):
#     parser.addoption("--driver", action="store", default="chrome", help="Type in browser type")
#     parser.addoption("--url", action="store", default="https://qa.moodle.net/", help="url")
#     parser.addoption("--username", action="store", default="manager", help="username")
#     parser.addoption("--password", action="store", default="test", help="password")


# @pytest.fixture(scope='module', autouse=True)
# def browser(request):
#     # setUp
#     # driver = request.config.getoption("--driver")
#     # if driver == 'chrome':
#     #     driver = webdriver.Chrome()
#     #     driver.get("about:blank")
#     #     driver.implicitly_wait(10)
#     #     driver.maximize_window()
#     # else:
#     #     print('only chrome is supported at the moment')
#     #     return driver

#     driver = webdriver.Chrome()
#     driver.get("about:blank")
#     driver.implicitly_wait(10)
#     driver.maximize_window()

#     yield driver

#     # tearDown
#     driver.quit()
# #
