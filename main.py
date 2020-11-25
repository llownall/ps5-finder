import time
import logging

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
        except Exception as e:
            logging.error(e)
            send_exception_message(e)

    time.sleep(CHECK_INTERVAL)
