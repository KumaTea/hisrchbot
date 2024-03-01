from pyrogram import Client
from datetime import datetime
from bot.auth import ensure_auth
from pyrogram.types import Message
from func.messages import is_valid_msg
from bot.store import text_store, time_store


@ensure_auth
async def save_msg(client: Client, message: Message) -> None:
    if is_valid_msg(message):
        text = message.text or message.caption
        text_store.raw_add_msg(message.chat.id, message.id, text)
        time_store.update_msg_time(message.chat.id, message.date or datetime.now())


@ensure_auth
async def update_msg(client: Client, message: Message) -> None:
    if is_valid_msg(message):
        text = message.text or message.caption
        text_store.raw_add_msg(message.chat.id, message.id, text)
    else:
        text_store.delete_msg(message)


@ensure_auth
async def delete_msgs(client: Client, messages: list[Message]) -> None:
    for message in messages:
        return text_store.delete_msg(message)
