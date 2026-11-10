from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from database import get_list_expenses
from keyboards import keyboard_start


router = Router(name='list')

@router.message(F.text.in_({'/list', 'Список трат'}))
async def get_expenses(message: Message, state: FSMContext):

    await state.clear()

    expenses = get_list_expenses(telegram_id=message.from_user.id)
    if not expenses:
        await message.answer('У вас пока что не трат',
                             reply_markup=keyboard_start())
        return

    text = 'Ваши последние 10 трат: \n'

    for e_id, category, amount, date in expenses:
        text += f"{e_id}. {category} -- {amount} | {date} \n"

    await message.answer(text)
