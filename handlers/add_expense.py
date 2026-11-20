from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from datetime import date,datetime

from database import add_expense, get_user_categories, add_user_category, delete_category_expenses
from keyboards import keyboard_add, keyboard_start, keyboard_return, keyboard_categories, keyboard_delete_categories, \
    keyboard_accept

router = Router(name='add')

class AddExpense(StatesGroup):
    waiting_date = State()
    waiting_category = State()
    waiting_expense = State()
    waiting_new_category = State()
    waiting_delete_category = State()
    waiting_confirm_delete = State()


## waiting command add
@router.message(F.text.in_({'/add', 'Добавить трату'}))
async def start_add(message: Message,state: FSMContext) -> None:

    await state.clear()


    await message.answer("Введите дату траты \n"
                         "Пример: сегодня или 2026 01 01 ",
                         reply_markup=keyboard_add())
    await state.set_state(AddExpense.waiting_date)


## waiting state date
@router.message(AddExpense.waiting_date)
async def process_date(message: Message, state: FSMContext) -> None:

    if not message.text or not message.text.strip():
        await state.clear()
        await message.answer('Неверный формат записи! Отправьте текст.',
                             reply_markup=keyboard_start())
        return

    if message.text.lower() == 'отмена':
        await state.clear()
        await message.answer('Отмена текущего действия',
                             reply_markup=keyboard_start())
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
            await message.answer('Введена некорректная дата',
                                 reply_markup=keyboard_start())
            return

    await message.answer('Введите категорию траты: ',
                         reply_markup=keyboard_categories(get_user_categories(message.from_user.id)))

    await state.set_state(AddExpense.waiting_category)


## waiting state category
@router.message(AddExpense.waiting_category, F.text == 'Добавить категорию')
async def process_add_category(message: Message, state: FSMContext) -> None:
    categories = get_user_categories(message.from_user.id)

    if len(categories) >= 9:
        await message.answer('Вы уже привысили лимит категорий!',
                             reply_markup=keyboard_categories(categories))
        return

    await message.answer('Введите название новой категории (до 20 символов):',
                         reply_markup=keyboard_return())


    await state.set_state(AddExpense.waiting_new_category)


@router.message(AddExpense.waiting_new_category)
async def save_new_category(message: Message, state: FSMContext) -> None:
    categories = get_user_categories(message.from_user.id)

    if not message.text or not message.text.strip():
        await message.answer('Неверный формат записи! Отправьте текст.',
                             reply_markup=keyboard_categories(categories))
        return

    if message.text.lower() == 'отмена':
        await state.clear()
        await message.answer('Отмена текущего действия',
                             reply_markup=keyboard_start())
        return

    if len(message.text) > 20:
        await message.answer('Название категории больше 20 символов!')
        return

    res = add_user_category(message.from_user.id, message.text)

    if res == 'ok':
        await message.answer(f'Категория {message.text} успешно добавлена!\n\n Можете добавить трату!',
                             reply_markup=keyboard_return())
        await state.update_data(category=message.text.strip().capitalize())
        await state.set_state(AddExpense.waiting_expense)
    elif res == 'exists':
        await message.answer(f'Категория {message.text} уже существует!\n\n Можете добавить трату!',
                             reply_markup=keyboard_return())
        await state.update_data(category=message.text.strip().capitalize())
        await state.set_state(AddExpense.waiting_expense)
    elif res == 'limit':
        await state.clear()
        await message.answer(f'Превышен лимит категорий!',
                             reply_markup=keyboard_categories(categories))
        return


@router.message(AddExpense.waiting_category, F.text == 'Удалить категорию')
async def process_delete_category(message: Message, state: FSMContext) -> None:
    categories = get_user_categories(message.from_user.id)

    await message.answer('Какую категорию удалить?',
                         reply_markup=keyboard_delete_categories(categories))

    await state.set_state(AddExpense.waiting_delete_category)

@router.message(AddExpense.waiting_delete_category)
async def delete_category(message: Message, state: FSMContext) -> None:
    categories = get_user_categories(message.from_user.id)

    if len(categories) <= 1:
        await state.clear()
        await message.answer('Нельзя удалить последнюю категорию! Для начала добавьте еще одну.',
                             reply_markup=keyboard_start())
        return

    if not message.text or not message.text.strip():
        await message.answer('Неверный формат записи! Отправьте текст.',
                             reply_markup=keyboard_categories(categories))
        return

    if message.text.lower() == 'отмена':
        await state.clear()
        await message.answer('Отмена текущего действия',
                             reply_markup=keyboard_start())
        return

    if message.text not in categories:
        await message.answer('Выберите категорию из списка!',
                             reply_markup=keyboard_delete_categories(categories))
        return

    await message.answer('Вы действительно хотите удалить категорию и ВСЕ траты в ней?',
                         reply_markup=keyboard_accept())

    await state.update_data(accept=message.text.strip().capitalize())
    await state.set_state(AddExpense.waiting_confirm_delete)


@router.message(AddExpense.waiting_confirm_delete)
async def delete(message: Message, state: FSMContext) -> None:
    categories = get_user_categories(message.from_user.id)
    data = await state.get_data()
    cat_to_delete = data['accept']

    if not message.text or not message.text.strip():
        await message.answer('Неверный формат записи! Отправьте текст.',
                             reply_markup=keyboard_categories(categories))
        return

    if message.text.strip().capitalize() == 'Да':
        if delete_category_expenses(message.from_user.id, cat_to_delete) > 0:
            await state.clear()
            await message.answer(f'Успешно удалена категория {cat_to_delete} !',
                                 reply_markup=keyboard_start())
            return
        else:
            await state.clear()
            await message.answer('Ошибка!',
                                 reply_markup=keyboard_start())
            return
    elif message.text.strip().capitalize() == 'Отмена':
        await state.clear()
        await message.answer('Отмена текущего действия',
                             reply_markup=keyboard_start())
    else:
        await message.answer('Нажми на кнопки!',
                             reply_markup=keyboard_delete_categories(categories))





@router.message(AddExpense.waiting_category)
async def process_category(message: Message, state: FSMContext) -> None:

    categories = get_user_categories(message.from_user.id)

    if not message.text or not message.text.strip():
        await message.answer('Неверный формат записи! Нажмите на кнопку.',
                             reply_markup=keyboard_categories(categories))
        return

    if message.text.lower() == 'отмена':
        await state.clear()
        await message.answer('Отмена текущего действия',
                             reply_markup=keyboard_start())
        return


    if message.text not in categories:
        await message.answer('Пожалуйста, выберите категорию с помощью кнопок ниже 👇',
                             reply_markup=keyboard_categories(categories))
        return

    await state.update_data(category=message.text.strip().capitalize())
    await message.answer('Введите трату: ',
                         reply_markup=keyboard_return())
    await state.set_state(AddExpense.waiting_expense)

## waiting state expense
@router.message(AddExpense.waiting_expense)
async def process_amount(message: Message, state: FSMContext) -> None:

    if not message.text or not message.text.strip():
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
        amount = int(message.text)
    except ValueError:
        await message.answer('Ошибка! Введите число!',
                             reply_markup=keyboard_start())
        return

    data = await state.get_data()
    add_expense(
        telegram_id = message.from_user.id,
        date = data['date'],
        category_name = data['category'],
        amount = amount
    )

    await state.clear()
    await message.answer(f"Трата {amount} руб. в категории {data['category']} успешно добавлена!",
                         reply_markup=keyboard_start())




