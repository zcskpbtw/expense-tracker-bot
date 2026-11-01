from aiogram import Router,types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from keyboards import keyboard_start


router = Router(name='start')


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer('Привет! Я твой бот для учета трат, что-бы добавить трату или посмотреть статистику, жми на кнопки!\n\n'
                         'Для помощи: /help',
                         reply_markup=keyboard_start())

@router.message(Command('help'))
async def cmd_help(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer('/start - Перезапустить бота \n'
                         '/help  - Помощь \n'
                         '/stats - Посмотреть статистику \n'
                         '/add   - Добавить трату \n'
                         '/list  - Список для удаления \n'
                         '/delete  - Удалить трату \n'
                         '/delete_all - Удалить все траты \n')
