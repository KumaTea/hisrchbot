import logging
import meilisearch
import configparser
from pyrogram import Client
from bot.store import TextMsgStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

config = configparser.ConfigParser()
config.read('config.ini')
bot = Client(
    'bot',
    api_id=config['bot']['api_id'],
    api_hash=config['bot']['api_hash'],
    bot_token=config['bot']['bot_token'],
)

meili = meilisearch.Client(
    config['meili']['url'],
    config['meili']['api_key']
)

scheduler = AsyncIOScheduler()
text_store = TextMsgStore()
