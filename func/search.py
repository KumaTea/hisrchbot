from pyrogram import Client
from typing import Optional
from pyrogram.types import Chat
from bot.auth import ensure_auth
from bot.store import time_store
from func.tools import get_content
from pyrogram.types import Message
from search.core import search_core
from common.data import MAX_RESULT_LEN
from search.clean import is_remedial_trigger


def get_message_link(chat: Chat, msg_id: int) -> str:
    if chat.username:
        msg_link = f'https://t.me/{chat.username}/{msg_id}'
    else:
        link_chat_id = str(chat.id)[4:]
        msg_link = f'https://t.me/c/{link_chat_id}/{msg_id}'
    return msg_link


def format_result(term: str, result: str, msg_link: str):
    result = result.replace('\n', ' ')

    index = result.find(term)
    if index == -1:
        if len(result) > MAX_RESULT_LEN:
            return f'[{result[:MAX_RESULT_LEN-1]}…]({msg_link})'
        return f'[{result}]({msg_link})'

    original_len = len(result)
    if original_len > MAX_RESULT_LEN:
        padding_len = max(0, (MAX_RESULT_LEN - len(term)) // 2 - 1)
        start_index = max(0, index - padding_len)
        end_index = min(original_len, index + len(term) + padding_len)
        result = f'{result[start_index:end_index]}'
        if start_index:
            result = f'…{result}'
        if end_index < original_len:
            result = f'{result}…'
    return result.replace(
        term,
        f'**[{term}]({msg_link})**',
        1
    )


async def search(message: Message, exact: bool = True) -> Optional[Message]:
    search_term = get_content(message)
    if not search_term:
        return await message.reply_text('未输入搜索词 😡')

    chat_id = message.chat.id
    search_result = search_core(chat_id, search_term, exact_search=exact)

    if not search_result.success:
        failed_reason = search_result.failed_reason or '未知错误'
        return await message.reply_text('搜索失败 😭\n' + failed_reason, disable_web_page_preview=True)

    results = search_result.results
    if not results:
        return await message.reply_text('未找到相关结果 🥺')

    formatted_results = [
        format_result(search_term, result['text'], get_message_link(message.chat, result['id']))
        for result in results
    ]

    text = '搜索结果 🤩\n\n'
    i = 1
    for result in formatted_results:
        text += f'{i}. {result}\n'
        i += 1

    if not is_remedial_trigger(chat_id):
        time_store.trigger(chat_id)
    return await message.reply_text(text, disable_web_page_preview=True)


@ensure_auth
async def command_search(client: Client, message: Message) -> Optional[Message]:
    return await search(message)


@ensure_auth
async def command_fuzzy(client: Client, message: Message) -> Optional[Message]:
    return await search(message, exact=False)
