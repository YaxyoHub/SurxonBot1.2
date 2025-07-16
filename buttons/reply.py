from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

phone_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Telefon raqam ulashish', request_contact=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

location_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Lokatsiya ulashish', request_location=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)