import logging
from bot.session import bot
from bot.session import meili
from datetime import datetime
from share.local import trusted_group
from common.data import STALE_CHAT_TIME
from bot.store import text_store, time_store


def clean_chat(chat_id: int) -> None:
    text_store.clear_chat(chat_id)
    time_store.delete(chat_id)
    meili.delete_index(chat_id)
    logging.warning(f'Clean chat {chat_id}')


async def clean_stale() -> None:
    chat_ids_a = text_store.msgs.keys()
    chat_ids_b = time_store.data.keys()
    if set(chat_ids_a) != set(chat_ids_b):
        logging.error('text_store is not sync with time_store!')
        diff_a = set(chat_ids_a) - set(chat_ids_b)
        diff_b = set(chat_ids_b) - set(chat_ids_a)
        logging.error(f'{diff_a=}, {diff_b=}')

    for chat_id in chat_ids_a:
        if chat_id in trusted_group:
            continue
        chat_time = time_store.query(chat_id)
        last_msg_time = chat_time.last_msg_time
        if last_msg_time:
            if (datetime.now() - last_msg_time).total_seconds() < STALE_CHAT_TIME:
                continue
        await bot.leave_chat(chat_id)
        clean_chat(chat_id)

    for chat_id in chat_ids_a:
        if chat_id in trusted_group:
            continue
        chat_time = time_store.query(chat_id)
        last_trigger_time = chat_time.last_trigger_time
        trigger_informed = chat_time.trigger_informed
        if trigger_informed:
            if (datetime.now() - last_trigger_time).total_seconds() > STALE_CHAT_TIME:
                await bot.send_message(chat_id, '本 bot 已至少一个月未被使用，即将离开本群，再见。')
                await bot.leave_chat(chat_id)
                clean_chat(chat_id)
        else:
            if (datetime.now() - last_trigger_time).total_seconds() > STALE_CHAT_TIME // 2:
                # chat_time.trigger_informed = True
                # don't know if this works
                time_store.data[chat_id].trigger_informed = True
                await bot.send_message(chat_id, '本 bot 已至少半个月未被使用，为减轻服务器压力，即将离开本群。')


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
