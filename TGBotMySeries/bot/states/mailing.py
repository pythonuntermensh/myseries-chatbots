from aiogram.dispatcher.filters.state import State, StatesGroup

class Mailing(StatesGroup):
    waiting_for_mailing_message = State()