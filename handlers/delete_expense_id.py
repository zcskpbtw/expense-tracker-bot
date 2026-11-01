from aiogram.filters import Command
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from database import delete_by_id
from functions import is_valid_text


router = Router(name='delete')

class Delete(StatesGroup):
    waiting_id = State()

@router.message(Command('delete'))
async def get_expenses(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer('Введите айди траты которую хотите удалить')
    await state.set_state(Delete.waiting_id)

@router.message(Delete.waiting_id)
async def process_date(message: Message, state: FSMContext) -> None:
    if not is_valid_text(message.text):
        await message.answer('Неверный формат записи! Отправьте текст.')
        return
    try:
        exp_id = int(message.text)
    except ValueError:
        await message.answer('Ошибка! Введите число!')
        return

    if delete_by_id(exp_id=exp_id,
                    user_id=message.from_user.id) > 0:
        await message.answer('Трата успешно удалена!')
    else:
        await message.answer('Нет траты с таким id')

    await state.clear()
