# # tg0bot0aiogram0webhook
#
# import logging
# import os
# from flask import Flask, request
#
# from aiogram.dispatcher import Dispatcher
# from aiogram.dispatcher.webhook import SendMessage
# from aiogram.utils.executor import start_webhook
# from aiogram import Bot, types
#
# TOKEN = os.getenv('BOT_TOKEN')
# bot = Bot(token=TOKEN)
# dp = Dispatcher(bot)
# server = Flask(__name__)
#
# HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')
#
# # webhook settings
# WEBHOOK_HOST = f'https://tg0bot0aiogram0webhook.herokuapp.com/'
# WEBHOOK_PATH = f'/{TOKEN}'
# WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'
#
# # webserver settings
# WEBAPP_HOST = '0.0.0.0'
# WEBAPP_PORT = 80
#
#
# @dp.message_handler(commands=['start'])
# def start(call: types.CallbackQuery):
#     call.answer('Hello, ' + call.message.from_user.first_name)
#
#
# @dp.callback_query_handler(content_types=['text'])
# def echo(call: types.CallbackQuery):
#     call.answer(call.message.text)
#
#
# @server.route('/' + TOKEN, methods=['POST'])
# def get_message():
#     json_string = request.get_data().decode('utf-8')
#     update = telebot.types.Update.de_json(json_string)
#     bot.process_new_updates([update])
#     return '!', 200
#
#
# @server.route('/')
# def webhook():
#     bot.delete_webhook()
#     bot.set_webhook(url=WEBHOOK_URL)
#     return '!', 200
#
#
# async def on_startup(dispatcher):
#     await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)
#
#
# async def on_shutdown(dispatcher):
#     await bot.delete_webhook()
#
#
# @dp.message_handler()
# async def echo(message: types.Message):
#     return SendMessage(message.chat.id, message.text)
#
#
# if __name__ == '__main__':
#     logging.basicConfig(level=logging.INFO)
#     server.run(host="0.0.0.0", port=int(os.environ.get('PORT', '5000'))
#
#     start_webhook(
#         dispatcher=dp,
#         webhook_path=WEBHOOK_PATH,
#         skip_updates=True,
#         on_startup=on_startup,
#         on_shutdown=on_shutdown,
#         host=WEBAPP_HOST,
#         port=WEBAPP_PORT,
#     )
#
#
#


import logging
import os

from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.webhook import SendMessage
from aiogram.utils.executor import start_webhook


BOT_TOKEN = os.getenv('BOT_TOKEN')
HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

# webhook settings
WEBHOOK_HOST = 'https://tg0bot0aiogram0webhook.herokuapp.com/'
WEBHOOK_PATH = f'/{BOT_TOKEN}'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = 'localhost'  # or ip
WEBAPP_PORT = 3001

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler()
async def echo(message: types.Message):
    # Regular request
    # await bot.send_message(message.chat.id, message.text)

    # or reply INTO webhook
    return SendMessage(message.chat.id, message.text)


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    # insert code here to run it after start


async def on_shutdown(dp):
    logging.warning('Shutting down..')

    # insert code here to run it before shutdown

    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()

    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning('Bye!')


if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )