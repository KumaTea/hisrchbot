from pyrogram import Client
from typing import Optional
from pyrogram.types import Message
from common.info import administrators
from search.index import update_indexes
from bot.store import text_store, time_store


# @ensure_auth
# already checked
async def command_force_update(client: Client, message: Message) -> Optional[Message]:
    if message.from_user.id in administrators:
        await update_indexes(rescue=True)
        return await message.reply('Force updated.')


async def command_debug_info(client: Client, message: Message) -> Optional[Message]:
    if message.from_user.id in administrators:
        text = 'DEBUG INFO\n'
        text += f'  `{len(text_store.msgs)=}`\n'
        # for chat_id in text_store.msgs:
        chat_id = -1001932978232
        text += (
            f'  `{chat_id=}`\n'
            f'  `{len(text_store.msgs[chat_id])=}`\n'
            f'  `{time_store.data[chat_id]=}`\n'
        )
        return await message.reply(text)
