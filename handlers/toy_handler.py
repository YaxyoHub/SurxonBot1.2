from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message
from loader import bot
from database.toy_sql import get_toy
from buttons.inline import flower_button

toy_view_router = Router()


# 🔘 Barcha o‘yinchoqlarni ko‘rish
@toy_view_router.callback_query(F.data == "choose_toy")
async def show_first_toy(callback: CallbackQuery):
    await callback.message.delete()

    toys = get_toy()
    if not toys:
        return await callback.message.answer("❌ O‘yinchoqlar topilmadi.")

    await send_toy(callback.message, toys, index=0)


# 🔁 Navbatdagi yoki oldingi o‘yinchoq
@toy_view_router.callback_query(F.data.startswith("toy_page:"))
async def paginate_toys(callback: CallbackQuery):
    await callback.message.delete()

    _, index = callback.data.split(":")
    index = int(index)

    toys = get_toy()
    if index < 0 or index >= len(toys):
        return await callback.message.answer("❌ Bunday sahifa mavjud emas.")

    await send_toy(callback.message, toys, index)


# 📦 O‘yinchoqni yuboruvchi asosiy funksiya
async def send_toy(msg: Message, toys: list, index: int):
    toy = toys[index]
    toy_id = toy["id"]
    name = toy["name"]
    price = toy["price"]
    desc = toy["description"]
    photos = toy["photos"]

    caption = (
        f"<b>🧸 {name}</b>\n"
        f"💰 Narxi: {price} UZS\n\n"
        f"{desc if desc else ''}"
    )

    # 🔘 Tugmalarni quramiz
    buttons = []

    nav_buttons = []
    if index > 0:
        nav_buttons.append(
            InlineKeyboardButton(text="◀️ Oldingi", callback_data=f"toy_page:{index - 1}")
        )
    if index < len(toys) - 1:
        nav_buttons.append(
            InlineKeyboardButton(text="Keyingi ▶️", callback_data=f"toy_page:{index + 1}")
        )
    if nav_buttons:
        buttons.append(nav_buttons)

    buttons.append([
        InlineKeyboardButton(text="📦 Buyurtma berish", callback_data=f"toy:{toy_id}")
    ])
    buttons.append([
        InlineKeyboardButton(text="🔙 Ortga", callback_data="back_to_flower")
    ])

    markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    # 🔽 Rasm + caption
    if photos:
        await msg.answer_photo(
            photo=photos[0],
            caption=caption,
            parse_mode="HTML",
            reply_markup=markup
        )
    else:
        await msg.answer(
            text=caption,
            parse_mode="HTML",
            reply_markup=markup
        )


# 🔙 Ortga bosilganda
@toy_view_router.callback_query(F.data == "back_to_flower")
async def go_back(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("🔙 Asosiy bo‘limga qaytdingiz.", reply_markup=flower_button)
