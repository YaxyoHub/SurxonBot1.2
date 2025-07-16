import asyncio
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InputMediaPhoto
from aiogram.fsm.context import FSMContext

from data.needfull_funcs import IsAdmin
from database.sql import get_user
from database.toy_sql import add_toy
from data.config import CHANNELS, ADMINS
from states.states import AddToyState
from admin_handlers.admin_keyboards import admin_menu

add_toy_router = Router()


# ➕ O'yinchoq qo‘shishni boshlash
@add_toy_router.callback_query(F.data == "add_toy", IsAdmin())
async def start_adding_toy(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("🧸 O'yinchoq nomini kiriting:")
    await state.set_state(AddToyState.name)


# 📝 O'yinchoq nomi
@add_toy_router.message(AddToyState.name)
async def get_name(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer("💰 O'yinchoq narxini kiriting (faqat sonlarda 10000):")
    await state.set_state(AddToyState.price)


# 💵 Narx
@add_toy_router.message(AddToyState.price)
async def get_price(msg: Message, state: FSMContext):
    if not msg.text.isdigit():
        return await msg.answer("❌ Iltimos, raqam kiriting (masalan: 75000)")
    await state.update_data(price=int(msg.text))
    await msg.answer("📝 O'yinchoq tavsifini yozing:")
    await state.set_state(AddToyState.description)


# 📄 Tavsif
@add_toy_router.message(AddToyState.description)
async def get_description(msg: Message, state: FSMContext):
    await state.update_data(description=msg.text)
    await msg.answer("🖼 Endi 1 dona rasm yuboring:")
    await state.set_state(AddToyState.photos)


# 🖼 Rasm (1 dona)
@add_toy_router.message(AddToyState.photos, F.photo)
async def get_photo(msg: Message, state: FSMContext):
    file_id = msg.photo[-1].file_id
    await state.update_data(photos=[file_id])
    await msg.answer("✅ Rasm qabul qilindi. Xabarlar jo‘natilmoqda...")

    data = await state.get_data()

    # 🧸 Bazaga qo‘shish
    add_toy(
        name=data["name"],
        price=data["price"],
        description=data["description"],
        photos=data["photos"]
    )

    text = (
        f"<b>🧸 Yangi o'yinchoq!</b>\n\n"
        f"🧸: <b>{data['name']}</b>\n"
        f"💰 Narxi: {data['price']} so‘m\n"
        f"📝 {data['description']}\n\n"
        f"Ushbu o'yinchoq botga joylandi ✅\n"
        f"Buyurtma uchun: @surhon_gullari_bot"
    )

    media = [InputMediaPhoto(media=file_id, caption=text, parse_mode="HTML")]

    # 📢 Kanalga yuborish
    try:
        if isinstance(CHANNELS, list):
            for ch in CHANNELS:
                await msg.bot.send_media_group(chat_id=ch, media=media)
        else:
            await msg.bot.send_media_group(chat_id=CHANNELS, media=media)
    except Exception as e:
        for admin in ADMINS:
            try:
                await msg.bot.send_message(admin, f"❌ Kanalga yuborishda xatolik:\n<code>{e}</code>", parse_mode="HTML")
            except:
                pass

    # 👥 Foydalanuvchilarga yuborish
    users = get_user()
    sent = 0
    for user in users:
        user_id = user['user_id'] if isinstance(user, dict) else user[1]
        try:
            await msg.bot.send_media_group(chat_id=user_id, media=media)
            sent += 1
        except:
            continue
        await asyncio.sleep(0.05)

    await msg.answer(f"✅ O'yinchoq qo‘shildi va {sent} ta foydalanuvchiga yuborildi!", reply_markup=admin_menu)
    await state.clear()
