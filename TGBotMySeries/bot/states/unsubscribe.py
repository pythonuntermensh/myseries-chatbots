from aiogram.dispatcher.filters.state import State, StatesGroup

class Unsubscribe(StatesGroup):
    waiting_for_series_name = State()
    waiting_for_series_num = State()