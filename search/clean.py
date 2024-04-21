import logging
from bot.session import bot
from bot.session import meili
from datetime import datetime
from share.local import trusted_group
from common.data import STALE_CHAT_TIME
from bot.store import text_store, time_store
from pyrogram.errors.exceptions.bad_request_400 import ChannelInvalid


def clean_chat(chat_id: int) -> None:
    text_store.clear_chat(chat_id)
    time_store.delete(chat_id)
    meili.delete_index(chat_id)
    logging.warning(f'[search.clean]\tClean chat {chat_id}')


async def safe_clean(chat_id: int, leave: bool = True, inform_msg: str = '') -> bool:
    is_invalid = False
    try:
        if inform_msg:
            await bot.send_message(chat_id, inform_msg)
        if leave:
            await bot.leave_chat(chat_id)
    except ChannelInvalid:
        is_invalid = True
        logging.warning(f'[search.clean]\tChannelInvalid {chat_id}')
    return is_invalid


async def clean_stale() -> None:
    chat_ids_a = text_store.msgs.keys()
    chat_ids_b = time_store.data.keys()
    if set(chat_ids_a) != set(chat_ids_b):
        logging.error('[search.clean]\ttext_store is not sync with time_store!')
        diff_a = set(chat_ids_a) - set(chat_ids_b)
        diff_b = set(chat_ids_b) - set(chat_ids_a)
        logging.error(f'{diff_a=}, {diff_b=}')

    # check stale chats by message time
    for chat_id in list(chat_ids_a):
        if chat_id in trusted_group:
            continue
        chat_time = time_store.query(chat_id)
        last_msg_time = chat_time.last_msg_time
        if last_msg_time:
            if (datetime.now() - last_msg_time).total_seconds() < STALE_CHAT_TIME:
                continue
        await safe_clean(chat_id, leave=True)
        clean_chat(chat_id)

    # check stale chats by trigger time
    for chat_id in list(chat_ids_a):
        if chat_id in trusted_group:
            continue
        chat_time = time_store.query(chat_id)
        last_trigger_time = chat_time.last_trigger_time
        trigger_informed = chat_time.trigger_informed
        if trigger_informed:
            if (datetime.now() - last_trigger_time).total_seconds() > STALE_CHAT_TIME:
                await safe_clean(chat_id, leave=True, inform_msg='本 bot 已至少一个月未被使用，因此离开本群，再见。')
                clean_chat(chat_id)
        else:
            if (datetime.now() - last_trigger_time).total_seconds() > STALE_CHAT_TIME // 2:
                # chat_time.trigger_informed = True
                # don't know if this works
                time_store.data[chat_id].trigger_informed = True
                time_store.save()
                chat_is_invalid = await safe_clean(chat_id, leave=False, inform_msg='本 bot 已至少半个月未被使用，为减轻服务器压力，即将离开本群。')
                if chat_is_invalid:
                    clean_chat(chat_id)
                logging.warning(f'[search.clean]\tInform chat {chat_id}')


def is_remedial_trigger(chat_id: int) -> bool:
    if chat_id not in time_store.data:
        return False
    # chat_time = time_store.query(chat_id)
    chat_time = time_store.data[chat_id]
    trigger_informed = chat_time.trigger_informed
    if not trigger_informed:
        return False
    last_trigger_time = chat_time.last_trigger_time
    if STALE_CHAT_TIME // 2 < (datetime.now() - last_trigger_time).total_seconds() < STALE_CHAT_TIME // 2 + 60 * 60 * 24:
        return True
    return False
