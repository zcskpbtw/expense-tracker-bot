from aiogram.filters import Command
from database import get_max_expense, avg_expenses
from aiogram import Router
from aiogram.types import Message



router = Router(name='stats')


@router.message(Command('stats'))
async def stats(message: Message):
    text = ''
    for date, category, amount in get_max_expense(message.from_user.id):
        text += f'Дата: {date} | {category} - {amount} \n\n'
    for amounts, days in avg_expenses(message.from_user.id):
        try:
            text += f'за дни трат ({days}), в среднем было потрачено: {amounts/days} руб.'
        except ZeroDivisionError:
            await message.answer('Нет трат!')
            return
    await message.answer(text)



