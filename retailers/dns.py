import requests
from selenium.common.exceptions import NoSuchElementException

from retailers.base_retailer import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from settings import CHROMEDRIVER_PATH


class DNS(Retailer):
    retailer_name = 'ДНС'

    ps5_url = 'https://www.dns-shop.ru/product/2645e72c6fca1b80/igrovaa-konsol-playstation-5/'
    # ps5_url = 'https://www.dns-shop.ru/product/040b40013e6b3332/igrovaa-konsol-playstation-4-slim-black-1-tb--3-igry/'

    @classmethod
    def check_status(cls):
        super().on_check_status()

        try:
            driver = webdriver.Chrome(CHROMEDRIVER_PATH)
            driver.get(cls.ps5_url)
            elem = driver.find_element_by_class_name('product-card-price__current')
        except NoSuchElementException:
            logging.info(f'Selenium ничего не нашел ({cls.retailer_name})')
            super().on_check_status_end()
        else:
            raise InStock(f'InStock: {elem.text[:-2]} ({cls.retailer_name})')
        finally:
            driver.close()
