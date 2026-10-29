import asyncio
from config import dp,bot
from handlers import start,fallback


async def main() -> None:
    dp.include_router(start.router)
    dp.include_router(fallback.router)

    print('запуск бота')

    try:
        await dp.start_polling(bot)
    except asyncio.CancelledError:
        pass
    finally:
        await bot.session.close()
        print('бот остановлен корректно')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Остановка по команде пользователя...')