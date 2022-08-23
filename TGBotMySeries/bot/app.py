import asyncio
from aiogram import bot, executor
import handlers
from loader import dp, bot
from tasks.check_new_series import check_new_series
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(check_new_series(10, bot))
    executor.start_polling(dp, on_startup=on_startup)

