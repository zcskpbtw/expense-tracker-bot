from aiogram.filters import Command
from aiogram import Router
from aiogram.types import Message
from database import get_list_expenses


router = Router(name='list')

@router.message(Command('list'))
async def get_expenses(message: Message):
    expenses = get_list_expenses(user_id=message.from_user.id)

    if not expenses:
        await message.answer('У вас пока что не трат')
        return

    text = 'Ваши траты за период: \n'

    for exp_id, date, category, amount in expenses:
        text += f"{exp_id}. Дата: {date} | Категория: {category} - {amount} \n"

    await message.answer(text)
