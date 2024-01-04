import asyncio
from aiogram import Bot, Dispatcher
from config.config import config
from handlers import hendlers, echo_hendler, commands

from handlers.fsm import storage
from keyboards.main_menu import set_mein_menu


# def registration_all_handlers(dp: Dispatcher):
#     registration_command_handler(dp)
#     registration_handler(dp)
#     registration_echo_handler(dp)


async def main():
    bot: Bot = Bot(token=config.tg_bot.token)
    dp: Dispatcher = Dispatcher(storage=storage)

    print('Bot on')


    # registration_all_handlers(dp)

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
