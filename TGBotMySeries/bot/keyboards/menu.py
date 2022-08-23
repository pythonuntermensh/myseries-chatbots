from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Подписаться на сериал"),
        ],
        [
            KeyboardButton(text="Отписаться от сериала"),
        ],
        [
            KeyboardButton(text="Все подписки"),
        ],
        [
            KeyboardButton(text="Подписаться на новинки"),
        ],
        [
            KeyboardButton(text="Отписаться от новинок"),
        ],
        [
            KeyboardButton(text="Баг репорт"),
        ],
        [
            KeyboardButton(text="Актуальная ссылка")
        ],
    ],
    resize_keyboard=True 
)