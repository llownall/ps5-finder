import os

from telegram.ext import Updater

from settings import CHAT_ID

updater = Updater(token=os.environ['TOKEN'], use_context=True)


def start_polling():
    updater.start_polling()


def send_exception_message(exception):
    message = str(exception)
    updater.bot.send_message(chat_id=CHAT_ID, text=message)
    updater.bot.send_photo(chat_id=CHAT_ID, photo=open('last_screenshot.png', 'rb'))
