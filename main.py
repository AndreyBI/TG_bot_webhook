# tg0bot0aiogram0webhook

import logging
import os
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.webhook import SendMessage
from aiogram.utils.executor import start_webhook
from aiogram import Bot, types
from telegram.ext import Updater

TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

# webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = 80


async def on_startup(dispatcher):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dispatcher):
    await bot.delete_webhook()


@dp.message_handler()
async def echo(message: types.Message):
    return SendMessage(message.chat.id, message.text)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # start_webhook(
    #     dispatcher=dp,
    #     webhook_path=WEBHOOK_PATH,
    #     skip_updates=True,
    #     on_startup=on_startup,
    #     on_shutdown=on_shutdown,
    #     host=WEBAPP_HOST,
    #     port=WEBAPP_PORT,
    # )

    PORT = int(os.environ.get('PORT', '80'))
    updater = Updater(TOKEN)
    # add handlers
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN,
                          webhook_url=f"https://{HEROKU_APP_NAME}.herokuapp.com/" + TOKEN)
    updater.idle()