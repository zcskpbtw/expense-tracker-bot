from aiogram import types
from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


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
        [types.KeyboardButton(text='График')],
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
        resize_keyboard=True
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

def keyboard_categories(categories: list[str]):
    builder = ReplyKeyboardBuilder()

    for category in categories:
        builder.button(text=category)


    builder.adjust(3)


    btn1 = KeyboardButton(text='Добавить категорию')
    btn2 = KeyboardButton(text='Удалить категорию')

    if len(categories) < 9:
        builder.row(btn1,btn2)
    else:
        builder.row(btn2)

    builder.row(KeyboardButton(text='Отмена'))

    return builder.as_markup(resize_keyboard=True)