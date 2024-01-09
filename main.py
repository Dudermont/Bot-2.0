import asyncio
from aiogram import Bot, Dispatcher
from config.config import config
from handlers import hendlers, echo_hendler, commands

from handlers.fsm import storage
from keyboards.main_menu import set_mein_menu


async def main():
    bot: Bot = Bot(token=config.tg_bot.token)
    dp: Dispatcher = Dispatcher(storage=storage)

    print('Bot on')

    await set_mein_menu(bot)
    dp.include_router(commands.router)
    dp.include_router(hendlers.router)
    dp.include_router(echo_hendler.router)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except(KeyboardInterrupt, SystemExit):
        print('Bot stopped')
