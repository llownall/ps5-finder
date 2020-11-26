from selenium.common.exceptions import NoSuchElementException

from retailers.base_retailer import *
from website import load_page_and_return_driver


class Sony(Retailer):
    retailer_name = 'Sony Store'
    expected_string = 'Временно нет на складе'

    ps5_url = 'https://store.sony.ru/product/konsol-playstation-5-317406/'

    # ps5_url = 'https://store.sony.ru/product/igrovaya-konsol-playstation-4-pro-1-tb-s-komplektom-igr-316844/'

    @classmethod
    def check_status(cls):
        super().on_check_status()

        driver = load_page_and_return_driver(cls.ps5_url)
        try:
            elem = driver.find_element_by_class_name('item-price-wrapper') \
                .find_element_by_class_name('a-preorder')

            if 'hide' in elem.get_attribute('class'):
                cls.save_screenshot(driver)
                raise UnexpectedData(f'UnexpectedData: надпись {cls.expected_string} стала скрыта. '
                                     f'Значит, другая надпись стала видимой...')
            else:
                logging.info(f'Надпись на месте')
                super().on_check_status_end()
        except NoSuchElementException:
            cls.save_screenshot(driver)
            raise UnexpectedData(f'UnexpectedData: selenium ничего не нашел, а ДОЛЖЕН БЫЛ!')
        finally:
            driver.close()
