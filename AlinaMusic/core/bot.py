#
# Copyright (C) 2024 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved.
#
import uvloop

uvloop.install()


import sys

from pyrogram import Client
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import (
    ChatSendPhotosForbidden,
    ChatWriteForbidden,
    FloodWait,
)
from pyrogram.types import (
    BotCommand,
    BotCommandScopeAllChatAdministrators,
    BotCommandScopeAllGroupChats,
    BotCommandScopeAllPrivateChats,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

import config

from ..logging import LOGGER


class AlinaBot(Client):
    def __init__(self):
        LOGGER(__name__).info(f"Starting Bot")
        super().__init__(
            "AlinaMusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
        )

    async def edit_message_text(self, *args, **kwargs):
        try:
            return await super().edit_message_text(*args, **kwargs)
        except FloodWait as e:
            time = int(e.value)
            await asyncio.sleep(time)
            if time < 25:
                return await self.edit_message_text(self, *args, **kwargs)

    async def send_message(self, *args, **kwargs):
        if kwargs.get("send_direct", False):
            kwargs.pop("send_direct", None)
            return await super().send_message(*args, **kwargs)

        try:
            return await super().send_message(*args, **kwargs)
        except FloodWait as e:
            time = int(e.value)
            await asyncio.sleep(time)
            if time < 25:
                return await self.send_message(self, *args, **kwargs)
        except ChatWriteForbidden:
            chat_id = kwargs.get("chat_id") or args[0]
            if chat_id:
                await self.leave_chat(chat_id)
                

    async def send_photo(self, *args, **kwargs):
        try:
            return await super().send_photo(*args, **kwargs)
        except FloodWait as e:
            time = int(e.value)
            await asyncio.sleep(time)
            if time < 25:
                return await self.send_photo(self, *args, **kwargs)
        except ChatSendPhotosForbidden:
            chat_id = kwargs.get("chat_id") or args[0]
            if chat_id:
                await self.send_message(chat_id, "I don't have the right to send photos in this chat, leaving now..")
                await self.leave_chat(chat_id)

    async def start(self):
        await super().start()
        get_me = await self.get_me()
        self.username = get_me.username
        self.id = get_me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.mention = self.me.mention

        # Create the button
        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="๏ ᴀᴅᴅ ᴍᴇ ɪɴ ɢʀᴏᴜᴘ ๏",
                        url=f"https://t.me/{self.username}?startgroup=true",
                    )
                ]
            ]
        )

        try:
            await self.send_message(
                config.LOG_GROUP_ID,
                text="**╔═══❰𝐖𝐄𝐋𝐂𝐎𝐌𝐄❱═══❍⊱❁۪۪\n║\n║┣⪼🥀𝐁𝐨𝐭 𝐒𝐭𝐚𝐫𝐭𝐞𝐝 𝐁𝐚𝐛𝐲🎉\n║\n║◈ {self.mention}\n║\n║┣⪼🎈𝐈𝐃:- `{self.id}` \n║\n║┣⪼🎄@{self.username} \n║ \n║┣⪼💖𝐓𝐡𝐚𝐧𝐤𝐬 𝐅𝐨𝐫 𝐔𝐬𝐢𝐧𝐠😍\n║\n╚══════════════❍⊱❁**",
                reply_markup=button,
            )
        except:
            LOGGER(__name__).error(
                "Bot has failed to access the log group. Make sure that you have added your bot to your log channel and promoted as admin!"
            )
            # sys.exit()
        if config.SET_CMDS == str(True):
            try:
                await self.set_bot_commands(
                    commands=[
                        BotCommand("start", "• دەستپێکردنی بۆت"),
                        BotCommand("help", "• فەرمان و ڕوونکردنەوە"),
                        BotCommand("ping", "• پشکنینی بۆت"),
                    ],
                    scope=BotCommandScopeAllPrivateChats(),
                )
                await self.set_bot_commands(
                    commands=[
                         BotCommand("start", "• دەستپێکردنی بۆت"),
                        BotCommand("help", "• فەرمان و ڕوونکردنەوە"),
                        BotCommand("ping", "• پشکنینی بۆت"),
                        BotCommand("play", "• پەخشکردنی گۆرانی داواکراو"),
                        BotCommand("vplay", "• پەخشکردنی ڤیدیۆی داواکراو"),
                        BotCommand("stop", "• وەستاندنی پەخشکردن"),
                        BotCommand("pause", "• وەستاندنی پەخشکردن بۆ ماوەیەکی کاتی"),
                        BotCommand("resume", "• دەستپێکردنەوەی پەخشکردن"),
                        BotCommand("queue", "• پشکنین بۆ گۆرانی ڕیزکراو"),
                        BotCommand(
                            "skip", "• تێپەڕاندنی گۆرانی-پەخشکردن بۆ گۆرانی دواتر"
                        ),
                        BotCommand("reload", "• ڕیلۆدکردنی بۆت"),
                        BotCommand("end", "• وەستاندنی پەخشکردن"),
                        BotCommand("song", "• داگرتنی گۆرانی"),
                        BotCommand("video", "• داگرتنی ڤیدیۆ"),
                        BotCommand("couples", "• دیاری کردن کەپڵ تەنیا بۆخۆشی"),
                        BotCommand("cute", "• دیاری کردنی ڕێژەی قشتیت تەنیا یارییە"),
                        BotCommand(
                            "love", "• دیاری کردنی ڕێژەی خۆشەویستی نێوان دوو کەس"
                        ),
                        BotCommand("sudolist", "• لیستی گەشەپێدەرانی بۆت"),
                        BotCommand("dev", "• خاوەنی بۆت"),
                        BotCommand("staff", "• پیشاندانی ستافی ئەدمینەکان"),
                        BotCommand("bots", "• پیشاندانی بۆتەکانی گرووپ"),
                        BotCommand("botcheck", "• پشکنینی بۆتەکانی تێلەگرام"),
                        BotCommand("gdata", "• زانیاری گرووپەکان"),
                        BotCommand("stats", "• ئاماری بۆتی ئەلینا"),
                        BotCommand("admin", "• بانگکردنی ئەدمینەکانی گرووپ"),
                        BotCommand("gpt", "• چات جیپیتی"),
                        BotCommand("gemini", "• زیرەکی دەستکردی گوگڵ"),
                        BotCommand("tr", "• وەرگێڕانی دەق بۆ هەر زمانێك"),
                        BotCommand("lyrics", "• هێنانی ژێرنووسی گۆرانی"),
                    ],
                    scope=BotCommandScopeAllGroupChats(),
                )
                await self.set_bot_commands(
                    commands=[
                        BotCommand("start", "• دەستپێکردنی بۆت"),
                        BotCommand("ping", "• پشکنینی بۆت"),
                        BotCommand("help", "• فەرمانەکان"),
                        BotCommand("all", "• تاگکردنی ئەندامەکان بە دەق"),
                        BotCommand("cancel", "• وەستاندنی تاگکردن"),
                        BotCommand("settings", "• ڕێکخستی بۆت"),
                        BotCommand("reload", "• ڕیلۆدکردنی بۆت"),
                        BotCommand("play", "• پەخشکردنی گۆرانی داواکراو"),
                        BotCommand("vplay", "• پەخشکردنی ڤیدیۆی داواکاراو"),
                        BotCommand("pause", "• وەستاندنی پەخشکردن بۆ ماوەیەکی کاتی"),
                        BotCommand("resume", "• دەستپێکردنەوەی پەخشکردن"),
                        BotCommand("queue", "• پشکنین بۆ گۆرانی ڕیزکراو"),
                        BotCommand(
                            "skip", "• تێپەڕاندنی گۆرانی-پەخشکردن بۆ گۆرانی دواتر"
                        ),
                        BotCommand("end", "• وەستاندنی پەخشکردن"),
                        BotCommand("playlist", "• لیستی گۆرانی-پەخشکراو"),
                        BotCommand("stop", "• وەستاندنی پەخشکردن"),
                        BotCommand("lyrics", "• هێنانی دەقی گۆرانی"),
                        BotCommand("song", "• داگرتنی گۆرانی"),
                        BotCommand("video", "• داگرتنی ڤیدیۆ"),
                        BotCommand("couples", "• دیاری کردن کەپڵ تەنیا بۆخۆشی"),
                        BotCommand("cute", "• دیاری کردنی ڕێژەی قشتیت تەنیا یارییە"),
                        BotCommand(
                            "love", "• دیاری کردنی ڕێژەی خۆشەویستی نێوان دوو کەس"
                        ),
                        BotCommand("sudolist", "• لیستی گەشەپێدەرانی بۆت"),
                        BotCommand("dev", "• خاوەنی بۆت"),
                        BotCommand("filter", "• زیادکردنی چات"),
                        BotCommand("lang", "• گۆڕینی زمانی بۆت"),
                        BotCommand("welcome", "• دانانی بەخێرهاتن"),
                        BotCommand("staff", "• پیشاندانی ستافی ئەدمینەکان"),
                        BotCommand("bots", "• پیشاندانی بۆتەکانی گرووپ"),
                        BotCommand("botcheck", "• پشکنینی بۆتەکانی تێلەگرام"),
                        BotCommand("gdata", "• زانیاری گرووپەکان"),
                        BotCommand("stats", "• ئاماری بۆتی ئەلینا"),
                        BotCommand(
                            "story", "• بۆ داخستن و کردنەوەی ناردنی ستۆری لە گرووپ"
                        ),
                        BotCommand(
                            "forward", "• بۆ داخستن و کردنەوەی ناردنی ڕێکڵام لە گرووپ"
                        ),
                        BotCommand("admin", "• بانگکردنی ئەدمینەکانی گرووپ"),
                        BotCommand("gpt", "• چات جیپیتی"),
                        BotCommand("gemini", "• زیرەکی دەستکردی گوگڵ"),
                        BotCommand("tr", "• وەرگێڕانی دەق بۆ هەر زمانێك"),
                        BotCommand("ban", "• دەرکردنی-باندکردنی کەسێك"),
                        BotCommand("unban", "• لادانی باند-دەرکردنی لەسەر کەسێك"),
                        BotCommand("mute", "• کپکردنی-ئاگاداری کەسێك"),
                        BotCommand("unmute", "• لادانی ئاگاداری-کپکردن"),
                        BotCommand("warn", "• ئاگادارکردنەوەی کەسێک"),
                        BotCommand("promote", "• زیادکردنی ئەدمین"),
                        BotCommand("demote", "• لادانی ئەدمین"),
                        BotCommand("purge", "• سڕینەوەی چاتی گرووپ بە ڕیپلەی"),
                        BotCommand("open", "• کردنەوەی تێلی گرووپ"),
                        BotCommand("close", "• داخستنی تێلی گرووپ"),
                        BotCommand("playmode", "• گۆڕینی پەخشکردن"),
                        BotCommand("quran", "• پەخشکردنی قورئانی پیرۆز",
                        ),
                    ],
                    scope=BotCommandScopeAllChatAdministrators(),
                )
            except:
                pass
        else:
            pass
        try:
            a = await self.get_chat_member(config.LOG_GROUP_ID, self.id)
            if a.status != ChatMemberStatus.ADMINISTRATOR:
                LOGGER(__name__).error("Please promote bot as admin in logger group")
                sys.exit()
        except Exception:
            pass
        if get_me.last_name:
            self.name = get_me.first_name + " " + get_me.last_name
        else:
            self.name = get_me.first_name
        LOGGER(__name__).info(f"MusicBot started as {self.name}")

    async def stop(self):
        await super().stop()
