import requests
from selenium.common.exceptions import NoSuchElementException

from retailers.base_retailer import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from settings import CHROMEDRIVER_PATH


class Ozon(Retailer):
    retailer_name = 'OZON'
    expected_string = 'Товара нет в продаже'

    ps5_url = 'https://www.ozon.ru/product/igrovaya-konsol-playstation-5-belyy-178337786/'
    # ps5_url = 'https://www.ozon.ru/product/igrovaya-konsol-microsoft-xbox-one-microsoft-s-1tb-forza-horizon-4-lego-speed-champions-171825423/?stat=YW5fMQ%3D%3D'

    @classmethod
    def check_status(cls):
        super().on_check_status()

        try:
            driver = webdriver.Chrome(CHROMEDRIVER_PATH)
            driver.get(cls.ps5_url)

            elem = driver.find_element_by_class_name('fake-sale-block')

            if elem.text != cls.expected_string:
                raise UnexpectedData(f'UnexpectedData: найдена строка {elem.text} вместо '
                                     f'ожидаемой {cls.expected_string} ({cls.retailer_name})')
        except NoSuchElementException:
            raise UnexpectedData(f'UnexpectedData: selenium ничего не нашел, а ДОЛЖЕН БЫЛ! ({cls.retailer_name})')
        else:
            logging.info(f'Надпись на месте ({cls.retailer_name})')
            super().on_check_status_end()
        finally:
            driver.close()
