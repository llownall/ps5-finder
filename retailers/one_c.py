from selenium.common.exceptions import NoSuchElementException

from retailers.base_retailer import *
from website import load_page_and_return_driver


class OneC(Retailer):
    retailer_name = '1C Интерес'
    expected_string = 'Нет в наличии'
    in_stock_string = 'В наличии'

    ps5_url = 'https://www.1c-interes.ru/catalog/all6969/30328282/'

    # ps5_url = 'https://www.1c-interes.ru/catalog/all6963/28429893/'

    @classmethod
    def check_status(cls):
        super().on_check_status()

        driver = load_page_and_return_driver(cls.ps5_url)
        try:
            elem = driver.find_element_by_class_name('product_card_detail') \
                .find_element_by_class_name('popup-available')

            if elem.text != cls.expected_string:
                if elem.text == cls.in_stock_string:
                    cls.save_screenshot(driver)
                    raise InStock(f'InStock: {cls.retailer_name}')
                else:
                    cls.save_screenshot(driver)
                    raise UnexpectedData(f'UnexpectedData: найдена строка {elem.text} вместо '
                                         f'ожидаемой {cls.expected_string}')
        except NoSuchElementException:
            cls.save_screenshot(driver)
            raise UnexpectedData(f'UnexpectedData: selenium ничего не нашел, а ДОЛЖЕН БЫЛ!')
        else:
            logging.info(f'Надпись на месте')
            super().on_check_status_end()
        finally:
            driver.close()
