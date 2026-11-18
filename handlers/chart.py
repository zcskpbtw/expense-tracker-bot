from aiogram import Router, F
from aiogram.types import Message, BufferedInputFile
from aiogram.fsm.context import FSMContext

# Импортируем наши функции
from database import get_expenses_for_chart  # Эту функцию тебе нужно будет написать в database.py
from charts import create_pie_chart

router = Router(name='chart')


@router.message(F.text.in_({'/chart', 'График'}))
async def send_chart(message: Message, state: FSMContext):
    # 1. Сбрасываем состояние (если пользователь был в процессе добавления траты)
    await state.clear()

    # 2. Получаем данные из базы
    data = get_expenses_for_chart(message.from_user.id)

    # 3. Проверяем, есть ли вообще данные
    if not data:
        await message.answer('У вас пока нет трат для построения графика.')
        return

    # 4. Отправляем сообщение "Загрузка...", так как генерация графика может занять секунду
    loading_msg = await message.answer('⏳ Строю график...')

    # 5. Генерируем график
    chart_buffer = create_pie_chart(data)

    if chart_buffer:
        # 6. Создаем объект файла для Telegram
        # BufferedInputFile берет данные из памяти и говорит Телеграму, что это картинка
        photo = BufferedInputFile(chart_buffer.getvalue(), filename="chart.png")

        # 7. Отправляем фото
        await message.answer_photo(
            photo=photo,
            caption="📊 Ваши траты по категориям"
        )

        # 8. Удаляем сообщение "Загрузка..."
        await loading_msg.delete()
    else:
        await loading_msg.edit_text('Не удалось построить график.')