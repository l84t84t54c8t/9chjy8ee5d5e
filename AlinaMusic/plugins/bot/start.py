#
# Copyright (C) 2024 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the MIT License.
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved.
#
import asyncio
import time

from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtubesearchpython.__future__ import VideosSearch

import config
from AlinaMusic import HELPABLE, Telegram, YouTube, app
from AlinaMusic.misc import SUDOERS, _boot_
from AlinaMusic.plugins.play.playlist import del_plist_msg
from AlinaMusic.plugins.sudo.sudoers import sudoers_list
from AlinaMusic.utils.database import (
    add_served_chat,
    add_served_user,
    get_assistant,
    get_lang,
    get_userss,
    is_banned_user,
    is_on_off,
    is_served_private_chat,
)
from AlinaMusic.utils.decorators.language import LanguageStart
from AlinaMusic.utils.formatters import get_readable_time
from AlinaMusic.utils.functions import MARKDOWN, WELCOMEHELP
from AlinaMusic.utils.inline import alive_panel, private_panel, start_pannel
from config import BANNED_USERS, START_IMG_URL
from strings import command, get_string

from .help import paginate_modules

loop = asyncio.get_running_loop()


@app.on_message(group=-1)
async def ban_new(client, message):
    user_id = (
        message.from_user.id if message.from_user and message.from_user.id else 777000
    )
    chat_name = message.chat.title if message.chat.title else ""

    # Ensure user_id is a valid type (string or int)
    if await is_banned_user(int(user_id)):  # Convert to int if necessary
        try:
            alert_message = "😳"
            BAN = await message.chat.ban_member(user_id)
            if BAN:
                await message.reply_text(alert_message)
        except Exception as e:
            print(f"Failed to ban member: {e}")


