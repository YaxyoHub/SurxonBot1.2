import asyncio
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from admin_handlers.admin_keyboards import admin_menu
from states.states import DeleteFlowerState
from database.sql import get_all_flowers, delete_flower_by_id

del_flower_router = Router()

# 1. Boshlanish
@del_flower_router.callback_query(F.data == "see_flower")
async def start_deleting(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.set_state(DeleteFlowerState.page)
    await state.update_data(page=0)
    await show_delete_page(callback.message, 0)


# 2. Sahifani chiqarish (message yuborish uchun, yangi message yaratadi)
async def show_delete_page(message: Message, page: int):
    flowers = get_all_flowers()
    if not flowers:
        return await message.answer("❗️ Hozircha gul yo‘q.")

    per_page = 1
    total = len(flowers)
    start = page * per_page
    end = start + per_page

    if start >= total:
        page = 0
        start = 0
        end = per_page

    flower = flowers[start]
    text = (
        f"<b>{flower['name']}</b>\n"
        f"💰 {flower['price']} so‘m\n"
        f"📝 {flower.get('description', 'Tavsif yo‘q')}"
    )

    # 🔘 Tugmalar
    buttons = [
        [InlineKeyboardButton(text="🗑 O‘chirish", callback_data=f"delete:{flower['id']}")]
    ]

    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data="prev_d"))
    if end < total:
        nav_buttons.append(InlineKeyboardButton(text="➡️ Keyingi", callback_data="next_d"))
    if nav_buttons:
        buttons.append(nav_buttons)

    buttons.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_admin")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    try:
        await message.answer_photo(photo=flower['photos'][0], caption=text, parse_mode="HTML", reply_markup=keyboard)
    except Exception:
        await message.answer(text=text, parse_mode="HTML", reply_markup=keyboard)


# Yangi: Sahifani tahrirlash uchun funktsiya
async def edit_delete_page(callback: CallbackQuery, page: int):
    flowers = get_all_flowers()
    if not flowers:
        return await callback.message.edit_caption("❗️ Hozircha gul yo‘q.", reply_markup=None)

    per_page = 1
    total = len(flowers)
    start = page * per_page
    end = start + per_page

    if start >= total:
        page = 0
        start = 0
        end = per_page

    flower = flowers[start]
    text = (
        f"Nomi: <b>{flower['name']}</b>\n"
        f"💰 Narxi: {flower['price']} so‘m\n"
        f"📝 Tavsif: {flower.get('description', 'Tavsif yo‘q')}"
    )

    buttons = [
        [InlineKeyboardButton(text="🗑 O‘chirish", callback_data=f"delete:{flower['id']}")]
    ]

    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data="prev_d"))
    if end < total:
        nav_buttons.append(InlineKeyboardButton(text="➡️ Keyingi", callback_data="next_d"))
    if nav_buttons:
        buttons.append(nav_buttons)

    buttons.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_admin")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    try:
        # Rasm o'zgarishi uchun media tahrirlash
        media = InputMediaPhoto(media=flower['photos'][0], caption=text, parse_mode="HTML")
        await callback.message.edit_media(media=media, reply_markup=keyboard)
    except Exception:
        # Agar rasm bo'lmasa yoki tahrirlashda xatolik bo'lsa, captionni tahrirlashga urinadi
        await callback.message.edit_caption(caption=text, parse_mode="HTML", reply_markup=keyboard)


# 3. O'chirish
@del_flower_router.callback_query(F.data.startswith("delete:"))
async def delete_flower(callback: CallbackQuery, state: FSMContext):
    try:
        flower_id = int(callback.data.split(":")[1])
        delete_flower_by_id(flower_id)
        await callback.answer("✅ Gul o‘chirildi!", show_alert=True)

        data = await state.get_data()
        await callback.message.delete()
        await show_delete_page(callback.message, data.get("page", 0))

    except Exception as e:
        await callback.answer("❌ O‘chirishda xatolik!", show_alert=True)
        print(f"[delete_flower ERROR] {e}")


# 4. Navigatsiya (edit qilish)
@del_flower_router.callback_query(F.data.in_(["prev_d", "next_d"]))
async def navigate(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    page = data.get("page", 0)

    if callback.data == "next_d":
        page += 1
    elif callback.data == "prev_d":
        page = max(0, page - 1)

    await state.update_data(page=page)

    # Mavjud message ni o'chirish emas, balki edit qilish
    await edit_delete_page(callback, page)
    await callback.answer()  # to‘g‘ri tugma bosilgani uchun javob berish


# 5. Orqaga
@del_flower_router.callback_query(F.data == "back_admin")
async def back_menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.clear()
    await callback.message.answer("🔧 Admin panelga qaytdingiz", reply_markup=admin_menu)
