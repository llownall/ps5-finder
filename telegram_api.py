import os

from telegram.ext import Updater

from settings import CHAT_ID

updater = Updater(token=os.environ['TOKEN'], use_context=True)


def send_exception_message(exception):
    message = str(exception)
    updater.bot.send_message(
        chat_id=CHAT_ID,
        text=message
    )
