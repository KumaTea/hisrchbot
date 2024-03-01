import asyncio
import logging
from bot.session import meili
from datetime import datetime
from search.tools import until_succeeded
from bot.store import text_store, time_store
from common.data import INDEX_INTERVAL, STALE_CHAT_TIME


def clean_stale() -> None:
    chat_ids_a = text_store.msgs.keys()
    chat_ids_b = time_store.data.keys()
    if set(chat_ids_a) != set(chat_ids_b):
        logging.error('text_store is not sync with time_store!')
        diff_a = set(chat_ids_a) - set(chat_ids_b)
        diff_b = set(chat_ids_b) - set(chat_ids_a)
        logging.error(f'{diff_a=}, {diff_b=}')

    for chat_id in chat_ids_a:
        chat_time = time_store.query(chat_id)
        last_msg_time = chat_time.last_msg_time
        if last_msg_time:
            if (datetime.now() - last_msg_time).seconds < STALE_CHAT_TIME:
                continue
        text_store.clear_chat(chat_id)
        time_store.delete(chat_id)
        meili.delete_index(chat_id)
        logging.warning(f'Clean stale chat {chat_id}')


def need_update(chat_id: int) -> bool:
    chat_time = time_store.query(chat_id)
    last_msg_time = chat_time.last_msg_time
    if not last_msg_time:
        return False
    last_index_time = chat_time.last_index_time
    if not last_index_time:
        return True
    if (datetime.now() - last_index_time).seconds < INDEX_INTERVAL:
        return False
    if last_msg_time > last_index_time:
        return True
    return False


async def update_chat_index(chat_id: int) -> None:
    chat_msgs_json = text_store.chat_to_json(chat_id)
    if not chat_msgs_json:
        return None
    index = meili.index(chat_id)
    del_task = index.delete_all_documents()
    await until_succeeded(del_task)

    add_task = index.add_documents(chat_msgs_json)
    await until_succeeded(add_task)

    time_store.update_index_time(chat_id, datetime.now())
    logging.info(f'Updated index for chat {chat_id}')


async def update_indexes(rescue: bool = False) -> None:
    text_store.clean_all()

    chat_ids = text_store.msgs.keys()
    tasks = []
    for chat_id in chat_ids:
        if need_update(chat_id) or rescue:
            tasks.append(update_chat_index(chat_id))
    if tasks:
        await asyncio.gather(*tasks)

    time_store.save()
    text_store.save()
