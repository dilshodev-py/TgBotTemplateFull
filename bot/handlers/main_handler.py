from aiogram import html, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from db.models import User

main_router = Router()


@main_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    user = await User.exists_user(id_=message.from_user.id)
    if not user:
        await User.create(id=message.from_user.id, username=message.from_user.username)
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")
