
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

from config import BANNED_USERS
from AlinaMusic import app
from AlinaMusic.core.call import Alina
from AlinaMusic.utils.database import is_music_playing, music_on
from AlinaMusic.utils.decorators import AdminRightsCheck



@app.on_message(
    filters.command(
        ["resume", "cresume", "د", "دەستپێکردنەوە"],
        prefixes=["/", "!", "%", "", "@", "#"],
    )
    & ~filters.private
    & ~BANNED_USERS
)
@AdminRightsCheck
async def resume_com(cli, message: Message, _, chat_id):
    if not len(message.command) == 1:
        return await message.reply_text(_["general_2"])
    if await is_music_playing(chat_id):
        return await message.reply_text(_["admin_3"])
    await music_on(chat_id)
    await Yukki.resume_stream(chat_id)
    buttons_resume = [
        [
            InlineKeyboardButton(
                text="‣‣I 𝖲𝗄𝗂𝗉", callback_data=f"ADMIN Skip|{chat_id}"
            ),
            InlineKeyboardButton(text="▢ 𝖲𝗍𝗈𝗉", callback_data=f"ADMIN Stop|{chat_id}"),
        ],
        [
            InlineKeyboardButton(
                text="II 𝖯𝖺𝗎𝗌𝖾",
                callback_data=f"ADMIN Pause|{chat_id}",
            ),
        ],
    ]
    await message.reply_text(
        _["admin_4"].format(message.from_user.mention),
        reply_markup=InlineKeyboardMarkup(buttons_resume),
    )
