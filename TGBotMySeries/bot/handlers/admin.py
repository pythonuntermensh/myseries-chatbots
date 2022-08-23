from aiogram import types
from aiogram.dispatcher.filters import Command
from data.config import ADMINS
from keyboards import admin
from loader import dp


@dp.message_handler(Command("admin"))
async def bot_admin(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        await message.answer("Выберите опцию", reply_markup=admin)
