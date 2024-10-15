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
from pyrogram.errors import ChannelInvalid
from pyrogram.types import Message

from strings import command, get_command
from AlinaMusic import app
from AlinaMusic.misc import SUDOERS, db
from AlinaMusic.utils.database.memorydatabase import (
    get_active_chats,
    get_active_video_chats,
    remove_active_chat,
    remove_active_video_chat,
)

# Commands
ACTIVEVC_COMMAND = get_command("ACTIVEVC_COMMAND")
ACTIVEVIDEO_COMMAND = get_command("ACTIVEVIDEO_COMMAND")
AC_COMMAND = get_command("AC_COMMAND")


# Function for removing the Active voice and video chat also clear the db dictionary for the chat
async def _clear_(chat_id):
    db[chat_id] = []
    await remove_active_video_chat(chat_id)
    await remove_active_chat(chat_id)


@app.on_message(filters.command(ACTIVEVC_COMMAND) & SUDOERS)
async def activevc(_, message: Message):
    mystic = await message.reply_text("**- هێنانی ئەو گرووپانەی تێلیان کردۆتەوە . .**")
    served_chats = await get_active_chats()
    text = ""
    j = 0
    for x in served_chats:
        try:
            title = (await app.get_chat(x)).title
            if (await app.get_chat(x)).username:
                user = (await app.get_chat(x)).username
                text += f"<b>{j + 1}.</b>  [{title}](https://t.me/{user})[`{x}`]\n"
            else:
                text += f"<b>{j + 1}. {title}</b> [`{x}`]\n"
            j += 1
        except ChannelInvalid:
            await _clear_(x)
            continue
    if not text:
        await mystic.edit_text("**- هیچ تێلێکی ڤیدیۆی چالاک نەدۆزرایەوە**")
    else:
        await mystic.edit_text(
            f"**- تێلی دەنگی گرووپەکان :\n\n{text}**",
            disable_web_page_preview=True,
        )


@app.on_message(filters.command(ACTIVEVIDEO_COMMAND) & SUDOERS)
async def activevi_(_, message: Message):
    mystic = await message.reply_text("**- هێنانی ئەو گرووپانەی تێلیان کردۆتەوە . .**")
    served_chats = await get_active_video_chats()
    text = ""
    j = 0
    for x in served_chats:
        try:
            title = (await app.get_chat(x)).title
            if (await app.get_chat(x)).username:
                user = (await app.get_chat(x)).username
                text += f"<b>{j + 1}.</b>  [{title}](https://t.me/{user})[`{x}`]\n"
            else:
                text += f"<b>{j + 1}. {title}</b> [`{x}`]\n"
            j += 1
        except ChannelInvalid:
            await _clear_(x)
            continue
    if not text:
        await mystic.edit_text("**- هیچ تێلێکی ڤیدیۆی چالاک نەدۆزرایەوە**")
    else:
        await mystic.edit_text(
            f"**- تێلی ڤیدیۆیی گرووپەکان :\n\n{text}**",
            disable_web_page_preview=True,
        )


@app.on_message(filters.command(["/ac", "/av", "چالاکی پەخش"], "") & SUDOERS)
async def vc(client, message: Message):
    ac_audio = str(len(await get_active_chats()))
    ac_video = str(len(await get_active_video_chats()))
    await message.reply_text(
        f"<b>✫ زانیاری چالاکی پەخشکردن :</b>\n\n<b>دەنگی : {ac_audio}\nڤیدیۆ : {ac_video}</b>"
    )


__MODULE__ = "Active"
__HELP__ = f"""
<b>✧ {command("AC_COMMAND")}</b> - Check active voice chats on the bot.

<b>✧ {command("ACTIVEVC_COMMAND")}</b> - Check active voice and video calls on the bot.

<b>✧ {command("ACTIVEVIDEO_COMMAND")}</b> - Check active video calls on the bot.

<b>✧ {command("STATS_COMMAND")}</b> - Check bot stats.
"""
