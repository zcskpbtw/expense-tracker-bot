from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from database import delete_by_id,delete_all_exp
from functions import is_valid_text
from keyboards import keyboard_start, keyboard_return, keyboard_accept

router = Router(name='delete_all')

class Delete(StatesGroup):
    waiting_accept = State()

@router.message(Command('delete_all'))
async def get_expenses(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer('Вы уверены что хотите удалить все траты?', reply_markup=keyboard_accept())
    await state.set_state(Delete.waiting_accept)

@router.message(Delete.waiting_accept)
async def delete(message: Message, state: FSMContext):
    if message.text.lower() == 'отмена':
        await message.answer('Отмена текущего действия', reply_markup=keyboard_start())
    elif message.text.lower() == 'да':
        if delete_all_exp(message.from_user.id) > 0:
            await message.answer('Траты успешно удалены!', reply_markup=keyboard_start())
        else:
            await message.answer('Таблица трат пуста!', reply_markup=keyboard_start())
    else:
        await message.answer('Я тебя не понимаю', reply_markup=keyboard_start())
    await state.clear()
