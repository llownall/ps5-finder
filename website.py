from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from settings import CHROMEDRIVER_PATH, PAGE_LOAD_TIMEOUT

chrome_options = Options()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')


def load_page_and_return_driver(url):
    driver = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=chrome_options)
    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    driver.get(url)
    return driver
