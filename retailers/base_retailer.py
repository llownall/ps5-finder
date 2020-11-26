import datetime
import logging


class InStock(Exception):
    pass


class UnexpectedData(Exception):
    pass


class ParseError(Exception):
    pass


class Retailer:
    status_check_call_counter = 0
    status_check_call_success_counter = 0
    retailer_name = ''

    @classmethod
    def on_check_status(cls):
        logging.info(f'Проверка статуса товара ритейлера {cls.retailer_name}')
        cls.status_check_call_counter += 1

    @classmethod
    def on_check_status_end(cls):
        logging.info(f'Проверка статуса товара ритейлера {cls.retailer_name} завершена. Ничего нового')
        cls.status_check_call_success_counter += 1

    @classmethod
    def check_status(cls):
        pass

    @classmethod
    def save_screenshot(cls, driver):
        driver.save_screenshot('last_screenshot.png')
        driver.save_screenshot(f'screenshots/{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
                               f'_{cls.retailer_name}.png')
