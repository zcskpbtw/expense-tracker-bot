from aiogram import Router, F
from aiogram.types import Message, BufferedInputFile
from aiogram.fsm.context import FSMContext

from database import get_expenses_for_chart
from charts import create_pie_chart


router = Router(name='chart')

## waiting command chart
@router.message(F.text.in_({'/chart', 'График'}))
async def send_chart(message: Message, state: FSMContext):

    await state.clear()

    data = get_expenses_for_chart(message.from_user.id)

    if not data:
        await message.answer('У вас пока нет трат для построения графика.')
        return

    loading_msg = await message.answer('⏳ Строю график...')

    chart_buffer = create_pie_chart(data)

    if chart_buffer:

        photo = BufferedInputFile(chart_buffer.getvalue(), filename="chart.png")

        await message.answer_photo(
            photo=photo,
            caption="📊 Ваши траты по категориям"
        )

        await loading_msg.delete()
    else:
        await loading_msg.edit_text('Не удалось построить график.')