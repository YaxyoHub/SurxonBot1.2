import asyncio
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import InputMediaPhoto
from aiogram.fsm.context import FSMContext

from buttons.inline import flower_button
from states.states import DeleteFlowerState
from database.sql import get_all_flowers
from loader import bot

flower_router = Router()

# 🟢 Boshlanishi
@flower_router.callback_query(F.data == "choose_flower")
async def start_deleting(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.set_state(DeleteFlowerState.page)
    await state.update_data(page=0)
    await show_delete_page(callback.message.chat.id, 0, state)

# 🔁 Sahifani ko‘rsatish
async def show_delete_page(chat_id: int, page: int, state: FSMContext):
    flowers = get_all_flowers()
    if not flowers:
        await bot.send_message(chat_id, "❗️ Hozircha hech qanday gul yo‘q.", reply_markup=flower_button)
        return

    per_page = 1
    total = len(flowers)
    start = page * per_page
    if start >= total:
        page = 0
        start = 0

    flower = flowers[start]

    photo = flower["photos"][0] if flower["photos"] else None

    caption = (
        f"💐 Nomi: <b>{flower['name']}</b>\n"
        f"💰 Narxi: {flower['price']} so‘m\n"
        f"📝 Tavsif: {flower.get('description', 'Tavsif yo‘q')}"
    )

    buttons = [
        [InlineKeyboardButton(text="Buyurtma qilish", callback_data=f"order:{flower['id']}")]
    ]
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data="prev"))
    if start + per_page < total:
        nav_buttons.append(InlineKeyboardButton(text="➡️ Keyingi", callback_data="next"))
    if nav_buttons:
        buttons.append(nav_buttons)
    buttons.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_menu")])
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    msg = await bot.send_photo(chat_id, photo=photo, caption=caption, parse_mode="HTML", reply_markup=markup)

    await state.update_data(
        page=page,
        message_id=msg.message_id
    )

# ⬅️➡️ Sahifalar orasida yurish
@flower_router.callback_query(F.data.in_(["prev", "next"]))
async def navigate(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    page = data.get("page", 0)

    if callback.data == "next":
        page += 1
    elif callback.data == "prev":
        page = max(0, page - 1)

    flowers = get_all_flowers()
    total = len(flowers)
    start = page
    if start >= total:
        page = 0
        start = 0

    flower = flowers[start]
    photo = flower["photos"][0] if flower["photos"] else None

    caption = (
        f"Nomi: <b>{flower['name']}</b>\n"
        f"💰 Narxi: {flower['price']} so‘m\n"
        f"📝 Tavsif: {flower.get('description', 'Tavsif yo‘q')}"
    )

    buttons = [
        [InlineKeyboardButton(text="Buyurtma qilish", callback_data=f"order:{flower['id']}")]
    ]
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data="prev"))
    if start + 1 < total:
        nav_buttons.append(InlineKeyboardButton(text="➡️ Keyingi", callback_data="next"))
    if nav_buttons:
        buttons.append(nav_buttons)
    buttons.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_menu")])
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    try:
        await callback.message.edit_media(
            media=InputMediaPhoto(media=photo, caption=caption, parse_mode="HTML"),
            reply_markup=markup
        )
    except Exception as e:
        print(f"Edit media error: {e}")

    await state.update_data(page=page, message_id=callback.message.message_id)


# 🔙 Orqaga qaytish
@flower_router.callback_query(F.data == "back_menu")
async def back_menu(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    # Eski postni o‘chirish
    old_msg_id = data.get("message_id")
    if old_msg_id:
        try:
            await bot.delete_message(callback.message.chat.id, old_msg_id)
        except:
            pass

    await state.clear()
    await bot.send_message(callback.message.chat.id, "Asosiy menuga qaytdingiz", reply_markup=flower_button)
