from pyrogram import Client
from bot.auth import ensure_auth
from bot.session import text_store
from pyrogram.types import Message
from common.info import self_id


def is_valid_msg(message: Message) -> bool:
    if message.from_user:
        user_id = message.from_user.id
        if user_id == self_id:
            return False

    text = message.text or message.caption
    if text and not text.startswith('/'):
        return True
    return False


def clean_msg() -> None:
    text_store.clean_all()


@ensure_auth
async def save_msg(client: Client, message: Message) -> None:
    if is_valid_msg(message):
        text = message.text or message.caption
        text_store.raw_add_msg(message.chat.id, message.id, text)


@ensure_auth
async def update_msg(client: Client, message: Message) -> None:
    if is_valid_msg(message):
        text = message.text or message.caption
        text_store.raw_add_msg(message.chat.id, message.id, text)
    else:
        text_store.delete_msg(message)


@ensure_auth
async def delete_msg(client: Client, message: Message) -> None:
    return text_store.delete_msg(message)
