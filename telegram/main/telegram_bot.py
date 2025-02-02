import asyncio
from aiogram import Bot
from django.conf import settings

TOKEN = "7428797811:AAF0zPdkhpBADfbBmlNq-JOxb2blQE5KPcg"
CHAT_ID = "8131945136"

async def send_telegram_message(text):
    """Асинхронная отправка сообщения через aiogram"""
    bot = Bot(token=TOKEN)
    try:
        await bot.send_message(chat_id=CHAT_ID, text=text)
    finally:
        await bot.session.close()

def send_message_sync(text):
    """Обёртка для вызова асинхронной функции из синхронного Django-кода"""
    asyncio.run(send_telegram_message(text))
