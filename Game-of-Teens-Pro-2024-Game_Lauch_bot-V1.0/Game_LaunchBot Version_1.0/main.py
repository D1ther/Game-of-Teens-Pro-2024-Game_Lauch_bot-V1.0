from aiogram import Bot, Dispatcher, Router
from dotenv import load_dotenv
from os import getenv
from app.heandlers import rt
from aiogram.types import BotCommand
from art import tprint


import app.data_base.data_base as sdb
import asyncio
import sqlite3


load_dotenv()

TOKEN = getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()



# ФУНКЦІЯ ПІДКЛЮЧЕННЯ ДО БАЗИ ДАНИХ 
async def start_db():
     
    sdb.base_connect()
    print('Підключення до бази даних виконано ')


# ГОЛОВНА ФУНКЦІЯ
async def main():
    tprint(text='Game Launch Bot', font='bulbhead')
    await start_db()
    dp.include_router(rt)
    await dp.start_polling(bot)

if __name__ == '__main__':    

    try:
        asyncio.run(main())


    except KeyboardInterrupt:
        print('Вихід')

