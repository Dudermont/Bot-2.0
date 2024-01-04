from aiogram import types, Dispatcher
lexicon: dict[str, str] = {
    'registration': '\nВаша учетная запись зарегистрирована. '
                    '\nНапишите /help или нажмите на команду, чтобы узнать, что может бот',
    'help_menu': "Чего изволите?",
    'spending': 'Введите сумму',
    'echo_answer': 'К сожалению не могу с вам подискутировать😭. Я могу только следить за вашими тратами 💵.',
    'cash_error': 'Произошла ошибка.⚠️ \nВвести надо положительное число.➕ \nА также до 8 знаков до точки и до 2 знаков после точки.',
    'month_error': 'Произошла ошибка.⚠️ \nВвести надо положительное число от 1 до 12.➕ \nИли название месяца.',
    'year_error': 'Произошла ошибка.⚠️ \nВвести надо положительное число от 1 до 9999.➕',
    'cancel': 'Вы отменили ввод'

}
