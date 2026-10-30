import asyncio
from config import dp,bot
from handlers import start,fallback,add_expense,get_all_expenses,delete_expense_id


async def main() -> None:
    dp.include_router(start.router)
    dp.include_router(add_expense.router)
    dp.include_router(get_all_expenses.router)
    dp.include_router(delete_expense_id.router)
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
