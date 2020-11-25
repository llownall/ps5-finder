import requests
from selenium.common.exceptions import NoSuchElementException

from retailers.base_retailer import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from settings import CHROMEDRIVER_PATH


class OneC(Retailer):
    retailer_name = '1C Интерес'
    expected_string = 'Нет в наличии'
    in_stock_string = 'В наличии'

    ps5_url = 'https://www.1c-interes.ru/catalog/all6969/30328282/'
    # ps5_url = 'https://www.1c-interes.ru/catalog/all6963/28429893/'

    @classmethod
    def check_status(cls):
        super().on_check_status()

        try:
            driver = webdriver.Chrome(CHROMEDRIVER_PATH)
            driver.get(cls.ps5_url)

            elem = driver.find_element_by_class_name('product_card_detail') \
                .find_element_by_class_name('popup-available')

            if elem.text != cls.expected_string:
                if elem.text == cls.in_stock_string:
                    raise InStock(f'InStock: {cls.retailer_name}')
                else:
                    raise UnexpectedData(f'UnexpectedData: найдена строка {elem.text} вместо '
                                         f'ожидаемой {cls.expected_string} ({cls.retailer_name})')
        except NoSuchElementException:
            raise UnexpectedData(f'UnexpectedData: selenium ничего не нашел, а ДОЛЖЕН БЫЛ! ({cls.retailer_name})')
        else:
            logging.info(f'Надпись на месте ({cls.retailer_name})')
            super().on_check_status_end()
        finally:
            driver.close()
