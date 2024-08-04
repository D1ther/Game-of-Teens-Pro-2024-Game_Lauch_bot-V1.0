from aiogram import Router, Bot, F, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, BotCommand, CallbackQuery
from aiogram.fsm.context import FSMContext
from app.data_base.data_base import reg, create_game, show_game_name, show_game_photo, show_game_plot, select_game_plot_for_id, select_game_photo_for_id, update_game_name, update_game_photo, update_game_plot, game_removed, select_game_name
from app.fsm_states import AddGame, UpdateGame, GPT
from app.keyboards import main, game_menu, game_update_menu, cancle_markup, cancle_menu, stop_chatting_sinnbo, remove_game
from aiogram.filters.state import StateFilter
from app.gpt import question


import sqlite3 as sq



rt = Router()

# Меню команд бота
async def menu_cmd(bot:Bot):

    commands = [
        BotCommand(command='/start', description='Запустити/Перезапустити бота🔃'),
        BotCommand(command='/add_game', description='Додати гру до списку ігор➕'),
        BotCommand(command='/show_my_game', description='Показує усі ваші ігри📜'),
        BotCommand(command='/update_game', description='Оновити гру з вашого списку🔄'),
        BotCommand(command='/remove_game', description='Видалити гру зі свого списку🗑')
    ]

    await bot.set_my_commands(commands=commands)


# Команда старт
@rt.message(CommandStart())
async def start(message:Message):

    await menu_cmd(message.bot)

    await reg(tg_name=message.from_user.full_name, tg_id=message.from_user.id)

    await message.answer(text='Вітаю у TG launcher bot 🎮\n Тут ви зможете почати вести колекцію своїх ігор, або лишити підказки у іграх для себе 😁',
                         reply_markup=main)


# Хендлер додаваня гри

@rt.message(Command('add_game'))
async def get_game_name(message:Message, state:FSMContext):
    
    await state.set_state(AddGame.game_name)

    await message.answer(text='Напишіть назву гри яку бажаєте додати 🕹')


# Отримання назви гри
@rt.message(AddGame.game_name)
async def get_game_name_save(message:Message, state:FSMContext):
    game_name = message.text
    tg_id = message.from_user.id
    selected_game = await select_game_name(tg_id=tg_id, name=game_name)
    print(selected_game, game_name)

    
    game = selected_game is not None and game_name in selected_game

# Перевірка чи є у бд гра з точно такою ж назвою
    if game:

        await state.set_state(AddGame.game_name)
        await message.answer('Гра з такою назвою вже існує у вашій бібліотеці❌\n Змініть назву гри яку хочете додати')

    else:
        
        await state.update_data(name=message.text)
        await state.set_state(AddGame.photo_game)

        await message.answer(text='Надішліть зображення гри 🖼, або будь-яку потрібну вам інформацію про гру')


# отримання фото гри
@rt.message(AddGame.photo_game)
async def get_photo_save(message:Message, state:FSMContext):

    if message.content_type == types.ContentType.PHOTO:
        await state.update_data(game_photo=message.photo[-1].file_id)
    else:
        await state.update_data(game_photo=message.text)

    await state.set_state(AddGame.plot_game)

    await message.answer(text='Напишіть опис гри ✍, або будь-яку потрібну для вас інформацію про гру')


# отримання опису гри
@rt.message(AddGame.plot_game)
async def get_plot_save(message:Message, state:FSMContext):
    await state.update_data(game_plot=message.text)
    data = await state.get_data()
    game_name = data.get('name')
    game_photo = data.get('game_photo')
    game_plot = data.get('game_plot')
    tg_id = message.from_user.id
    
    await create_game(game_name=game_name, photo=game_photo, plot=game_plot, tg_id=tg_id)
        
    await message.answer(text=f'Гру було додано успішно 🎮')

    await state.clear()


# Команда показу усіх ігор
@rt.message(Command('show_my_game'))
@rt.message(F.text == 'Переглянути мої ігри🎮')
async def show_my_game(message:Message):

    tg_id = message.from_user.id


    await message.answer(text='Оберіть гру яку хочете переглянути', 
                         reply_markup= await game_menu(tg_id=tg_id))


# Перегляд свого профіля
@rt.message(F.text == 'Мій профіль🧑')
async def my_profile(message:Message):
    
    await message.answer(f"Ваше ім'я: {message.from_user.full_name}🧑\n Ваш ID {message.from_user.id}🆔 ")

# Перегля ігор людини
@rt.callback_query(F.data.startswith('gameid_'))
async def get_game_info(callback:CallbackQuery):
    tg_id = callback.message.chat.id
    print(f'ід юзера: {tg_id}')
    game_name = callback.data.split('_')[1]
    game_name_for = game_name
    print(f'Назва гри: {game_name}')


    # Отримання посилання фото гри з бд
    game_photos = await select_game_photo_for_id(title=game_name, tg_id=tg_id)
    print(game_photos)
    game_photo_list = []

    for games in game_photos:
        game_name = games
        game_photo_list.append(game_name)

    for game in game_photo_list:
        photo_game = game
    print(photo_game)

    # отримання опису гри з бд
    id_for_plot = callback.message.chat.id
    game_name_for_plot = callback.data.split('_')[1]

    game_plot = await select_game_plot_for_id(title=game_name_for_plot, tg_id=id_for_plot)
    print(game_plot)

    await callback.answer(' ')
    await callback.message.answer_photo(photo=photo_game, caption=f'Назва гри: {game_name_for} \n \n опис гри:\n {game_plot}  ')

