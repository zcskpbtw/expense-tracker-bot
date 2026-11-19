from aiogram import Router,types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from keyboards import keyboard_start
from database import set_default_categories

router = Router(name='start')

## waiting command start
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:

    await state.clear()

    set_default_categories(message.from_user.id)

    await message.answer('Привет! Я твой бот для учета трат, что-бы добавить трату или посмотреть статистику, жми на кнопки!\n\n'
                         'Для помощи: /help',
                         reply_markup=keyboard_start())

## waiting command help
@router.message(Command('help'))
async def cmd_help(message: Message, state: FSMContext) -> None:

    await state.clear()

    await message.answer('/start - Запустить бота \n'
                         '/help - Помощь \n'
                         '/add - Добавить трату \n'
                         '/stats - Посмотреть статистику \n'
                         '/chart - Построить диаграмму трат \n'
                         '/list - Список трат \n'
                         '/delete - Удалить трату \n'
                         '/delete_all - Удалить все траты')
