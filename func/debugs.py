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
        chat_count = len(text_store.msgs)
        text += f'  `{chat_count=}`\n'
        # for chat_id in text_store.msgs:
        chat_id = -1001932978232
        msg_count = len(text_store.msgs[chat_id])
        last_msg = time_store.data[chat_id].last_msg_time.strftime('%m-%d %H:%M')
        last_index = time_store.data[chat_id].last_index_time.strftime('%m-%d %H:%M')
        last_trigger = time_store.data[chat_id].last_trigger_time.strftime('%m-%d %H:%M')
        text += (
            f'  `{chat_id=}`\n'
            f'  `{msg_count=}`\n'
            f'  `{last_msg=}`\n'
            f'  `{last_index=}`\n'
            f'  `{last_trigger=}`\n'
        )
        return await message.reply(text)
