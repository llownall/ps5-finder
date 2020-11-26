from selenium.common.exceptions import NoSuchElementException

from retailers.base_retailer import *
from website import load_page_and_return_driver


class DNS(Retailer):
    retailer_name = 'ДНС'

    ps5_url = 'https://www.dns-shop.ru/product/2645e72c6fca1b80/igrovaa-konsol-playstation-5/'

    # ps5_url = 'https://www.dns-shop.ru/product/040b40013e6b3332/igrovaa-konsol-playstation-4-slim-black-1-tb--3-igry/'

    @classmethod
    def check_status(cls):
        super().on_check_status()

        driver = load_page_and_return_driver(cls.ps5_url)
        try:
            elem = driver.find_element_by_class_name('product-card-price__current')
        except NoSuchElementException:
            cls.save_screenshot(driver)
            logging.info(f'Selenium ничего не нашел')
            super().on_check_status_end()
        else:
            cls.save_screenshot(driver)
            raise InStock(f'InStock: {elem.text[:-2]}')
        finally:
            driver.close()
