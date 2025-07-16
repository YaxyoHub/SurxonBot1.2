import os
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from buttons.reply import phone_button, location_button
from buttons.inline import flower_button
from database.toy_sql import get_toy_by_id
from loader import bot

# .env dan GROUP_ID ni olish
group_id = os.getenv("GROUP_ID")

order_toy_router = Router()


# 🔘 FSM: buyurtma bosqichlari
class ToyOrderState(StatesGroup):
    name = State()
    phone = State()
    quantity = State()
    location = State()


# 📦 Buyurtma tugmasi bosilganda
@order_toy_router.callback_query(F.data.startswith("toy:"))
async def start_order(callback: CallbackQuery, state: FSMContext):
    _, toy_id = callback.data.split(":")
    await state.update_data(toy_id=toy_id)

    await callback.message.answer("👤 Iltimos, to‘liq ismingizni yozing:")
    await state.set_state(ToyOrderState.name)


# 👤 Ism
@order_toy_router.message(ToyOrderState.name)
async def get_name(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer("📞 Telefon raqamingizni yuboring:", reply_markup=phone_button)
    await state.set_state(ToyOrderState.phone)


# ☎️ Telefon
@order_toy_router.message(ToyOrderState.phone)
async def get_phone(msg: Message, state: FSMContext):
    phone = msg.contact.phone_number if msg.contact else msg.text
    await state.update_data(phone=phone)

    await msg.answer("🔢 Miqdorni kiriting (nechta buyurtma qilmoqchisiz):")
    await state.set_state(ToyOrderState.quantity)


# 🔢 Miqdor
@order_toy_router.message(ToyOrderState.quantity)
async def get_quantity(msg: Message, state: FSMContext):
    if not msg.text.isdigit():
        return await msg.answer("❗️ Iltimos, raqam kiriting. Masalan: 2")

    await state.update_data(quantity=int(msg.text))
    await msg.answer("📍 Lokatsiyangizni yuboring:", reply_markup=location_button)
    await state.set_state(ToyOrderState.location)


# 📍 Lokatsiya
@order_toy_router.message(ToyOrderState.location, F.location)
async def get_location(msg: Message, state: FSMContext):
    latitude = msg.location.latitude
    longitude = msg.location.longitude
    await state.update_data(lat=latitude, lon=longitude)

    # ✅ Foydalanuvchiga tasdiq
    await msg.answer("✅ Buyurtmangiz qabul qilindi! Tez orada siz bilan bog‘lanamiz.", reply_markup=flower_button)

    data = await state.get_data()
    toy_id = data["toy_id"]
    toy, photos = get_toy_by_id(toy_id)

    # 📩 Guruhga yuborish
    caption = (
        f"📥 <b>Yangi buyurtma!</b>\n\n"
        f"🧸 O'yinchoq: <b>{toy['name']}</b>\n"
        f"💰 Narxi: {toy['price']} so‘m\n"
        f"🔢 Miqdor: {data['quantity']} ta\n\n"
        f"👤 Ism: <b>{data['name']}</b>\n"
        f"📞 Telefon: <b>{data['phone']}</b>\n"
        f"🇺🇿 Telegram: @{msg.from_user.username}\n"
        f"📍 Lokatsiya: <a href='https://maps.google.com/?q={latitude},{longitude}'>Xaritada ko‘rish</a>\n"
        f"🆔 User ID: <code>{msg.from_user.id}</code>"
    )

    try:
        if photos:
            await bot.send_photo(
                chat_id=group_id,
                photo=photos[0],
                caption=caption,
                parse_mode="HTML"
            )
        else:
            await bot.send_message(
                chat_id=group_id,
                text=caption,
                parse_mode="HTML"
            )
    except Exception as e:
        print("❗️ Guruhga yuborishda xatolik:", e)

    await state.clear()
