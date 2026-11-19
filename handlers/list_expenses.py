from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database import get_list_expenses
from keyboards import keyboard_start


router = Router(name='list')

## waiting command list
@router.message(F.text.in_({'/list', 'Список трат'}))
async def get_expenses(message: Message, state: FSMContext):

    await state.clear()

    expenses = get_list_expenses(telegram_id=message.from_user.id)
    if not expenses:
        await message.answer('У вас пока что не трат',
                             reply_markup=keyboard_start())
        return

    text = ''

    for cnt, (e_id, category, amount, date) in enumerate(expenses, start=1):
        text += f"{cnt}. {category} -- {amount} | {date}\n"

    text = f'Ваши последние добавленные траты ({len(expenses)}):\n' + text

    await message.answer(text)
