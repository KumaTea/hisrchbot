from pyrogram import Client
from pyrogram.types import Update


async def print_update(client: Client, update: Update, users, chats):
    return print(update)
