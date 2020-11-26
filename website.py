import time

from selenium import webdriver

from settings import CHROMEDRIVER_PATH, PAGE_LOAD_TIMEOUT, AFTER_LOAD_PAUSE


options = webdriver.ChromeOptions()
# options.add_argument('headless')


def load_page_and_return_driver(url):
    driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)
    driver.set_window_size(1920, 969)
    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    driver.get(url)
    time.sleep(AFTER_LOAD_PAUSE)
    return driver
