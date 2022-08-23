import asyncio
from loader import bot
from tasks.check_new_series import check_new_series
import events


def main():
    bot.run_forever()

if __name__=='__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(check_new_series(30, bot))
    main()
