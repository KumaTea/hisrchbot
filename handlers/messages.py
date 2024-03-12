from pyrogram import Client
from datetime import datetime
from bot.auth import ensure_auth
from pyrogram.types import Message
from bot.store import text_store, time_store
from func.messages import is_valid_msg, add_msg_web_preview


async def add_msg(message: Message) -> None:
    text = message.text or message.caption
    web_preview = await add_msg_web_preview(message)
    if web_preview:
        text += f'\n{web_preview}'
    text_store.raw_add_msg(message.chat.id, message.id, text)


@ensure_auth
async def save_msg(client: Client, message: Message) -> None:
    if is_valid_msg(message):
        await add_msg(message)
        time_store.update_msg_time(message.chat.id, message.date or datetime.now())


@ensure_auth
async def update_msg(client: Client, message: Message) -> None:
    if is_valid_msg(message):
        await add_msg(message)
    else:
        text_store.delete_msg(message)


@ensure_auth
async def delete_msgs(client: Client, messages: list[Message]) -> None:
    for message in messages:
        text_store.delete_msg(message)
