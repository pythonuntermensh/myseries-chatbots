from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}! Я бот портала MySeries. О всех командах ты можешь прочитать нажав на кнопку /help", reply_markup=types.ReplyKeyboardRemove())
