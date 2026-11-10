from aiogram.fsm.context import FSMContext
from database import get_all_expenses, get_max_expense, avg_expenses, get_list_expenses
from aiogram import Router, F
from aiogram.types import Message

# переход выполнен

router = Router(name='stats')


@router.message(F.text.in_({'/stats', 'Статистика'}))
async def stats(message: Message, state: FSMContext):

    await state.clear()

    text = ''

    if not get_list_expenses(message.from_user.id):
        await message.answer('У вас пока что не трат')
        return

    for amount, days in get_all_expenses(message.from_user.id):
        text += f'Всего за период ({days}), было потрачено: {amount} руб.\n\n'

    for date, category, amount in get_max_expense(message.from_user.id):
        text += f'Максимальная трата \nДата: {date} | {category} - {amount} руб. \n\n'

    for amounts, days in avg_expenses(message.from_user.id):
        try:
            text += f'За эти дни в среднем было потрачено: {amounts/days} руб.'
        except ZeroDivisionError:
            await message.answer('Нет трат!')
            return

    await message.answer(text)



