from aiogram.fsm.state import State, StatesGroup

class AddGame(StatesGroup):
    game_name = State()
    photo_game = State()
    plot_game = State()

class UpdateGame(StatesGroup):
    new_game_name = State()
    new_game_photo = State()
    new_game_plot = State()

class GPT(StatesGroup):
    give_question = State()
    chatting = State()