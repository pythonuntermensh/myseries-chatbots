from aiogram.dispatcher.filters.state import State, StatesGroup

class SecondUrl(StatesGroup):
    waiting_for_new_url = State()