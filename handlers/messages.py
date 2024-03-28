from pyrogram import Client
from datetime import datetime
from common.info import self_id
from share.auth import ensure_auth
from pyrogram.types import Message
from func.search import reply_search
from common.data import WHAT_TO_SEARCH
from bot.store import text_store, time_store
from func.messages import is_valid_msg, add_msg_web_preview


async def add_msg(message: Message) -> None:
    text = message.text or message.caption
    web_preview = await add_msg_web_preview(message)
    if web_preview:
        text += f'\n{web_preview}'
    text_store.raw_add_msg(message.chat.id, message.id, text)


async def save_msg(client: Client, message: Message) -> None:
    if is_valid_msg(message):
        await add_msg(message)
        time_store.update_msg_time(message.chat.id, message.date or datetime.now())


@ensure_auth
async def process_msg(client: Client, message: Message) -> None:
    replied = message.reply_to_message
    if replied and replied.from_user.id == self_id and replied.text == WHAT_TO_SEARCH:
        return await reply_search(message)
    return await save_msg(client, message)


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
