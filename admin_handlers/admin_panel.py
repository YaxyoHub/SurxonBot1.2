from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command

from data.needfull_funcs import IsAdmin
from admin_handlers.admin_keyboards import admin_menu

from admin_handlers.reklama_handler import reklama_router
from admin_handlers.see_users_handler import users_router
from admin_handlers.add_flower_handler import add_flower_router
from admin_handlers.del_flower_handler import del_flower_router
# from admin_handlers.see_flower_handler import see_flower_router

admin_router = Router()

@admin_router.message(Command("admin"), IsAdmin())
async def admin_panel(msg: Message):
    await msg.answer("Salom Admin\n\n"
                     f"/admin - admin panelga o'tish uchun\n"
                     f"/add_admin - botga admin qo'shish va o'chirish uchun", reply_markup=admin_menu)

@admin_router.callback_query(F.data == "accept_yes", IsAdmin())
async def accept_yesss(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Qabul qilindi ✅")



admin_router.include_router(reklama_router)
admin_router.include_router(users_router)
admin_router.include_router(add_flower_router)
admin_router.include_router(del_flower_router)