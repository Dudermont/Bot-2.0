from aiogram import Bot, types


async def set_mein_menu(bot: Bot):
    main_menu_commands = [
        # types.BotCommand(command='/start', description='Приветствие'),
        types.BotCommand(command='/menu', description='Вызвать меню')
        # types.BotCommand(command='/spending', description='Внести трату')
        # types.BotCommand(command='/cancel', description='Отменить ввод данных')
    ]
    await bot.set_my_commands(main_menu_commands)
