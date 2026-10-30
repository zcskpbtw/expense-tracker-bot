from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command


router = Router(name='start')

@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer('Привет! Я твой бот для учета трат, что-бы добавить трату или посмотреть статистику, жми на кнопки!')

@router.message(Command('help'))
async def cmd_help(message: Message) -> None:
    await message.answer('/start - Перезапустить бота \n'
                         '/help  - Помощь \n'
                         '/stats - Посмотреть статистику \n'
                         '/add   - Добавить трату \n'
                         '/delete  - Удалить трату \n')
