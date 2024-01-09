from aiogram.filters import BaseFilter
from aiogram.types import Message
from keyboards.keyboard import month3



class Is_money(BaseFilter):
    async def __call__(self, message: Message):
        if message.text.isdigit() and len(message.text) < 8:
            return True
        if message.text.find(',') != -1:
            r = message.text.replace(',', '.').split('.')
        else:
            r = message.text.split('.')
        if len(r) > 2:
            return False
        if not r[0].isdigit() or len(r[0]) > 8:
            return False
        if not r[1].isdigit() or len(r[1]) > 2:
            return False
        return True


class Is_month(BaseFilter):
    async def __call__(self, message: Message):
        if message.text.isdigit() and 1 <= int(message.text) <= 12 or len(
                message.text.split()) == 1 and message.text.title() in month3.values():
            return True
