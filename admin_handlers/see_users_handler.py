from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from admin_handlers.admin_keyboards import admin_menu
from database.sql import get_user
from data.needfull_funcs import IsAdmin

users_router = Router()


@users_router.callback_query(F.data == "see_users", IsAdmin())
async def show_users(callback: CallbackQuery):
    await callback.message.delete()
    users = get_user()
    if not users:
        return await callback.message.answer("⛔️ Hech qanday foydalanuvchi topilmadi.")

    text = f"👥 <b>Umumiy {len(users)} ta foydalanuvchi bor</b>"
    
    await callback.message.answer(text, reply_markup=admin_menu, parse_mode="HTML")

