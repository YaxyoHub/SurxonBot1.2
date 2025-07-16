import time
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramForbiddenError

from admin_handlers.admin_keyboards import admin_menu
from data.needfull_funcs import IsAdmin
from data.config import CHANNELS, ADMINS
from states.states import AdsState
from database.sql import get_user
from loader import bot

reklama_router = Router()

# 📢 Admin reklamani boshlaydi
@reklama_router.callback_query(F.data == "send_ads", IsAdmin())
async def reklama_cmd(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AdsState.add)
    await callback.message.answer("📢 Marhamat, reklamani botga yuborishingiz mumkin.")
    await callback.message.answer()

# 📩 Reklama yuboriladi (copy_message orqali)
import asyncio

@reklama_router.message(AdsState.add, IsAdmin())
async def reklama_yuborish(msg: Message, state: FSMContext):
    from_chat_id = msg.chat.id
    message_id = msg.message_id
    users = get_user()

    sent = 0
    blocked = 0

    # 🟡 Kanalga yuborish (ixtiyoriy)
    try:
        await bot.copy_message(
            chat_id=CHANNELS,
            from_chat_id=from_chat_id,
            message_id=message_id
        )
    except Exception as e:
        error_text = f"❌ <b>Kanalga yuborishda xatolik:</b>\n<code>{e}</code>"
        for admin_id in ADMINS:
            try:
                await bot.send_message(admin_id, error_text, parse_mode="HTML", reply_markup=admin_menu)
            except:
                pass

    # 👥 Foydalanuvchilarga yuborish
    for user in users:
        try:
            user_id = user["user_id"]  # DictCursor bo‘lsa
            await bot.copy_message(
                chat_id=user_id,
                from_chat_id=from_chat_id,
                message_id=message_id
            )
            sent += 1
        except TelegramForbiddenError:
            blocked += 1
        except Exception as e:
            print(f"Xatolik foydalanuvchi {user}: {e}")
        await asyncio.sleep(0.01)  # to‘g‘ri usul

    await msg.answer(
        f"✅ Reklama yuborish yakunlandi.\n"
        f"📤 Yuborildi: {sent} ta foydalanuvchiga\n"
        f"⛔️ Bloklaganlar: {blocked} ta", 
        reply_markup=admin_menu
    )
    await state.clear()
