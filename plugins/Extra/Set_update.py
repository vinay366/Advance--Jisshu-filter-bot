from pyrogram import Client, filters , enums
from info import ADMINS
import re
from database.users_chats_db import db


@Client.on_message(filters.command("set_muc") & filters.user(ADMINS))
async def set_muc_id(client: Client, message: Message):
    try:
        if len(message.command) < 2:
            await message.reply("Please provide A Channel ID To Set The Movies Update Channel.\n\n**Usage:** `/set_muc -1001234567890`")
            return
        id = message.command[1]
        if not id.startswith('-100') or len(id) != 14:
            await message.reply("Invalid Channel ID. Please Make Sure It Starts With '-100'.")
            return
        is_suc = await db.movies_update_channel_id(id)
        if is_suc:
            await message.reply("Successfully Set Movies Update Channel ID: " + id)
        else:
            await message.reply("Failed To Set Movies Update Channel ID: " + id)
    except Exception as e:
        print('Err in set_muc_id', e)
        await message.reply("Failed to set movies channel ID! Because : " + str(e))
        
