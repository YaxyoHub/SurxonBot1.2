import time, asyncio
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from data.needfull_funcs import IsAdmin
from database.sql import add_flower, get_user
from data.config import CHANNELS, ADMINS
from states.states import AddFlowerState
from admin_handlers.admin_keyboards import admin_menu

add_flower_router = Router()

# ➕ Gul qo‘shishni boshlash
@add_flower_router.callback_query(F.data == "add_flower", IsAdmin())
async def start_adding_flower(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("🌸 Gul nomini kiriting:")
    await state.set_state(AddFlowerState.name)

# ✅ Gul nomi olindi
@add_flower_router.message(AddFlowerState.name)
async def get_name(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer("💰 Gul narxini kiriting:")
    await state.set_state(AddFlowerState.price)

# ✅ Narx olindi
@add_flower_router.message(AddFlowerState.price)
async def get_price(msg: Message, state: FSMContext):
    if not msg.text.isdigit():
        return await msg.answer("❌ Iltimos, raqam kiriting (masalan: 50000)")
    await state.update_data(price=int(msg.text))
    await msg.answer("📝 Tavsifni yozing:")
    await state.set_state(AddFlowerState.description)

# ✅ Tavsif olindi
@add_flower_router.message(AddFlowerState.description)
async def get_description(msg: Message, state: FSMContext):
    await state.update_data(description=msg.text)
    await msg.answer("🖼 Iltimos, 1 dona gul rasmini yuboring.")
    await state.set_state(AddFlowerState.photos)

# 📷 Faqat 1 dona rasm qabul qilish va darhol keyingi bosqichga o‘tish
@add_flower_router.message(AddFlowerState.photos, F.photo)
async def get_photo(msg: Message, state: FSMContext):
    file_id = msg.photo[-1].file_id
    await state.update_data(photos=[file_id])

    await msg.answer("✅ Rasm qabul qilindi.\nXabar Foydalanuvchilarga yuborilmoqda...")

    data = await state.get_data()

    # 🌸 Bazaga yozish
    flower_id = add_flower(
        name=data["name"],
        price=data["price"],
        description=data["description"],
        photos=data["photos"]
    )

    text = (
        f"<b>🌸 Yangi gul!</b>\n\n"
        f"💐: <b>{data['name']}</b>\n"
        f"💰 Narxi: {data['price']} so‘m\n"
        f"📝 {data['description']}\n\n"
        f"Ushbu gul botga joylandi ✅\n"
        f"Bemalol bot orqali buyurtma bershingiz mumkin\n"
        f"🛒 Buyurtma berish uchun: @surhon_gullari_bot"
    )

    media = [InputMediaPhoto(media=file_id, caption=text, parse_mode="HTML")]

    # 🛡 Kanalga yuborish
    try:
        await msg.bot.send_media_group(chat_id=CHANNELS, media=media)
    except Exception as e:
        for admin in ADMINS:
            try:
                await msg.bot.send_message(admin, f"❌ Kanalga yuborishda xatolik:\n<code>{e}</code>", parse_mode="HTML")
            except:
                pass

    # 👤 Foydalanuvchilarga yuborish
    users = get_user()
    sent = 0
    for user in users:
        user_id = user['user_id'] if isinstance(user, dict) else user[1]
        try:
            await msg.bot.send_media_group(chat_id=user_id, media=media)
            sent += 1
        except:
            continue
        await asyncio.sleep(0.05)  # anti-spam

    await msg.answer(f"✅ Gul qo‘shildi va {sent} ta foydalanuvchiga yuborildi!", reply_markup=admin_menu)
    await state.clear()
