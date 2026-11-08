from aiogram import types

def keyboard_add():
    kb = [
        [types.KeyboardButton(text='Сегодня')],
        [types.KeyboardButton(text='Отмена')]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder='Введите дату:'
    )
    return keyboard

def keyboard_start():
    kb = [
        [types.KeyboardButton(text='Добавить трату')],
        [types.KeyboardButton(text='Статистика')],
        [types.KeyboardButton(text='Список трат')],
        [types.KeyboardButton(text='Удалить трату')]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder='Выберите действие:'
    )
    return keyboard

def keyboard_return():
    kb = [
        [types.KeyboardButton(text='Отмена')]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder='Введите айди траты:'
    )
    return keyboard

def keyboard_accept():
    kb = [
        [types.KeyboardButton(text='Да')],
        [types.KeyboardButton(text='Отмена')]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    return keyboard