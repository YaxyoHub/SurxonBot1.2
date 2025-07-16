import asyncio
import logging
from loader import dp, bot
from data.needfull_funcs import menu_commands

from handlers.start_handler import start_router

from handlers.boglanish import boglanish_router
from handlers.bot_haqida import about_router
from handlers.error_handler import error_router

from handlers.flower_handler import flower_router
from handlers.order_handler import order_router

from handlers.toy_handler import toy_view_router
from handlers.order_toy import order_toy_router

from admin_handlers.admin_panel import admin_router
from admin_handlers.admin_qushish import add_admin_router
from admin_handlers.add_toy_handler import add_toy_router
from admin_handlers.del_toy_handler import del_toy_router


dp.include_router(start_router)

dp.include_router(admin_router)
dp.include_router(add_admin_router)
dp.include_router(add_toy_router)
dp.include_router(del_toy_router)

dp.include_router(flower_router)
dp.include_router(order_router)

dp.include_router(toy_view_router)
dp.include_router(order_toy_router)

dp.include_router(boglanish_router)
dp.include_router(about_router)


dp.include_router(error_router)

async def main():
    await menu_commands()
    await dp.start_polling(bot)

if __name__ == "__main__":
    print("✅ Bot ishga tushmoqda...")
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

