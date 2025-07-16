from aiogram import Bot
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery, BotCommand, BotCommandScopeDefault
from data.config import CHANNELS, ADMINS
from loader import bot

async def is_user_subscribed(bot: Bot, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNELS, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception:
        return False


class IsAdmin(BaseFilter):
    async def __call__(self, obj: Message | CallbackQuery, bot: Bot) -> bool:
        return obj.from_user.id in ADMINS

async def menu_commands():
    commands = [
        BotCommand(command="start", description="Botni ishga tushirish uchun"),
        BotCommand(command='help', description="Yordam uchun")
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())