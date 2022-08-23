from aiogram.dispatcher.filters.state import State, StatesGroup

class MainUrl(StatesGroup):
    waiting_for_new_url = State()