# Оновлення гри
# Оновлення назви гри
@rt.callback_query(F.data.startswith('gameupd_'))
async def get_new_game_name(callback:CallbackQuery, state:FSMContext):
    await state.set_state(UpdateGame.new_game_name)
    game_name = callback.data.split('_')[1]

    await state.update_data(game_name=game_name)

    await callback.answer('')
    await callback.message.answer(text='Нпишіть нову назву для гри🎮',
                                  reply_markup=cancle_markup)

@rt.message(StateFilter(UpdateGame.new_game_name))
async def save_new_game_name(message:Message, state:FSMContext):
    await state.update_data(new_name=message.text)
    data = await state.get_data()
    new_name = data.get('new_name')
    game_name = data.get('game_name')
    tg_id = message.from_user.id
    print(tg_id)
    print(game_name)
    print(new_name)

    await update_game_name(new_game_title=new_name, title=game_name, tg_id=tg_id)

    await state.set_state(UpdateGame.new_game_plot)
    await message.answer(text='Напишіть новий опис гри ✍',
                            reply_markup=cancle_markup)

# Отримання нового опису гри
@rt.message(StateFilter(UpdateGame.new_game_plot))
async def save_new_game_plot(message:Message, state:FSMContext):
    await state.update_data(new_plot=message.text)
    data = await state.get_data()
    new_plot = data.get('new_plot')
    print(new_plot)
    game_name = data.get('game_name')
    tg_id = message.from_user.id
    print(f'updated plot: {new_plot}')

    await update_game_plot(new_plot=new_plot, title=game_name, tg_id=tg_id)

    await state.set_state(UpdateGame.new_game_photo)
    await message.answer('Надішліть нове фото гри 📸',
                         reply_markup=cancle_markup)

# Отримання нового фото гри
@rt.message(StateFilter(UpdateGame.new_game_photo))
async def save_new_game_photo(message:Message, state:FSMContext):

    if message.content_type == types.ContentType.PHOTO:
        await state.update_data(new_photo=message.photo[-1].file_id)
    else:
        await state.update_data(new_photo=message.text)

    data = await state.get_data()
    new_photo = data.get('new_photo')
    new_name = data.get('new_name')
    tg_id = message.from_user.id

    await update_game_photo(new_photo=new_photo, title=new_name, tg_id=tg_id)

    await message.answer(text='Гру оновлено')

    await state.clear()

# Меню вибору гри для оновлення
@rt.message(Command('update_game'))
@rt.message(F.text == 'Оновити гру🔄')
async def update_game_menu(message:Message):
    tg_id = message.from_user.id
    
    await message.answer(text='Оберіть гру яку хочете оновити',
                            reply_markup=await game_update_menu(tg_id=tg_id))
    

# Скасування дії
@rt.callback_query(F.data == 'cancle')
async def cancle(callback:CallbackQuery,state:FSMContext):
    await callback.answer('')
    await state.clear()

    await callback.message.answer(text='Ви повернулися у головне меню😄')

# Робота з нейромережею
@rt.message(F.text == 'SinnBo🤖')
async def state_chatting(message:Message, state:FSMContext):
    await state.set_state(GPT.chatting)

    await message.answer(text="Вітаю!\n Я штучний інтелект на ім'я SinnBo🤖 \n Раніше, я був геймером, який пройшов не 1 тисячу ігор. Тепер я влаштувався помічником для геймерів і готовий відповісти на ваші питання! Я чекаю ваших питань \n\n ❗Оскльки SinnBo використовує безкоштовну модель штучного інтелекту, іноді можливі баги. Також SinnBo не зберігає історію останніх запитів, та дає відповідь тільки на той, що ви надіслали тільки що. Ще запити можуть оброблятися повільно❗")

@rt.message(StateFilter(GPT.chatting))
async def chatting(message:Message, state:FSMContext):
    process = await message.answer(text='Ваш запит обробляється♻')
    await state.update_data(prompt=message.text)
    data = await state.get_data()
    prompt = data.get("prompt")
    print(prompt)
    print(message.from_user.full_name)

    answer = await question(promt=prompt)
    await message.reply(answer, 
                         reply_markup=stop_chatting_sinnbo)
    
    await process.delete()
    
# припинити чат
@rt.callback_query(F.data == 'stop_chatting')
async def stop_chatting_with_SinnBo(callback:CallbackQuery, state:FSMContext):
    await state.clear()

    await callback.answer('')
    await callback.message.edit_text(text='Ви зупинили переписку з SinnBo🤖')

# Команда видалення гри
@rt.message(Command('remove_game'))
async def game_remove(message:Message):
    tg_id = message.from_user.id

    await message.answer(text='Оберіть гру для видалення🗑', 
                         reply_markup=await remove_game(tg_id=tg_id))

# видалення гри
@rt.callback_query(F.data.startswith('gamedel_'))
async def get_remove_game(callback:CallbackQuery):
    await callback.answer('')
    game_name = callback.data.split('_')[1]
    tg_id = callback.message.chat.id

    await game_removed(name=game_name, tg_id=tg_id)
    await callback.message.answer(text=f'Гру {game_name}, було видалено успішно✔')
