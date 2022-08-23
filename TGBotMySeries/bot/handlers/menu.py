from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message
from keyboards import menu

from loader import dp

@dp.message_handler(Command("menu"))
@dp.message_handler(text=["Меню", "меню"])
async def show_menu(message: Message):
    await message.answer("Меню", reply_markup=menu)

