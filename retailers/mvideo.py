import requests

from retailers.base_retailer import *
from bs4 import BeautifulSoup


class MVideo(Retailer):
    retailer_name = 'МВидео'
    expected_string = 'Товар распродан'

    ps5_url = 'https://www.mvideo.ru/products/igrovaya-konsol-sony-playstation-5-40073270?cityId=CityCZ_2246'
    # ps5_url = 'https://www.mvideo.ru/products/igrovaya-konsol-playstation-4-1tb-gts-hzd-spiderm-ps-3mes-40074231'

    @classmethod
    def check_status(cls):
        super().on_check_status()

        try:
            response = requests.get(cls.ps5_url, headers={
                'user-agent': 'Chrome/87.0.4280.66'
            })
            soup = BeautifulSoup(response.text, 'lxml')

            price_card = soup.select_one('.o-container__price-column .fl-pdp-pay .c-notifications')
            notification = price_card.select_one('.c-notifications__title')
            result = notification.text.strip()
            if result != cls.expected_string:
                raise UnexpectedData(f'UnexpectedData: найдена строка {result} вместо '
                                     f'ожидаемой {cls.expected_string} ({cls.retailer_name})')
            else:
                super().on_check_status_end()
        except AttributeError as e:
            raise InStock(f'InStock: {e} - видать не стало надписи {cls.expected_string} ({cls.retailer_name})')
