from aiogram.dispatcher.filters.state import State, StatesGroup

class BugReportAnswer(StatesGroup):
    waiting_for_user_url = State()
    waiting_for_answer_text = State()