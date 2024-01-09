from datetime import date
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from database import db_connect
from handlers.fsm import FSMFillspending, FSMCategoryspend, FSMDuringDay, FSMDuringMonth, FSMDuringYear, FSMDuringDuring
from keyboards.keyboard import keyboard_2, spend_during_keyboard, cancel_keyboard
from serveses.servises import (send_spend_dp, spend_category, day_db_select,
                               month_db_select, year_db_select, period_db_select)
from serveses.filters import Is_money, Is_month

from lexicon.lexicon import lexicon


router = Router()


# # ответ на кнопку help
# @router.callback_query(F.data == 'help')
# async def inline_kb_answer_help(query: CallbackQuery):
#     await help_command(query.message)


# Ответ на кнопку expense
@router.callback_query(F.data == 'expense')
async def inline_kb_answer_expense(query: CallbackQuery):
    await query.message.delete()
    await query.message.answer("Вы потратили:")
    await query.message.answer(str(*db_connect.all_spend(query.message.chat.username)))
    await query.message.answer(text=f'Чего изволите, {query.message.chat.first_name}?', reply_markup=keyboard_2)


# Ответ на кнопку spending
@router.callback_query(F.data == 'spending',  StateFilter(default_state))
async def inline_kb_answer_spending(query: CallbackQuery, state: FSMContext):
    await query.message.delete()
    await query.message.answer(text='Введите сумму', reply_markup=cancel_keyboard)
    await state.set_state(FSMFillspending.fill_spend)


# Если проходит проверку ввод денег
@router.message(StateFilter(FSMFillspending.fill_spend), Is_money())
async def take_cash(message: Message, state: FSMContext):
    await state.update_data(cash=message.text)
    await message.answer(text='Спасибо, а теперь введите категорию', reply_markup=cancel_keyboard)
    await state.set_state(FSMFillspending.fill_category)


# Если не проходит проверку ввод денег
@router.message(StateFilter(FSMFillspending.fill_spend))
async def wrong_take_cash(massage: Message):
    await massage.answer(lexicon['cash_error'], reply_markup=cancel_keyboard)


# Введение категории при заносе траты
@router.message(StateFilter(FSMFillspending.fill_category))
async def take_category(message: Message, state: FSMContext):
    await state.update_data(username=message.from_user.username, category=message.text)
    user_spend = await state.get_data()
    await message.answer(send_spend_dp(user_spend))
    await message.answer(text=f'Чего изволите, {message.from_user.first_name}?', reply_markup=keyboard_2)
    await state.clear()
    print(user_spend)


# Ответ на кнопку category
@router.callback_query(F.data == 'category', StateFilter(default_state))
async def inline_kb_answer_category(query: CallbackQuery, state: FSMContext):
    await query.message.delete()
    await query.message.answer(text='Введите категорию', reply_markup=cancel_keyboard)
    await state.set_state(FSMCategoryspend.fill_category)


# # Введение категории при выгрузке категорий
@router.message(StateFilter(FSMCategoryspend.fill_category))
async def give_expense(message: Message, state: FSMContext):
    await state.update_data(username=message.from_user.username, category=message.text)
    user_spend = await state.get_data()
    await message.answer(f"Вы потратили на {user_spend['category']}:")
    await message.answer(spend_category(user_spend))
    await message.answer(text=f'Чего изволите, {message.from_user.first_name}?', reply_markup=keyboard_2)
    await state.clear()


# Ответ на кнопку during
@router.callback_query(F.data == 'during', StateFilter(default_state))
async def inline_kb_answer_during(query: CallbackQuery):
    await query.message.answer("Бурлык", reply_markup=spend_during_keyboard)
    await query.message.delete()


# Ответ на кнопку day
@router.callback_query(F.data == 'day', StateFilter(default_state))
async def inline_kb_answer_day(query: CallbackQuery, state: FSMContext):
    await query.message.delete()
    await query.message.answer("Введите дату гггг-мм-дд", reply_markup=cancel_keyboard)
    await state.set_state(FSMDuringDay.fill_date)


