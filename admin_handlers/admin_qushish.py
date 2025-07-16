from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from states.states import Admin, DELETEadmin
from database.sql import add_admin_sql, delete_admin_sql, check_admin, get_admin
from data.needfull_funcs import IsAdmin
from admin_handlers.admin_keyboards import admin_menu

add_admin_router = Router()

admin_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="➕ Admin qo'shish", callback_data="admin_add"),
            InlineKeyboardButton(text="➖ Admin o'chirish", callback_data="admin_del")
        ],
        [
            InlineKeyboardButton(text="📝 Adminlar ro'yxati", callback_data="admin_list")
        ],
        [InlineKeyboardButton(text='🔙 Orqaga', callback_data='back')]
    ]
)

back_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='🔙 Ortga', callback_data='back_admin')]
    ]
)

@add_admin_router.message(Command("add_admin"), IsAdmin())
async def adminsss(message: Message):
    await message.reply("Admin qo'shish yoki o'chirish", reply_markup=admin_button)

@add_admin_router.callback_query(F.data == "admin_add")
async def add_adminssss(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Admin ismini kiriting:")
    await state.set_state(Admin.admin_name)

@add_admin_router.message(Admin.admin_name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(admin_name=message.text)
    await message.answer("Admin username ni yuboring:")
    await state.set_state(Admin.admin_username)


@add_admin_router.message(Admin.admin_username)
async def get_username(message: Message, state: FSMContext):
    await state.update_data(admin_username=message.text)
    await message.answer("Endi admin ID sini kiriting:")
    await state.set_state(Admin.admin_id)

@add_admin_router.message(Admin.admin_id)
async def get_id(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("⚠️ Admin ID uchun raqam kiriting")
    else:
        admin_idd = int(message.text)
        await state.update_data(admin_id=admin_idd)
        data = await state.get_data()
        add_admin_sql(data['admin_name'], data['admin_id'], data['admin_username'])
        await message.answer("Admin qo'shildi ✅", reply_markup=admin_button)
        await state.clear()


@add_admin_router.callback_query(F.data == "admin_del")
async def del_adminssss(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Admin ID sini kiriting:")
    await state.set_state(DELETEadmin.admin_id)
    
@add_admin_router.message(DELETEadmin.admin_id)
async def delete_adminssss(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("⚠️ Admin ID uchun raqam kiriting")
        return
    admin_id = int(message.text)
    result = check_admin(admin_id)
    if not result:
        await message.answer("Bunday IDli admin yo'q", reply_markup=admin_button)
    else:
        delete_admin_sql(admin_id)
        await message.answer("Admin o'chirildi ✅", reply_markup=admin_button)
    await state.clear()

@add_admin_router.callback_query(F.data == "admin_list")
async def show_admin_list(callback: CallbackQuery):
    admins = get_admin()
    text = "👥 <b>Adminlar ro'yxati:</b>\n\n"
    for index, admin in enumerate(admins, start=1):
        name = admin[1]
        admin_id = admin[2]
        admin_username = admin[3]
        text += f"{index}. <b>{name}</b> --- {admin_username} — <code>{admin_id}</code>\n"

    try:
        await callback.message.delete()
    except Exception as e:
        print("❌ Xabarni o‘chirishda xatolik:", e)

    await callback.message.answer(text, parse_mode="HTML", reply_markup=back_button)



@add_admin_router.callback_query(F.data == "back")
async def back_menu(callback: CallbackQuery):
    print("↩️ back (admin_menu) handler ishga tushdi")
    try:
        await callback.message.delete()
    except:
        print("Back menu xatosi")
    await callback.message.answer("🔧 Admin panelga qaytdingiz", reply_markup=admin_menu)

@add_admin_router.callback_query(F.data == "back_admin")
async def back_menu_admin(callback: CallbackQuery):
    print("↩️ back_admin (admin_button) handler ishga tushdi")
    try:
        await callback.message.delete()
    except Exception as e:
        print("❌ back_admin delete xatosi:", e)
    await callback.message.answer("Admin qo'shish yoki o'chirish", reply_markup=admin_button)


