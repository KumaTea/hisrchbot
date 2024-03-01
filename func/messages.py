from bot.store import text_store
from pyrogram.types import Message
from common.local import trusted_group
from common.data import MAX_MSG_LEN, TRUSTED_GROUP_MSG_LIMIT
from pyrogram.enums.message_entity_type import MessageEntityType


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
    if text.startswith('/'):
        return False
    entities = message.entities or message.caption_entities
    if entities:
        for entity in entities:
            # if entity.type in [MessageEntityType.PRE]:
            if entity.type == MessageEntityType.PRE:
                return False
    return True


def clean_msg() -> None:
    text_store.clean_all()
