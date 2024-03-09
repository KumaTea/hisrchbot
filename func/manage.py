from typing import Optional
from pyrogram import Client
from bot.store import text_store
from pyrogram.types import Message
from common.info import administrators


async def command_unindex(client: Client, message: Message) -> Optional[Message]:
    reply = message.reply_to_message
    if not reply:
        return await message.reply_text('请回复需要取消索引的消息')

    user_id = message.from_user.id
    replied_user_id = reply.from_user.id
    if user_id != replied_user_id and user_id not in administrators:
        return await message.reply_text('权限不足')

    # chat_id = message.chat.id
    # msg_id = reply.id
    result = text_store.delete_msg(reply)
    if result:
        return await message.reply_text('已取消上述消息的索引')
    else:
        return await message.reply_text('该消息本就未被索引')
