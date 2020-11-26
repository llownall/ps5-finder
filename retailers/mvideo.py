from selenium.common.exceptions import NoSuchElementException

from retailers.base_retailer import *
from website import load_page_and_return_driver


class MVideo(Retailer):
    retailer_name = 'МВидео'
    expected_strings = [
        'Товар распродан',
        'Дата поступления неизвестна',
    ]

    ps5_url = 'https://www.mvideo.ru/products/igrovaya-konsol-sony-playstation-5-40073270?cityId=CityCZ_2246'

    # ps5_url = 'https://www.mvideo.ru/products/igrovaya-konsol-playstation-4-1tb-gts-hzd-spiderm-ps-3mes-40074231'

    @classmethod
    def check_status(cls):
        super().on_check_status()

        driver = load_page_and_return_driver(cls.ps5_url)
        try:
            elem = driver.find_element_by_class_name('fl-pdp-pay') \
                .find_element_by_class_name('c-notifications__title')

            if elem.text in cls.expected_strings:
                logging.info(f'Надпись на месте')
                super().on_check_status_end()
            else:
                cls.save_screenshot(driver)
                raise UnexpectedData(f'UnexpectedData: новая надпись!')
        except NoSuchElementException:
            cls.save_screenshot(driver)
            raise UnexpectedData(f'UnexpectedData: selenium ничего не нашел, а ДОЛЖЕН БЫЛ!')
        finally:
            driver.close()
