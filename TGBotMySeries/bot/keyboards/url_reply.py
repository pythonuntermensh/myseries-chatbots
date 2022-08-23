from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

url_reply = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Меню"),
        ],
        [
            KeyboardButton(text="Заблокировано"),
        ],
    ],
    resize_keyboard=True 
)