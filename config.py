import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer


load_dotenv()

proxy_url = os.getenv("PROXY_URL")
token = os.getenv("BOT_TOKEN")

if not token:
    error = 'токен не найден! проверь файл .env'
    raise ValueError(error)

session = AiohttpSession(api=TelegramAPIServer.from_base(proxy_url))
bot = Bot(token=token,session=session)
dp = Dispatcher()
