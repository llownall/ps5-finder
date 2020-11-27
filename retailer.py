import datetime
import logging

from selenium.common.exceptions import NoSuchElementException

from website import load_page_and_return_driver


class HTMLChanged(Exception):
    pass


class ParseError(Exception):
    pass


class Retailer:
    is_current = False
    is_active = True
    status_check_call_counter = 0
    status_check_call_success_counter = 0
    last_html = None

    def __init__(self, retailer_name, ps5_url, html_class):
        self.retailer_name = retailer_name
        self.ps5_url = ps5_url
        self.html_class = html_class

    def on_check_status(self):
        logging.info(f'Проверка статуса товара ритейлера {self.retailer_name}')
        self.status_check_call_counter += 1

    def on_check_status_end(self):
        logging.info(f'Проверка статуса товара ритейлера {self.retailer_name} завершена. Ничего нового')
        self.status_check_call_success_counter += 1

    def check_status(self):
        self.on_check_status()

        driver = load_page_and_return_driver(self.ps5_url)
        try:
            elem = driver.find_element_by_class_name(self.html_class)
            inner_html = elem.text
            # inner_html = elem.get_attribute('innerHTML').strip()
            if self.last_html is None:
                self.last_html = inner_html
            elif self.last_html != inner_html:
                self.last_html = inner_html
                self.save_screenshot(driver)
                raise HTMLChanged(f'HTMLChanged')
            self.on_check_status_end()
        except NoSuchElementException:
            logging.info(f'Selenium ничего не нашел')
        finally:
            driver.close()

    def save_screenshot(self, driver):
        driver.save_screenshot('last_screenshot.png')
        driver.save_screenshot(f'screenshots/{datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")}'
                               f'_{self.retailer_name}.png')
