import threading
import time
import logging
import os

from telegram.ext import Updater, CommandHandler
from selenium.common.exceptions import TimeoutException

from retailers.base_retailer import *
from retailers.sony import Sony
from retailers.mvideo import MVideo
from retailers.dns import DNS
from retailers.eldorado import Eldorado
from retailers.one_c import OneC
from retailers.ozon import Ozon
from settings import CHECK_INTERVAL, CHAT_ID
from utils import get_human_time

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


def status(update, context):
    retailers_data = []
    for retailer in retailers:
        retailers_data.append(
            f'`{retailer.retailer_name:<12}: {retailer.status_check_call_success_counter} '
            f'/ {retailer.status_check_call_counter}{" ###" if retailer.is_current else ""}`'
        )
    retailers_data_string = '\n'.join(retailers_data)

    message = f'Бот работает *{get_human_time(datetime.datetime.now() - launch_time)}*\n' \
              f'_Справка по ритейлерам:_\n' \
              f'{retailers_data_string}'

    if pause_time is not None:
        message += f'\nПродолжение через {CHECK_INTERVAL - (datetime.datetime.now() - pause_time).seconds} ' \
                   f'секунд'

    context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode='MarkdownV2')


def send_exception_message(exception):
    message = str(exception)
    updater.bot.send_message(chat_id=CHAT_ID, text=message)
    updater.bot.send_photo(chat_id=CHAT_ID, photo=open('last_screenshot.png', 'rb'))


updater = Updater(
    token=os.environ['TOKEN'],
    use_context=True,
)

start_handler = CommandHandler('status', status)
updater.dispatcher.add_handler(start_handler)
threading.Thread(target=updater.start_polling).start()

launch_time = datetime.datetime.now()
pause_time = None

while True:
    for retailer in retailers:
        retailer.is_current = True
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
        finally:
            retailer.is_current = False

    logging.info(f'Ждем {CHECK_INTERVAL} секунд и повторяем...')
    pause_time = datetime.datetime.now()
    time.sleep(CHECK_INTERVAL)
    pause_time = None

