from handlers.messages import save_msg, update_msg, delete_msg, clean_msg
from bot.session import bot, scheduler
from pyrogram.handlers import MessageHandler, EditedMessageHandler, DeletedMessagesHandler
from pyrogram import filters


def register_handlers():
    # group messages
    bot.add_handler(MessageHandler(save_msg, filters.group))
    bot.add_handler(EditedMessageHandler(update_msg, filters.group))
    bot.add_handler(DeletedMessagesHandler(delete_msg))


def register_jobs():
    scheduler.add_job(clean_msg, 'cron', minute=0)
