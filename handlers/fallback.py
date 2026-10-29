from aiogram import Router
from aiogram.types import Message


router = Router(name='fallback')


@router.message()
async def any_message(message: Message) -> None:
    await message.answer('Я тебя не понимаю. Напиши /help')