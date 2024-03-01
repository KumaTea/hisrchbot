from pyrogram import Client
from typing import Optional
from common.info import self_id
from pyrogram.types import Message
from common.data import enter_group_zh


# @ensure_auth
async def enter_group(client: Client, message: Message) -> Optional[Message]:
    if message.new_chat_members:
        for member in message.new_chat_members:
            if member.id == self_id:
                return await message.reply_text(enter_group_zh, quote=False)
