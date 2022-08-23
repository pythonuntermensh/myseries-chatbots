from aiogram.dispatcher.filters.state import State, StatesGroup

class BugReport(StatesGroup):
    waiting_for_bug_report = State()