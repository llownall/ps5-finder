import threading
import time
import logging

from selenium.common.exceptions import TimeoutException

from retailers.base_retailer import *
from retailers.sony import Sony
from retailers.mvideo import MVideo
from retailers.dns import DNS
from retailers.eldorado import Eldorado
from retailers.one_c import OneC
from retailers.ozon import Ozon

from settings import CHECK_INTERVAL
from telegram_chat import send_exception_message, start_polling

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)

retailers = [
    Sony,
    MVideo,
    DNS,
    Eldorado,
    OneC,
    Ozon,
]

threading.Thread(target=start_polling)

while True:
    for retailer in retailers:
        try:
            retailer.check_status()
        except InStock as e:
            logging.critical(f'{e} ({retailer.retailer_name})')
            send_exception_message(f'{e} ({retailer.retailer_name})')
        except UnexpectedData as e:
            logging.warning(f'{e} ({retailer.retailer_name})')
            send_exception_message(f'{e} ({retailer.retailer_name})')
        except TimeoutException as e:
            logging.error(f'Таймаут {retailer.retailer_name}')
        except Exception as e:
            logging.error(f'{type(e)} ({retailer.retailer_name})')
            logging.error(f'{e} ({retailer.retailer_name})')
            send_exception_message(f'{e} ({retailer.retailer_name})')

    logging.info(f'Ждем {CHECK_INTERVAL} секунд и повторяем...')
    time.sleep(CHECK_INTERVAL)
