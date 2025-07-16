from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

admin_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📢 Reklama yuborish", callback_data='send_ads')],
        [InlineKeyboardButton(text="👥 Foydalanuvchilarni ko'rish", callback_data='see_users')],
        [InlineKeyboardButton(text="➕ Yangi Gul qo'shish", callback_data='add_flower')],
        [InlineKeyboardButton(text="➕ Yangi O'yinchoq qo'shish", callback_data='add_toy')],
        [InlineKeyboardButton(text="📋 Ro'yxatdagi barcha Gullarni ko'rish", callback_data='see_flower')],
        [InlineKeyboardButton(text="🎲 Ro'yxatdagi barcha O'yinchoqlarni ko'rish", callback_data='see_toy')]
    ]
)