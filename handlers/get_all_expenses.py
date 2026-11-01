from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from database import get_list_expenses
from keyboards import keyboard_start

router = Router(name='list')

@router.message(F.text.in_({'/list', 'Список трат'}))
async def get_expenses(message: Message, state: FSMContext):
    await state.clear()
    expenses = get_list_expenses(user_id=message.from_user.id)

    if not expenses:
        await message.answer('У вас пока что не трат', reply_markup=keyboard_start())
        return

    text = 'Ваши траты за период: \n'

    for exp_id, date, category, amount in expenses:
        text += f"{exp_id}. Дата: {date} | Категория: {category} - {amount} \n"

    await message.answer(text)
