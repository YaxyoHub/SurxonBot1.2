from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def subscription_check_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔗 Kanalga o‘tish", url="https://t.me/+yGG3li2r0A9mMTEy")],
        [InlineKeyboardButton(text="✅ Obuna bo‘ldim", callback_data="check_sub")]
    ])


def build_flower_list_kb(flowers: list[dict]):
    kb = InlineKeyboardMarkup(inline_keyboard=[])
    for flower in flowers:
        btn = InlineKeyboardButton(
            text=f"{flower['name']} — {flower['price']}",
            callback_data=f"flower:{flower['id']}:0"
        )
        kb.inline_keyboard.append([btn])
    return kb


def flower_navigation_keyboard(flower_id: str, page: int, max_photos: int):
    buttons = []

    if page > 0:
        buttons.append(InlineKeyboardButton(
            text="⬅️ Oldingi", callback_data=f"flower:{flower_id}:{page - 1}"
        ))
    if page < max_photos - 1:
        buttons.append(InlineKeyboardButton(
            text="➡️ Keyingi", callback_data=f"flower:{flower_id}:{page + 1}"
        ))

    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 Buyurtma qilish", callback_data=f"order:{flower_id}")],
        buttons
    ])

accept_btn = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Qabul qilish ✅", callback_data='accept_yes')]
    ]
)

flower_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🌸 Gullar bo'limi", callback_data='choose_flower')],
        [InlineKeyboardButton(text="🧸 O'yinchoqlar bo'limi", callback_data='choose_toy')],
        [InlineKeyboardButton(text="ℹ️ Bot haqida", callback_data="about_bot")],
        [InlineKeyboardButton(text="📲 Biz bilan bog'lanish", callback_data="connect_us")]
    ]
)

cancel_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='❌ Bekor qilish', callback_data='cancel')]
    ]
)

back_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='🔙 Ortga qaytish', callback_data='back_user_menu')]
    ]
)