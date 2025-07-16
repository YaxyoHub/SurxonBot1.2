from aiogram import Router, F
from aiogram.types import CallbackQuery

from database.sql import get_admin
from buttons.inline import back_button, flower_button

about_router = Router()

@about_router.callback_query(F.data == "about_bot")
async def about_cmd(callback: CallbackQuery):
    admins = get_admin()
    admin_text = []
    for i, admin in enumerate(admins, start=1):
        name = admin[1]
        username = admin[3]
        phone = admin[4]
        username_display = f"{username}" if username else "yo‘q"
        admin_text.append(
            f"👤 Admin {i}\n"
            f"▪️ Ismi: {name}\n"
            f"▪️ Telefon raqami: {phone}\n"
            f"▪️ Telegram: {username_display}\n"
        )
    
    # Bu umumiy matn
    full_text = (
        "🌸 <b>Surxon Gullari</b>\n\n"
        "Surxon Gullari - bot orqali siz o'zingizga yoqqan gul va "
        "o'yinchoqlarga buyurtma berishingiz mumkin.\n\n"
        "✅ Qulay va osson\n\n"
        "Botni ishlatish uchun botga /start bosing va menyuni tanlab hoziroq "
        "buyurtma berishni boshlang 🔈\n\n"
        "📍 Lokatsiya: https://maps.google.com\n"
        "📞 Biz bilan bog'lanish uchun:\n\n"
    )

    # Adminlar ro‘yxatini bitta matnga aylantiramiz
    admin_block = "\n".join(admin_text)

    # To‘liq matn
    total_text = full_text + admin_block

    await callback.message.edit_text(total_text, parse_mode="HTML", reply_markup=back_button)

@about_router.callback_query(F.data == "back_user_menu")
async def back_cmd(callack: CallbackQuery):
    await callack.message.edit_text("Asosiy menuga qaytdingiz", reply_markup=flower_button)
