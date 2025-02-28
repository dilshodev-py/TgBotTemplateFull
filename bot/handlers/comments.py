from aiogram import Router, F, Bot
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.models import Group

controller = Router()

GROUP_CHAT_ID = 0
restricted_users = set()


async def check_subscription(user_id, bot):
    required_chats = await Group.get_group_ids()
    for chat_id in required_chats:
        try:
            member = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
            if member.status in ['left', 'kicked']:
                return False
        except Exception as e:
            print(e)
            return False
    return True


@controller.message(F.chat.type.in_({"group", "supergroup"}), F.chat.id == GROUP_CHAT_ID)
async def controller_group(message: Message, bot: Bot):
    user_id = message.from_user.id

    if user_id in restricted_users or not await check_subscription(user_id=user_id, bot=bot):
        await message.delete()
        restricted_users.add(user_id)

        keyboard = InlineKeyboardBuilder()
        keyboard.add(
            InlineKeyboardButton(text="Botga o'tish", url=f"t.me/{(await bot.get_me()).username}"),
            InlineKeyboardButton(text="Tekshirish", callback_data="check_subscription")
        )
        keyboard.adjust(1, 1)

        await bot.send_message(
            chat_id=message.chat.id,
            text=f"{message.from_user.mention}, siz guruhda yozish uchun botga o'tib kanallarga a'zo bo'lishingiz kerak!\n"
                 "\nA'zo bo'lib, tekshirish tugmasini bosing!",
            reply_markup=keyboard.as_markup()
        )


@controller.callback_query(F.data == "check_subscription")
async def check_subscription_callback(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    if await check_subscription(user_id=user_id, bot=bot):
        restricted_users.discard(user_id)
        await callback.message.edit_text(
            text=f"✅ Tabriklaymiz! Endi guruhda yozishingiz mumkin. {callback.from_user.mention}",
            reply_markup=None
        )
    else:
        await callback.answer(
            text="Siz hali barcha kerakli kanallarga a'zo bo'lmadingiz!",
            show_alert=True
        )
