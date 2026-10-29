from aiogram.filters import Command
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from database import add_expense


router = Router(name='add')

class AddExpense(StatesGroup):
    waiting_date = State()
    waiting_category = State()
    waiting_expense = State()


@router.message(Command('add'))
async def start_add(message: Message, state: FSMContext) -> None:
    await message.answer("Введите дату траты: ")
    await state.set_state(AddExpense.waiting_date)

@router.message(AddExpense.waiting_date)
async def process_date(message: Message, state: FSMContext) -> None:
    await state.update_data(date=message.text)
    await message.answer('Введите категорию траты: ')
    await state.set_state(AddExpense.waiting_category)

@router.message(AddExpense.waiting_category)
async def process_category(message: Message, state: FSMContext) -> None:
    await state.update_data(category=message.text)
    await message.answer('Введите трату: ')
    await state.set_state(AddExpense.waiting_expense)

@router.message(AddExpense.waiting_expense)
async def process_amount(message: Message, state: FSMContext) -> None:
    try:
        amount = int(message.text)
    except ValueError:
        await message.answer('Ошибка! Введите число!')
        return
    data = await state.get_data()

    add_expense(
        user_id = message.from_user.id,
        date = data['date'],
        category = data['category'],
        amount = amount
    )
    await state.clear()
    await message.answer(f'Трата {amount} руб. в категории {data['category']} успешно добавлена!')




