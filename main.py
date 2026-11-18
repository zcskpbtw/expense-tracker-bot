import asyncio
from config import dp,bot
from database import init_db
from handlers import (start, fallback, add_expense, stats, chart, list_expenses,
                      delete_id_expense, delete_all_expenses)


async def main() -> None:
    init_db()

    dp.include_router(start.router)
    dp.include_router(add_expense.router)
    dp.include_router(stats.router)
    dp.include_router(chart.router)
    dp.include_router(list_expenses.router)
    dp.include_router(delete_id_expense.router)
    dp.include_router(delete_all_expenses.router)
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