# Ввод дня для получения трат
@router.message(StateFilter(FSMDuringDay.fill_date))
async def give_expense_per_day(message: Message, state: FSMContext):
    await state.update_data(username=message.from_user.username, date=message.text)
    user_date = await state.get_data()
    print(user_date)
    await message.answer(f"Вы потратили за {user_date['date']}:")
    await message.answer(str(*day_db_select(user_date)))
    await message.answer(text=lexicon['help_menu'], reply_markup=keyboard_2)
    await state.clear()


# Ответ на кнопку month
@router.callback_query(F.data == 'month', StateFilter(default_state))
async def inline_kb_answer_month(query: CallbackQuery, state: FSMContext):
    await query.message.delete()
    await query.message.answer('Введите месяц', reply_markup=cancel_keyboard)
    await state.set_state(FSMDuringMonth.fill_month)


# Ввод month для получения трат
@router.message(StateFilter(FSMDuringMonth.fill_month), Is_month())
async def give_expense_per_month(message: Message, state: FSMContext):
    await message.delete()
    await state.update_data(month=message.text.title(), year=date.today().year, username=message.chat.username)
    user_date = await state.get_data()
    print(user_date)
    await message.answer(f'Вы потратили за {user_date["month"]}')
    await message.answer(str(month_db_select(user_date)))
    await state.clear()


# Не верный ввод month для получения трат
@router.message(StateFilter(FSMDuringMonth.fill_month))
async def wrong_expense_per_month(message: Message):
    await message.answer(lexicon['month_error'], reply_markup=cancel_keyboard)


# Ответ на кнопку year
@router.callback_query(F.data == 'year', StateFilter(default_state))
async def inline_kb_answer_year(query: CallbackQuery, state: FSMContext):
    await query.message.delete()
    await query.message.answer('Введите год', reply_markup=cancel_keyboard)
    await state.set_state(FSMDuringYear.fill_year)


# Ввод year для получения трат
@router.message(StateFilter(FSMDuringYear.fill_year),
                lambda x: x.text.isdigit() and 1 <= int(x.text) <= 9999)
async def give_expense_per_year(message: Message, state: FSMContext):
    await message.delete()
    await state.update_data(year=message.text, username=message.chat.username)
    user_date = await state.get_data()
    print(user_date)
    await message.answer(f'Вы потратили за {user_date["year"]} год')
    await message.answer(str(year_db_select(user_date)))
    await state.clear()


# Не верный ввод year для получения трат
@router.message(StateFilter(FSMDuringYear.fill_year))
async def wrong_expense_per_year(message: Message):
    await message.answer(lexicon['year_error'], reply_markup=cancel_keyboard)


# Ответ на кнопку period
@router.callback_query(F.data == 'period', StateFilter(default_state))
async def inline_kb_answer_period(query: CallbackQuery, state: FSMContext):
    await query.message.delete()
    await query.message.answer('Введите первую дату гггг-мм-дд', reply_markup=cancel_keyboard)
    await state.set_state(FSMDuringDuring.fill_first_date)


# Ввод первой даты для получения трат
@router.message(StateFilter(FSMDuringDuring.fill_first_date))
async def take_first_date(message: Message, state: FSMContext):
    await state.update_data(first_year=message.text)
    await message.answer(text='Спасибо, а теперь вторую гггг-мм-дд', reply_markup=cancel_keyboard)
    await state.set_state(FSMDuringDuring.fill_second_date)


# Ввод второй даты для получения трат
@router.message(StateFilter(FSMDuringDuring.fill_second_date))
async def give_expense_period(message: Message, state: FSMContext):
    await message.delete()
    await state.update_data(second_year=message.text, username=message.chat.username)
    user_date = await state.get_data()
    print(user_date)
    await message.answer(f'Вы потратили c {user_date["first_year"]} по {user_date["second_year"]}:')
    await message.answer(str(period_db_select(user_date)))
    await state.clear()


# Ответ на кнопку canсel
@router.callback_query(~StateFilter(default_state))
async def inline_kb_cancel(query: CallbackQuery, state: FSMContext):
    await query.message.delete()
    await query.message.answer(lexicon['cancel'])
    await state.clear()
