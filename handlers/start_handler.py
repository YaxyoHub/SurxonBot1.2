from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from buttons.inline import flower_button, subscription_check_keyboard
from data.needfull_funcs import is_user_subscribed
from database.sql import add_user

start_router = Router()

@start_router.message(CommandStart())
async def start_cmd(msg: Message):
    add_user(msg.from_user.id, msg.from_user.full_name, msg.from_user.username or None)
    subscribed = await is_user_subscribed(msg.bot, msg.from_user.id)

    if not subscribed:
        await msg.answer(
            "👋 Botdan foydalanish uchun quyidagi kanalga obuna bo‘ling:",
            reply_markup=subscription_check_keyboard()
        )
    else:
        await msg.answer(
            f"🎉 Xush kelibsiz {msg.from_user.first_name} !",
            reply_markup=flower_button
        )

@start_router.message(Command('help'))
async def help_cmd(message: Message):
    await message.reply("Ushbu bot nima qila oladi?\n\n"
                        "/start -> bosing va asosiy menu chiqadi\n"
                        "Asosiy menudan Gullar bo'limi yoki O'yinchoqlar bo'limiga kiring\n"
                        "Va Gullar va o'yinchoqlarga buyurtma bering🤗")

# 👇 “✅ Obuna bo‘ldim” tugmasi bosilganda qayta tekshiradi
@start_router.callback_query(F.data == "check_sub")
async def check_subscription(callback: CallbackQuery):
    subscribed = await is_user_subscribed(callback.bot, callback.from_user.id)

    if not subscribed:
        await callback.answer(f"❗️Hali ham obuna bo'lmagansiz!", show_alert=True)
    else:
        await callback.message.edit_text(
            f"Salom {callback.from_user.first_name}",
            reply_markup=flower_button()
        )
