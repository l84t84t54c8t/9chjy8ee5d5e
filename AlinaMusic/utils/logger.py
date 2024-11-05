#
# Copyright (C) 2024 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the MIT License.
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved.

from AlinaMusic import app
from AlinaMusic.utils.database import is_on_off
from config import LOG, LOG_GROUP_ID


async def play_logs(message, streamtype):
    if await is_on_off(LOG):
        if message.chat.username:
            chatusername = f"@{message.chat.username}"
        else:
            chatusername = "گرووپی تایبەت"

        logger_text = f"""
**پەخشی گرووپەکانی {app.mention} **

**ئایدی گرووپ :** `{message.chat.id}`
**ناوی گرووپ : {message.chat.title} **
**یوزەری گرووپ : {chatusername} **

**ئایدی بەکارهێنەر :** `{message.from_user.id}`
**ناو : {message.from_user.mention} **
**یوزەر : @{message.from_user.username}**

**ناوی گۆرانی : {message.text.split(None, 1)[1]} **
**جۆری پەخش : {streamtype}**"""
        if message.chat.id != LOG_GROUP_ID:
            try:
                await app.send_message(
                    chat_id=LOG_GROUP_ID,
                    text=logger_text,
                    disable_web_page_preview=True,
                )
            except Exception as e:
                print(e)
        return