@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_comm(client, message: Message, _):
    chat_id = message.chat.id
    await add_served_user(message.from_user.id)
    await message.react("🕊️")
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name[0:4] == "help":
            keyboard = InlineKeyboardMarkup(
                paginate_modules(0, HELPABLE, close=True)
            )
            if config.START_IMG_URL:
                return await message.reply_photo(
                    photo=START_IMG_URL,
                    caption=_["help_1"],
                    reply_markup=keyboard,
                )
            else:
                return await message.reply_text(
                    text=_["help_1"],
                    reply_markup=keyboard,
                )
        if name[0:4] == "song":
            await message.reply_text(_["song_2"])
            return
        if name == "mkdwn_help":
            await message.reply(
                MARKDOWN,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )
        if name == "greetings":
            await message.reply(
                WELCOMEHELP,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )
        if name[0:3] == "sta":
            m = await message.reply_text("**🔎 گەڕان بۆ ئامار**")
            stats = await get_userss(message.from_user.id)
            tot = len(stats)
            if not stats:
                await asyncio.sleep(1)
                return await m.edit(_["ustats_1"])

            def get_stats():
                msg = ""
                limit = 0
                results = {}
                for i in stats:
                    top_list = stats[i]["spot"]
                    results[str(i)] = top_list
                    list_arranged = dict(
                        sorted(
                            results.items(),
                            key=lambda item: item[1],
                            reverse=True,
                        )
                    )
                if not results:
                    return m.edit(_["ustats_1"])
                tota = 0
                videoid = None
                for vidid, count in list_arranged.items():
                    tota += count
                    if limit == 10:
                        continue
                    if limit == 0:
                        videoid = vidid
                    limit += 1
                    details = stats.get(vidid)
                    title = (details["title"][:35]).title()
                    if vidid == "telegram":
                        msg += f"🔗[ᴛᴇʟᴇɢʀᴀᴍ ғɪʟᴇs ᴀɴᴅ ᴀᴜᴅɪᴏs]({config.SUPPORT_GROUP}) ** played {count} ᴛɪᴍᴇs**\n\n"
                    else:
                        msg += f"🔗 [{title}](https://www.youtube.com/watch?v={vidid}) ** played {count} times**\n\n"
                msg = _["ustats_2"].format(tot, tota, limit) + msg
                return videoid, msg

            try:
                videoid, msg = await loop.run_in_executor(None, get_stats)
            except Exception as e:
                print(e)
                return
            thumbnail = await YouTube.thumbnail(videoid, True)
            await m.delete()
            await message.reply_photo(photo=thumbnail, caption=msg)
            return
        if name[0:3] == "sud":
            await sudoers_list(client=client, message=message, _=_)
            await asyncio.sleep(1)
            if await is_on_off(config.LOG):
                return await app.send_message(
                    config.LOG_GROUP_ID,
                    f"**🧑🏻‍💻┋ کەسێکی نوێ هاتە ناو بۆت پشکنینی گەشەپێدەران\n\n👤┋ ناوی : {message.from_user.mention}\n👾┋ یوزەری : @{message.from_user.username}\n🆔┋ ئایدی :** `{message.from_user.id}`",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    message.from_user.first_name,
                                    url=f"https://t.me/{message.from_user.username}",
                                )
                            ]
                        ]
                    ),
                )
            return
        if name[0:3] == "lyr":
            query = (str(name)).replace("lyrics_", "", 1)
            lyrical = config.lyrical
            lyrics = lyrical.get(query)
            if lyrics:
                await Telegram.send_split_text(message, lyrics)
                return
            else:
                await message.reply_text("ғᴀɪʟᴇᴅ ᴛᴏ ɢᴇᴛ ʟʏʀɪᴄs.")
                return
        if name[0:3] == "del":
            await del_plist_msg(client=client, message=message, _=_)
            await asyncio.sleep(1)
        if name[0:3] == "inf":
            m = await message.reply_text("**🔎 گەڕان بۆ زانیاری گۆرانی**")
            query = (str(name)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
            searched_text = f"""
**🔍 زانیاری گۆرانی

❇️ ناونیشان : {title}

⏳ ماوە : {duration} Mins
👀 بینەر: {views}
⏰ کاتی بڵاوکردنەوە : {published}
🎥 کەناڵ : {channel}
📎 لینکی کەناڵ [ئێرە دابگرە]({channellink})
🔗 لینکی گۆرانی : [بەستەر]({link}) **
"""
            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="🎸 𝖵𝗂𝖽𝖾𝗈", callback_data=f"downloadvideo {query}"
                        ),
                        InlineKeyboardButton(
                            text="🎸 𝖠𝗎𝖽𝗂𝗈", callback_data=f"downloadaudio {query}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(text="🎧 sᴇᴇ ᴏɴ ʏᴏᴜᴛᴜʙᴇ 🎧", url=link),
                    ],
                ]
            )
            await m.delete()
            await app.send_photo(
                message.chat.id,
                photo=thumbnail,
                caption=searched_text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=key,
            )
            await asyncio.sleep(1)
            if await is_on_off(config.LOG):
                return await app.send_message(
                    config.LOG_GROUP_ID,
                    f"**🧑🏻‍💻┋ کەسێکی نوێ هاتە ناو بۆت زانیاری گۆرانی\n\n👤┋ ناوی : {message.from_user.mention}\n👾┋ یوزەری : @{message.from_user.username}\n🆔┋ ئایدی :** `{message.from_user.id}`",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    message.from_user.first_name,
                                    url=f"https://t.me/{message.from_user.username}",
                                )
                            ]
                        ]
                    ),
                )
    else:
        out = private_panel(_)
        vip = await message.reply_text(f"**بەخێربێی ئەزیزم ꨄ︎❣️.....**")
        await vip.edit_text(f"**بەخێربێی ئەزیزم ꨄ︎.❣️....**")
        await vip.edit_text(f"**بەخێربێی ئەزیزم ꨄ︎..❣️...**")
        await vip.edit_text(f"**بەخێربێی ئەزیزم ꨄ︎...❣️..**")
        await vip.edit_text(f"**بەخێربێی ئەزیزم ꨄ︎....❣️.**")
        await vip.edit_text(f"**بەخێربێی ئەزیزم ꨄ︎.....❣️**")

        await vip.delete()
        vips = await message.reply_text("**⚡د**")
        # await asyncio.sleep(0.1)
        await vips.edit_text("**⚡دە**")
        # await asyncio.sleep(0.1)
        await vips.edit_text("**⚡دەس**")
        # await asyncio.sleep(0.1)
        await vips.edit_text("**⚡دەست**")
        # await asyncio.sleep(0.1)
        await vips.edit_text("**⚡دەستپ**")
        # await asyncio.sleep(0.1)
        await vips.edit_text("**⚡دەستپێ**")
        # await asyncio.sleep(0.1)
        await vips.edit_text("**⚡دەستپێکردن .**")
        # await asyncio.sleep(0.1)
        await vips.edit_text("**⚡دەستپێکردن ..**")
        # await asyncio.sleep(0.1)
        await vips.edit_text("**⚡دەستپێکردن ...**")

        await vips.edit_text("**⚡دەستپێکردن .**")

        await vips.edit_text("**⚡دەستپێکردن ....**")
        photo_file = await app.download_media(message.from_user.photo.big_file_id)
        await vips.delete()

        if photo_file:
            try:
                await message.reply_photo(
                    photo=photo_file,
                    caption=_["start_1"].format(message.from_user.mention, app.mention),
                    reply_markup=InlineKeyboardMarkup(out),
                )
                if await is_on_off(config.LOG):
                    return await app.send_message(
                        config.LOG_GROUP_ID,
                        f"**🧑🏻‍💻┋ کەسێکی نوێ هاتە ناو بۆت\n\n👤┋ ناوی : {message.from_user.mention}\n👾┋ یوزەری : @{message.from_user.username}\n🆔┋ ئایدی :** `{message.from_user.id}`",
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        message.from_user.first_name,
                                        url=f"https://t.me/{message.from_user.username}",
                                    )
                                ]
                            ]
                        ),
                    )
            except Exception as e:

                await message.reply_photo(
                    photo=config.START_IMG_URL,
                    caption=_["start_1"].format(message.from_user.mention, app.mention),
                    reply_markup=InlineKeyboardMarkup(out),
                )
                if await is_on_off(config.LOG):
                    return await app.send_message(
                        config.LOG_GROUP_ID,
                        f"**🧑🏻‍💻┋ کەسێکی نوێ هاتە ناو بۆت\n\n👤┋ ناوی : {message.from_user.mention}\n👾┋ یوزەری : @{message.from_user.username}\n🆔┋ ئایدی :** `{message.from_user.id}`",
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        message.from_user.first_name,
                                        url=f"https://t.me/{message.from_user.username}",
                                    )
                                ]
                            ]
                        ),
                    )


