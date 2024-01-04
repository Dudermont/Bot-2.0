from aiogram import Router
from aiogram.types import Message
from lexicon.lexicon import lexicon
from keyboards.keyboard import keyboard_1


router = Router()


# Ответ на любое сообщение
@router.message()
async def message_answer(message: Message):
    await message.answer(lexicon['echo_answer'], reply_markup=keyboard_1)


# def registration_echo_handler(dp: Dispatcher):
#     dp.register_message_handler(message_answer)
