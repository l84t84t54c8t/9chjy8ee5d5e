#
# Copyright (C) 2024 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the MIT License.
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved.
#

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from AlinaMusic import app
from AlinaMusic.core.call import Alina
from AlinaMusic.utils.database import is_music_playing, music_off
from AlinaMusic.utils.decorators import AdminRightsCheck

from config import BANNED_USERS



@app.on_message(
    filters.command(
        ["pause", "cpause", "وسبە", "وەستانی کاتی"], prefixes=["/", "@", ".", "#", ""]
    )
    & ~filters.private
    & ~BANNED_USERS
)
@AdminRightsCheck
async def pause_admin(cli, message: Message, _, chat_id):
    if not len(message.command) == 1:
        return await message.reply_text(_["general_2"])
    if not await is_music_playing(chat_id):
        return await message.reply_text(_["admin_1"])
    await music_off(chat_id)
    await Alina.pause_stream(chat_id)
    buttons = [
        [
            InlineKeyboardButton(
                text="▷ 𝖱𝖾𝗌𝗎𝗆𝖾", callback_data=f"ADMIN Resume|{chat_id}"
            ),
            InlineKeyboardButton(
                text="𝖱𝖾𝗉𝗅𝖺𝗒 ↺", callback_data=f"ADMIN Replay|{chat_id}"
            ),
        ],
    ]
    await message.reply_text(_["admin_2"].format(message.from_user.mention),
    reply_markup=InlineKeyboardMarkup(buttons),
    )



__MODULE__ = "Pause"
__HELP__ = """
**Pause Music**

This module allows administrators to pause the music playback in the group.

Commands:
- /pause: Pause the music playback in groups.
- /cpause: Pause the music playback in channels.

Note:
- Only administrators can use these commands.
"""
