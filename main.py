import time
import logging

from selenium.common.exceptions import TimeoutException

from retailers.base_retailer import *
from retailers.mvideo import MVideo
from retailers.dns import DNS
from retailers.eldorado import Eldorado
from retailers.one_c import OneC
from retailers.ozon import Ozon
from settings import CHECK_INTERVAL
from telegram_api import send_exception_message

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)

retailers = [
    MVideo,
    DNS,
    Eldorado,
    OneC,
    Ozon,
]

while True:
    for retailer in retailers:
        try:
            retailer.check_status()
        except InStock as e:
            logging.critical(e)
            send_exception_message(e)
        except UnexpectedData as e:
            logging.warning(e)
            send_exception_message(e)
        except TimeoutException as e:
            logging.error(f'Таймаут {retailer.retailer_name}')
        except Exception as e:
            logging.error(type(e))
            logging.error(e)
            send_exception_message(e)

    time.sleep(CHECK_INTERVAL)
