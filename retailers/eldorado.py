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

        try:
            driver = load_page_and_return_driver(cls.ps5_url)
            elem = driver.find_element_by_class_name('bottomBlockContentRight')\
                .find_element_by_class_name('buy-box__status-label')
            if elem.text != cls.expected_string:
                raise UnexpectedData(f'UnexpectedData: найдена строка {elem.text} вместо '
                                     f'ожидаемой {cls.expected_string} ({cls.retailer_name})')
        except NoSuchElementException:
            raise InStock(f'InStock: selenium ничего не нашел, а ДОЛЖЕН БЫЛ! ({cls.retailer_name})')
        else:
            logging.info(f'Надпись на месте ({cls.retailer_name})')
            super().on_check_status_end()
        finally:
            driver.close()
