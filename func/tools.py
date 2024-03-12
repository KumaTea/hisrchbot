import logging
import aiohttp
from typing import Optional
from bs4 import BeautifulSoup
from pyrogram.types import Message


def get_content(message: Message) -> Optional[str]:
    text = message.text
    content_index = text.find(' ')
    # reply = message.reply_to_message
    if content_index == -1:
        # no text
        # if not reply:
        return None
    return text[content_index + 1:]


async def aget_html(url: str) -> Optional[str]:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                return await response.text()
        except aiohttp.ClientError as e:
            logging.error(str(e))
            return None


def get_meta_content(html: str, prop: str) -> Optional[str]:
    # property_index = html.find(f'property="{prop}"')
    # if property_index == -1:
    #     return None
    # content_index = html.find('content=', property_index)
    # if content_index == -1:
    #     return None
    # content_start = html.find('"', content_index)
    # content_end = html.find('"', content_start + 1)
    # return html[content_start + 1:content_end]

    # meta = re.findall(f'<meta property="{prop}" content="(.*?)"', html)
    # if meta:
    #     return meta[0]

    soup = BeautifulSoup(html, 'html.parser')
    meta = soup.find('meta', property=prop)
    if meta:
        return meta['content']
    return None


def get_html_title_desc(html: str) -> str:
    result = ''
    title = get_meta_content(html, 'og:title')
    if title:
        result += title + '\n'
    description = get_meta_content(html, 'og:description')
    if description:
        result += description

    return result
