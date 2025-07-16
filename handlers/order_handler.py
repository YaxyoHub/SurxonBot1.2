from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InputMediaPhoto, Location
from aiogram.fsm.context import FSMContext

from database.sql import get_flower
from states.states import OrderState
from data.config import ADMINS, GROUP
from buttons.inline import accept_btn, flower_button
from buttons.reply import phone_button, location_button
from loader import bot

order_router = Router()

# 🌸 Buyurtma tugmasi bosilganda
@order_router.callback_query(F.data.startswith("order:"))
async def start_order(callback: CallbackQuery, state: FSMContext):
    _, flower_id = callback.data.split(":")
    flower, _ = get_flower(flower_id)

    await state.update_data(flower_id=flower_id)
    await callback.message.answer(
        text=(
            f"🛒 Siz <b>{flower['name']}</b> uchun buyurtma bermoqchisiz.\n"
            f"Iltimos, to‘liq ismingizni yozing:"
        ),
        parse_mode="HTML"
    )
    await state.set_state(OrderState.waiting_for_name)


# 🧑 Ism yozgandan keyin
@order_router.message(OrderState.waiting_for_name)
async def get_name(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer("📞 Endi telefon raqamingizni yuboring:", reply_markup=phone_button)
    await state.set_state(OrderState.waiting_for_phone)


# 📱 Telefon yozgandan keyin
@order_router.message(OrderState.waiting_for_phone)
async def get_phone(msg: Message, state: FSMContext):
    if msg.contact:
        phone = msg.contact.phone_number
    else:
        phone = msg.text

    await state.update_data(phone=phone)
    await msg.answer("📍 Endi lokatsiyangizni yuboring:", reply_markup=location_button)
    await state.set_state(OrderState.lat)


# 📍 Lokatsiya qabul qilish
@order_router.message(OrderState.lat, F.location)
async def get_location(msg: Message, state: FSMContext):
    latitude = msg.location.latitude
    longitude = msg.location.longitude

    await state.update_data(lat=latitude, lon=longitude)
    await msg.answer("✅ Buyurtmangiz qabul qilindi! Tez orada siz bilan bog‘lanamiz.", reply_markup=flower_button)
    data = await state.get_data()

    flower, photos = get_flower(data["flower_id"])

    caption = (
        f"📥 <b>Yangi buyurtma!</b>\n\n"
        f"💐 Gul: <b>{flower['name']}</b>\n"
        f"💰 Narxi: {flower['price']}\n\n"
        f"👤 Ism: <b>{data['name']}</b>\n"
        f"🇺🇿 Telegram: @{msg.from_user.username}\n"
        f"📞 Telefon: <b>{data['phone']}</b>\n"
        f"📍 Lokatsiya: <a href='https://maps.google.com/?q={latitude},{longitude}'>Xaritada ko‘rish</a>\n"
        f"🆔 ID: <code>{msg.from_user.id}</code>"
    )

    if photos:
        # Faqat 1 dona rasmni yuboramiz, caption bilan
        try:
            await bot.send_photo(
                chat_id=GROUP,
                photo=photos[0],
                caption=caption,
                parse_mode="HTML",
                reply_markup=accept_btn
            )
        except Exception as e:
            print("❗️Rasm yuborishda xatolik:", e)
            await bot.send_message(
                chat_id=GROUP,
                text=caption,
                parse_mode="HTML",
                reply_markup=accept_btn
            )
    else:
        await bot.send_message(
            chat_id=GROUP,
            text=caption,
            parse_mode="HTML",
            reply_markup=accept_btn
        )

    await state.clear()
