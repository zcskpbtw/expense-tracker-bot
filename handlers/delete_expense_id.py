from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from database import delete_by_id,get_list_expenses
from functions import is_valid_text
from keyboards import keyboard_start,keyboard_return


router = Router(name='delete')

class Delete(StatesGroup):
    waiting_id = State()

@router.message(F.text.in_({'/delete', 'Удалить трату'}))
async def get_expenses(message: Message, state: FSMContext) -> None:

    await state.clear()
    
    if not get_list_expenses(user_id=message.from_user.id):
        await message.answer('У вас пока что не трат')
        return

    await message.answer('Введите айди траты которую хотите удалить',
                         reply_markup=keyboard_return())
    await state.set_state(Delete.waiting_id)

@router.message(Delete.waiting_id)
async def process_date(message: Message, state: FSMContext) -> None:

    if not is_valid_text(message.text):
        await state.clear()
        await message.answer('Неверный формат записи! Отправьте текст.',
                             reply_markup=keyboard_start())
        return

    if message.text.lower() == 'отмена':
        await state.clear()
        await message.answer('Отмена текущего действия',
                             reply_markup=keyboard_start())
        return

    try:
        exp_id = int(message.text)
    except ValueError:
        await message.answer('Ошибка! Введите айди!',
                             reply_markup=keyboard_start())
        return

    if delete_by_id(exp_id=exp_id,
                    user_id=message.from_user.id) > 0:
        await message.answer('Трата успешно удалена!',
                             reply_markup=keyboard_start())
    else:
        await message.answer('Нет траты с таким айди',
                             reply_markup=keyboard_start())

    await state.clear()
