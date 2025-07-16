import asyncio
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from admin_handlers.admin_keyboards import admin_menu
from states.states import DeleteToyState
from database.toy_sql import get_toy, delete_toy  # Bu funksiyalar bazadan toy olish va o‘chirish uchun
from data.needfull_funcs import IsAdmin

del_toy_router = Router()


# 1. Boshlanish
@del_toy_router.callback_query(F.data == "see_toy", IsAdmin())
async def start_deleting(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.set_state(DeleteToyState.page)
    await state.update_data(page=0)
    await show_delete_page(callback.message, 0)


# 2. Sahifani chiqarish
async def show_delete_page(message: Message, page: int):
    toys = get_toy()
    if not toys:
        return await message.answer("❗️ Hozircha o‘yinchoqlar yo‘q.")

    per_page = 1
    total = len(toys)
    start = page * per_page
    end = start + per_page

    if start >= total:
        page = 0
        start = 0
        end = per_page

    toy = toys[start]
    text = (
        f"<b>{toy['name']}</b>\n"
        f"💰 {toy['price']} so‘m\n"
        f"📝 {toy.get('description', 'Tavsif yo‘q')}"
    )

    buttons = [
        [InlineKeyboardButton(text="🗑 O‘chirish", callback_data=f"delete_toy:{toy['id']}")]
    ]

    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data="prev_toy"))
    if end < total:
        nav_buttons.append(InlineKeyboardButton(text="➡️ Keyingi", callback_data="next_toy"))
    if nav_buttons:
        buttons.append(nav_buttons)

    buttons.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_admin")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    try:
        await message.answer_photo(photo=toy['photos'][0], caption=text, parse_mode="HTML", reply_markup=keyboard)
    except Exception:
        await message.answer(text=text, parse_mode="HTML", reply_markup=keyboard)


# 3. Sahifani tahrirlash
async def edit_delete_page(callback: CallbackQuery, page: int):
    toys = get_toy()
    if not toys:
        return await callback.message.edit_caption("❗️ Hozircha o‘yinchoqlar yo‘q.", reply_markup=None)

    per_page = 1
    total = len(toys)
    start = page * per_page
    end = start + per_page

    if start >= total:
        page = 0
        start = 0
        end = per_page

    toy = toys[start]
    text = (
        f"Nomi: <b>{toy['name']}</b>\n"
        f"💰 Narxi: {toy['price']} so‘m\n"
        f"📝 Tavsif: {toy.get('description', 'Tavsif yo‘q')}"
    )

    buttons = [
        [InlineKeyboardButton(text="🗑 O‘chirish", callback_data=f"delete_toy:{toy['id']}")]
    ]

    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data="prev_toy"))
    if end < total:
        nav_buttons.append(InlineKeyboardButton(text="➡️ Keyingi", callback_data="next_toy"))
    if nav_buttons:
        buttons.append(nav_buttons)

    buttons.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_admin")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    try:
        media = InputMediaPhoto(media=toy['photos'][0], caption=text, parse_mode="HTML")
        await callback.message.edit_media(media=media, reply_markup=keyboard)
    except Exception:
        await callback.message.edit_caption(caption=text, parse_mode="HTML", reply_markup=keyboard)


# 4. O‘chirish
@del_toy_router.callback_query(F.data.startswith("delete_toy:"))
async def delete_toy_handler(callback: CallbackQuery, state: FSMContext):
    try:
        toy_id = int(callback.data.split(":")[1])
        delete_toy(toy_id)
        await callback.answer("✅ O‘yinchoq o‘chirildi!", show_alert=True)

        data = await state.get_data()
        await callback.message.delete()
        await show_delete_page(callback.message, data.get("page", 0))

    except Exception as e:
        await callback.answer("❌ O‘chirishda xatolik!", show_alert=True)
        print(f"[delete_toy ERROR] {e}")


# 5. Navigatsiya
@del_toy_router.callback_query(F.data.in_(["prev_toy", "next_toy"]))
async def navigate(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    page = data.get("page", 0)

    if callback.data == "next_toy":
        page += 1
    elif callback.data == "prev_toy":
        page = max(0, page - 1)

    await state.update_data(page=page)
    await edit_delete_page(callback, page)
    await callback.answer()


# 6. Orqaga
@del_toy_router.callback_query(F.data == "back_admin")
async def back_menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.clear()
    await callback.message.answer("🔧 Admin panelga qaytdingiz", reply_markup=admin_menu)
