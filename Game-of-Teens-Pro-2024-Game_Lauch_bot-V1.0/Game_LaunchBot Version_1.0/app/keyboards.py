from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.data_base.data_base import show_game_name
from aiogram.types import Message

import asyncio

# Клавіатура при старті
main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Мій профіль🧑')],[KeyboardButton(text='Переглянути мої ігри🎮'), KeyboardButton(text='Оновити гру🔄')],
        [KeyboardButton(text='SinnBo🤖')]
    ],
    resize_keyboard=True
)

# Меню після повернення в головне меню
cancle_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Мій профіль🧑')],[KeyboardButton(text='Переглянути мої ігри🎮'), KeyboardButton(text='Оновити гру🔄')],
        [KeyboardButton(text='SinnBo🤖')]
    ],
    resize_keyboard=True
)

stop_chatting_sinnbo = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Зупинити розмову з SinnBo', callback_data='stop_chatting')]
    ]
)




# Побудова клавіатури ігор

async def game_menu(tg_id:int=None):
    in_b = InlineKeyboardBuilder()
    games_list = []
    
    games_name = await show_game_name(tg_id=tg_id)


    for game in games_name:
        game_name = game[0]
        games_list.append(game_name)

    for game_title in games_list:
        in_b.add(InlineKeyboardButton(text=game_title, callback_data=f'gameid_{game_title}'))


    return in_b.adjust(3).as_markup()

# Побудова клавіатури для оновлення гри
async def game_update_menu(tg_id:int):
    in_b=InlineKeyboardBuilder()
    game_list = []

    game_name = await show_game_name(tg_id=tg_id)

    for game_title in game_name:
        game = game_title[0]
        game_list.append(game)

    for games in game_list:
        in_b.add(InlineKeyboardButton(text=games, callback_data=f'gameupd_{games}'))

    return in_b.adjust(3).as_markup()

# побудова клавіатури для видалення
async def remove_game(tg_id:int):
    in_b=InlineKeyboardBuilder()
    game_list = []

    game_name = await show_game_name(tg_id=tg_id)

    for game_title in game_name:
        game = game_title[0]
        game_list.append(game)

    for games in game_list:
        in_b.add(InlineKeyboardButton(text=games, callback_data=f'gamedel_{games}'))

    return in_b.adjust(3).as_markup()

# Повернення назад
cancle_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Це все, що я хотів додати', callback_data='cancle')]
    ]
)

