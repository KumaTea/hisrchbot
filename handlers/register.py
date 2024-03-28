import logging
from pyrogram import filters
from handlers.functions import *
from search.clean import clean_stale
from bot.session import bot, scheduler
from search.index import update_indexes
from handlers.messages import process_msg, update_msg, delete_msgs
from pyrogram.handlers import MessageHandler, EditedMessageHandler, DeletedMessagesHandler


def register_handlers():
    # group commands
    bot.add_handler(MessageHandler(command_search, filters.command(['search', 's']) & filters.group))
    bot.add_handler(MessageHandler(command_fuzzy, filters.command(['fuzzy']) & filters.group))
    bot.add_handler(MessageHandler(command_unindex, filters.command(['unindex']) & filters.group))

    # group messages
    bot.add_handler(MessageHandler(process_msg, filters.group))
    bot.add_handler(EditedMessageHandler(update_msg, filters.group))
    bot.add_handler(DeletedMessagesHandler(delete_msgs, filters.group))

    # private commands
    bot.add_handler(MessageHandler(command_force_update, filters.command(['force_update']) & filters.private))
    bot.add_handler(MessageHandler(command_debug_info, filters.command(['debug_info']) & filters.private))

    logging.info("[Bot] Handlers registered.")


def register_jobs():
    # scheduler.add_job(clean_msg, 'cron', minute=0)
    # done at index time
    scheduler.add_job(update_indexes, 'cron', minute=0)
    scheduler.add_job(clean_stale, 'cron', hour=12, minute=34)
    scheduler.start()
