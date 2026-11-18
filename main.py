import asyncio
import logging
from config import dp, bot
from database import init_db
from logger_config import setup_logger
from handlers import (start, fallback, add_expense, stats, chart, list_expenses,
                      delete_id_expense, delete_all_expenses)


async def main() -> None:
    setup_logger()

    init_db()

    dp.include_routers(
        start.router,
        add_expense.router,
        stats.router,
        chart.router,
        list_expenses.router,
        delete_id_expense.router,
        delete_all_expenses.router,
        fallback.router
    )

    logging.info('Запуск бота...')

    try:
        while True:
            try:
                await dp.start_polling(bot, polling_timeout=10, close_bot_session=False)
                break
            except Exception as e:
                logging.warning(f"Обрыв связи с Cloudflare: {e}. Переподключение через 3 сек...")
                await asyncio.sleep(3)
    except asyncio.CancelledError:
        pass
    finally:
        await bot.session.close()
        logging.info('Бот остановлен корректно')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Остановка по команде пользователя...')
