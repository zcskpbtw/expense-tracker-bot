from aiogram import Router, F, types
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio

from database import delete_id_expense, get_list_expenses
from keyboards import keyboard_start

router = Router(name='delete')

## waiting command delete
@router.message(F.text.in_({'/delete', 'Удалить трату'}))
async def get_expenses(message: Message, state: FSMContext) -> None:
    await state.clear()

    expenses = get_list_expenses(telegram_id=message.from_user.id)
    if not expenses:
        await message.answer('У вас пока что нет трат', reply_markup=keyboard_start())
        return

    text = ''
    builder = InlineKeyboardBuilder()

    for cnt, (e_id, category, amount, date) in enumerate(expenses, start=1):
        text += f"{cnt}. {category} -- {amount} | {date}\n"

        builder.add(types.InlineKeyboardButton(
            text=str(cnt),
            callback_data=f"delete_{e_id}"
        ))

    builder.adjust(3)
    text = f'Ваши последние траты ({len(expenses)}):\n' + text
    text += '\n\nВыберите номер траты, которую хотите удалить:'

    await message.answer(text,  reply_markup=builder.as_markup())

## waiting delete_id
@router.callback_query(F.data.startswith("delete_"))
async def process_delete_callback(callback: CallbackQuery) -> None:
    real_exp_id = int(callback.data.split("_")[1])

    if delete_id_expense(exp_id=real_exp_id, telegram_id=callback.from_user.id) > 0:
        await callback.message.edit_text('Удаляю трату...')
        await asyncio.sleep(1)
        await callback.message.edit_text(f'Трата id:{real_exp_id} успешно удалена!')
    else:
        await callback.message.edit_text('Удаляю трату...')
        await asyncio.sleep(1)
        await callback.message.edit_text('Ошибка: трата не найдена или уже удалена.')

    await callback.answer()