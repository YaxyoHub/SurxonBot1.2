from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from loader import bot
from data.config import GROUP
from database.sql import get_admins, get_admin

ADMINS = get_admins()

from states.states import ContactForm
from buttons.reply import phone_button
from buttons.inline import flower_button, cancel_button

boglanish_router = Router()

@boglanish_router.callback_query(F.data == "cancel")
async def boglanish(message: CallbackQuery):
    await message.message.delete()
    await message.message.answer("Bekor qilindi", reply_markup=flower_button)

@boglanish_router.callback_query(F.data == "connect_us")
async def call_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()

    admins = get_admin()
    if not admins:
        return await callback.message.answer("⚠️ Admin topilmadi.", reply_markup=cancel_button)

    admin_texts = []
    for i, admin in enumerate(admins, start=1):
        name = admin[1]
        # phone = admin[2]
        username = admin[3]
        phone = admin[4]
        username_display = f"{username}" if username else "yo‘q"

        admin_texts.append(
            f"<b>👤 Admin {i}</b>\n"
            f"▪️ Ismi: {name}\n"
            f"▪️ Telefon: {phone}\n"
            f"▪️ Telegram: {username_display}\n"
        )

    full_text = "Adminlar bilan bog‘lanish:\n\n" + "\n".join(admin_texts)
    full_text += "\nAgar hohlasangiz ismingizni kiriting:"

    await callback.message.answer(full_text, parse_mode="HTML", reply_markup=cancel_button)
    await state.set_state(ContactForm.name)


@boglanish_router.message(ContactForm.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Telefon raqamingizni kiriting (masalan: +998901234567):", reply_markup=phone_button)
    await state.set_state(ContactForm.phone)


@boglanish_router.message(ContactForm.phone, F.contact)
async def get_phone_contact(message: Message, state: FSMContext):
    phone = message.contact.phone_number
    if not phone.startswith("+"):
        phone = f"+{phone}"

    await state.update_data(phone=phone)
    data = await state.get_data()
    await message.answer("✅ So'rovingiz yuborildi", reply_markup=flower_button)
    msg = (
        f"📥 Yangi bog'lanish so'rovi:\n\n"
        f"👤 Ismi: {data['name']}\n"
        f"📞 Telefon: {data['phone']}\n"
        f"🇺🇿 Telegram: @{message.from_user.username or 'yo‘q'}\n"
        f"🆔 Telegram ID: {message.from_user.id}"
    )

    await bot.send_message(chat_id=GROUP, text=msg)


@boglanish_router.message(ContactForm.phone)
async def get_phone_text(message: Message, state: FSMContext):
    text = message.text.strip()

    if len(text) == 13 and text.startswith('+998') and text[1:].isdigit():
        await state.update_data(phone=text)
        data = await state.get_data()
        await message.answer("✅ So'rovingiz yuborildi", reply_markup=flower_button)

        msg = (
            f"📥 Yangi bog'lanish so'rovi:\n\n"
            f"👤 Ismi: {data['name']}\n"
            f"📞 Telefon: {data['phone']}\n"
            f"🇺🇿 Telegram: @{message.from_user.username or 'None'}\n"
            f"🆔 Telegram ID: {message.from_user.id}"
        )

        await bot.send_message(chat_id=GROUP, text=msg)
        

    else:
        await message.answer("❌ Telefon raqami noto‘g‘ri formatda. Qayta kiriting (masalan: +998901234567):")
