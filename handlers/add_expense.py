from functions import is_valid_text
from aiogram.filters import Command
from aiogram import Router,types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from database import add_expense
from datetime import date,datetime


router = Router(name='add')

class AddExpense(StatesGroup):
    waiting_date = State()
    waiting_category = State()
    waiting_expense = State()


@router.message(Command('add'))
async def start_add(message: Message,state: FSMContext) -> None:
    kb =[
        [types.KeyboardButton(text='Сегодня')],
        [types.KeyboardButton(text='Отмена')]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder='Введите дату'
        )
    await message.answer("Введите дату траты \n"
                         "Пример: сегодня или 2026 01 01 ", reply_markup=keyboard)
    await state.set_state(AddExpense.waiting_date)

@router.message(AddExpense.waiting_date)
async def process_date(message: Message, state: FSMContext) -> None:
    if not is_valid_text(message.text):
        await message.answer('Неверный формат записи! Отправьте текст.')
        return


    if message.text.lower() == 'отмена':
        await state.clear()
        await message.answer('Отмена текущего действия', reply_markup=types.ReplyKeyboardRemove())
        return
    elif message.text.lower() == 'сегодня':
        msg = date.today().strftime('%Y-%m-%d')
        await state.update_data(date=msg)
    else:
        msg = message.text.replace(' ','-')
        try:
            valid_date = datetime.strptime(msg, '%Y-%m-%d')
            await state.update_data(date=valid_date.strftime('%Y-%m-%d'))
        except ValueError:
            await message.answer('Введена некорректная дата')
            return

    await message.answer('Введите категорию траты: ', reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddExpense.waiting_category)

@router.message(AddExpense.waiting_category)
async def process_category(message: Message, state: FSMContext) -> None:
    if not is_valid_text(message.text):
        await message.answer('Неверный формат записи! Отправьте текст.')
        return
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




