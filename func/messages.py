from typing import Optional
from bot.store import text_store
from share.tools import find_url
from pyrogram.types import Message
from share.local import trusted_group
from func.tools import aget_html, get_html_title_desc
from pyrogram.enums.message_entity_type import MessageEntityType
from common.data import MAX_MSG_LEN, valid_commands, TWITTER_USER_AGENT, TRUSTED_GROUP_MSG_LIMIT


def is_valid_msg(message: Message) -> bool:
    if message.from_user:
        # user_id = message.from_user.id
        # if user_id == self_id:
        #     return False
        if message.from_user.is_bot:
            return False

    text = message.text or message.caption
    if not text:
        return False
    limit = MAX_MSG_LEN if message.chat.id not in trusted_group else TRUSTED_GROUP_MSG_LIMIT
    if len(text) > limit:
        return False
    if text.startswith('/') and not any(text.startswith(cmd) for cmd in valid_commands):
        return False
    entities = message.entities or message.caption_entities
    if entities:
        for entity in entities:
            if entity.type in [MessageEntityType.PRE, MessageEntityType.CUSTOM_EMOJI]:
                return False
    return True


async def add_msg_web_preview(message: Message) -> Optional[str]:
    # if message.has_web_preview:
    # not implemented?
    text = message.text or message.caption
    url = find_url(text)
    if not url:
        return None

    twi_urls = ['twitter.com', 'x.com', 't.co']
    if any(twi_url in url for twi_url in twi_urls):
        html = await aget_html(url, TWITTER_USER_AGENT)
    else:
        html = await aget_html(url)

    if not html:
        return None
    title_desc = get_html_title_desc(html)
    return title_desc


def clean_msg() -> None:
    text_store.clean_all()