@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def testbot(client, message: Message, _):
    photo_file = await app.download_media(message.chat.photo.big_file_id)
    out = alive_panel(_)
    uptime = int(time.time() - _boot_)
    chat_id = message.chat.id
    if photo_file:
        await message.reply_photo(
            photo=photo_file,
            caption=_["start_7"].format(app.mention, get_readable_time(uptime)),
            reply_markup=InlineKeyboardMarkup(out),
        )
    else:
        await message.reply_photo(
            photo=config.START_IMG_URL,
            caption=_["start_7"].format(app.mention, get_readable_time(uptime)),
            reply_markup=InlineKeyboardMarkup(out),
        )
    return await add_served_chat(message.chat.id)


@app.on_message(filters.new_chat_members, group=3)
async def welcome(client, message: Message):
    chat_id = message.chat.id
    if config.PRIVATE_BOT_MODE == str(True):
        if not await is_served_private_chat(message.chat.id):
            await message.reply_text(
                "**ᴛʜɪs ʙᴏᴛ's ᴘʀɪᴠᴀᴛᴇ ᴍᴏᴅᴇ ʜᴀs ʙᴇᴇɴ ᴇɴᴀʙʟᴇᴅ ᴏɴʟʏ ᴍʏ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜsᴇ ᴛʜɪs ɪғ ᴡᴀɴᴛ ᴛᴏ ᴜsᴇ ᴛʜɪs ɪɴ ʏᴏᴜʀ ᴄʜᴀᴛ sᴏ sᴀʏ ᴛᴏ ᴍʏ ᴏᴡɴᴇʀ ᴛᴏ ᴀᴜᴛʜᴏʀɪᴢᴇ ʏᴏᴜʀ ᴄʜᴀᴛ."
            )
            return await app.leave_chat(message.chat.id)
    else:
        await add_served_chat(chat_id)
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
            if member.id == app.id:
                photo_file = await app.download_media(message.chat.photo.big_file_id)
                userbot = await get_assistant(message.chat.id)
                out = start_pannel(_)
                await message.reply_photo(
                    photo=photo_file,
                    caption=_["start_2"].format(
                        message.from_user.mention,
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                )
            if member.id in config.OWNER_ID:
                return await message.reply_text(
                    _["start_3"].format(app.mention, member.mention)
                )
            if member.id in SUDOERS:
                return await message.reply_text(
                    _["start_4"].format(app.mention, member.mention)
                )
            return
        except:

            return


__MODULE__ = "Bot"
__HELP__ = f"""
<b>✦ c stands for channel play.</b>

<b>★ {command("STATS_COMMAND")}</b> - Get Top 10 Tracks Global Stats, Top 10 Users of Bot, Top 10 Chats on Bot, Top 10 Played in a chat, etc.

<b>★ {command("SUDOUSERS_COMMAND")}</b> - Check Sudo users of the bot.

<b>★ {command("LYRICS_COMMAND")} [Music Name]</b> - Search lyrics for the particular music on the web.

<b>★ {command("SONG_COMMAND")} [Track Name] or [YT Link]</b> - Download any track from YouTube in MP3 or MP4 formats.

<b>★ {command("QUEUE_COMMAND")}</b> - Check the queue list of music.

    <u><b>⚡️Private Bot:</b></u>
      
<b>✧ {command("AUTHORIZE_COMMAND")} [CHAT_ID]</b> - Allow a chat to use your bot.

<b>✧ {command("UNAUTHORIZE_COMMAND")} [CHAT_ID]</b> - Disallow a chat from using your bot.

<b>✧ {command("AUTHORIZED_COMMAND")}</b> - Check all allowed chats of your bot.
"""
