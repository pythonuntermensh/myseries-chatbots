from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Массовая рассылка"),
        ],
        [
            KeyboardButton(text="Изменить основную ссылку"),
        ],
        [
            KeyboardButton(text="Изменить зеркало"),
        ],
        [
            KeyboardButton(text="Отправить ответ на баг репорт"),
        ],
    ],
    resize_keyboard=True 
)