from selenium.common.exceptions import NoSuchElementException

from retailers.base_retailer import *
from website import load_page_and_return_driver


class Eldorado(Retailer):
    retailer_name = 'Эльдорадо'
    expected_string = 'Скоро в продаже'

    ps5_url = 'https://www.eldorado.ru/cat/detail/igrovaya-pristavka-sony-playstation-5/'

    # ps5_url = 'https://www.eldorado.ru/cat/detail/igrovaya-pristavka-xbox-one-microsoft-s-1tb-forza-horizon-4-lego-speed-champions/'

    @classmethod
    def check_status(cls):
        super().on_check_status()

        driver = load_page_and_return_driver(cls.ps5_url)
        try:
            elem = driver.find_element_by_class_name('bottomBlockContentRight') \
                .find_element_by_class_name('buy-box__status-label')
            if elem.text != cls.expected_string:
                cls.save_screenshot(driver)
                raise UnexpectedData(f'UnexpectedData: найдена строка {elem.text} вместо '
                                     f'ожидаемой {cls.expected_string}')
        except NoSuchElementException:
            cls.save_screenshot(driver)
            raise InStock(f'InStock: selenium ничего не нашел, а ДОЛЖЕН БЫЛ!')
        else:
            logging.info(f'Надпись на месте')
            super().on_check_status_end()
        finally:
            driver.close()
