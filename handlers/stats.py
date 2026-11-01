from aiogram.filters import Command
from database import get_all_expenses, get_max_expense, avg_expenses
from aiogram import Router
from aiogram.types import Message



router = Router(name='stats')


@router.message(Command('stats'))
async def stats(message: Message):
    text = ''
    for amount, days in get_all_expenses(message.from_user.id):
        text += f'Всего за период ({days}), было потрачено: {amount} руб.\n\n'
    for date, category, amount in get_max_expense(message.from_user.id):
        text += f'Максимальная трата \nДата: {date} | {category} - {amount} руб. \n\n'
    for amounts, days in avg_expenses(message.from_user.id):
        try:
            text += f'За эти дни в среднем было потрачено: {amounts/days} руб.'
        except ZeroDivisionError:
            await message.answer('Нет трат!')
            return
    await message.answer(text)



