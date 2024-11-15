#
# Copyright (C) 2024 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the MIT License.
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved.
#
import uvloop

uvloop.install()


import sys

from pyrogram import Client
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import BotCommand
from pyrogram.types import BotCommandScopeAllChatAdministrators
from pyrogram.types import BotCommandScopeAllGroupChats
from pyrogram.types import BotCommandScopeAllPrivateChats
from pyrogram.types import BotCommandScopeChat
from pyrogram.types import BotCommandScopeChatMember, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import ChatSendPhotosForbidden
from pyrogram.errors import ChatWriteForbidden
from pyrogram.errors import FloodWait
from pyrogram.errors import MessageIdInvalid

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
            sleep_threshold=240,
            max_concurrent_transmissions=5,
            workers=50,
        )

    async def edit_message_text(self, *args, **kwargs):
        try:
            return await super().edit_message_text(*args, **kwargs)
        except FloodWait as e:
            time = int(e.value)
            await asyncio.sleep(time)
            if time < 25:
                return await self.edit_message_text(self, *args, **kwargs)
        except MessageIdInvalid:
            pass

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
                await self.send_message(
                    chat_id,
                    "I don't have the right to send photos in this chat, leaving now..",
                )
                await self.leave_chat(chat_id)

    async def start(self):
        await super().start()
        get_me = await self.get_me()
        self.username = get_me.username
        self.id = get_me.id
        self.name = f"{get_me.first_name} {get_me.last_name or ''}"
        self.mention = get_me.mention
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
                text=(
                    f"<u><b>{self.mention} Bot Started :</b></u>\n\n"
                    f"Id : <code>{self.id}</code>\n"
                    f"Name : {self.name}\n"
                    f"Username : @{self.username}"
                ),
                reply_markup=button,
            )
        except Exception as e:
            LOGGER(__name__).error(
                "Bot failed to access the log group. Ensure the bot is added and promoted as admin."
            )
            LOGGER(__name__).error("Error details:", exc_info=True)
            sys.exit()

        if config.SET_CMDS == str(True):
            try:
                await self._set_default_commands()
            except Exception as e:
                LOGGER(__name__).warning("Failed to set commands:", exc_info=True)

    async def _set_default_commands(self):
        private_commands = [
            BotCommand("start", "• دەستپێکردنی بۆت"),
            BotCommand("help", "• فەرمان و ڕوونکردنەوە"),
            BotCommand("ping", "• پشکنینی بۆت"),
        ]
        group_commands = [
            BotCommand("start", "• دەستپێکردنی بۆت"),
            BotCommand("help", "• فەرمان و ڕوونکردنەوە"),
            BotCommand("ping", "• پشکنینی بۆت"),
            BotCommand("play", "• پەخشکردنی گۆرانی داواکراو"),
            BotCommand("vplay", "• پەخشکردنی ڤیدیۆی داواکراو"),
            BotCommand("pause", "• وەستاندنی پەخشکردن بۆ ماوەیەکی کاتی"),
            BotCommand("resume", "• دەستپێکردنەوەی پەخشکردن"),
            BotCommand("skip", "• تێپەڕاندنی گۆرانی-پەخشکردن بۆ گۆرانی دواتر"),
            BotCommand("end", "• وەستاندنی پەخشکردن"),
            BotCommand("stop", "• وەستاندنی پەخشکردن"),
            BotCommand("admin", "• بانگکردنی ئەدمینەکانی گرووپ"),
            BotCommand("gpt", "• چات جیپیتی"),
            BotCommand("gemini", "• زیرەکی دەستکردی گوگڵ"),
            BotCommand("tr", "• وەرگێڕانی دەق بۆ هەر زمانێك"),
            BotCommand("couples", "• دیاری کردن کەپڵ تەنیا بۆخۆشی"),
            BotCommand("cute", "• دیاری کردنی ڕێژەی قشتیت تەنیا یارییە"),
            BotCommand("sudolist", "• لیستی گەشەپێدەرانی بۆت"),
            BotCommand("dev", "• خاوەنی بۆت"),
            BotCommand("staff", "• پیشاندانی ستافی ئەدمینەکان"),
            BotCommand("quran", "• پەخشکردنی قورئانی پیرۆز"),
        ]
        admin_commands = [
            BotCommand("start", "• دەستپێکردنی بۆت"),
            BotCommand("ping", "• پشکنینی بۆت"),
            BotCommand("help", "• فەرمانەکان"),
            BotCommand("play", "• پەخشکردنی گۆرانی داواکراو"),
            BotCommand("vplay", "• پەخشکردنی ڤیدیۆی داواکاراو"),
            BotCommand("playlist", "• لیستی گۆرانی-پەخشکراو"),
            BotCommand("quran", "• پەخشکردنی قورئانی پیرۆز"),
            BotCommand("pause", "• وەستاندنی پەخشکردن بۆ ماوەیەکی کاتی"),
            BotCommand("resume", "• دەستپێکردنەوەی پەخشکردن"),
            BotCommand("skip", "• تێپەڕاندنی گۆرانی-پەخشکردن بۆ گۆرانی دواتر"),
            BotCommand("end", "• وەستاندنی پەخشکردن"),
            BotCommand("stop", "• وەستاندنی پەخشکردن"),
            BotCommand("playmode", "• گۆڕینی پەخشکردن"),
            BotCommand("settings", "• ڕێکخستی بۆت"),
            BotCommand("all", "• تاگکردنی ئەندامەکان بە دەق"),
            BotCommand("cancel", "• وەستاندنی تاگکردن"),
            BotCommand("couples", "• دیاری کردن کەپڵ تەنیا بۆخۆشی"),
            BotCommand("cute", "• دیاری کردنی ڕێژەی قشتیت تەنیا یارییە"),
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
                        BotCommand("story", "• بۆ داخستن و کردنەوەی ناردنی ستۆری لە گرووپ"),
                        BotCommand("forward", "• بۆ داخستن و کردنەوەی ناردنی ڕێکڵام لە گرووپ"),
        ]
        owner_commands = [
            BotCommand("update", "Update the bot"),
            BotCommand("restart", "Restart the bot"),
            BotCommand("logs", "Get logs"),
            BotCommand("export", "Export all data of mongodb"),
            BotCommand("import", "Import all data in mongodb"),
            BotCommand("addsudo", "Add a user as a sudoer"),
            BotCommand("delsudo", "Remove a user from sudoers"),
            BotCommand("sudolist", "List all sudo users"),
            BotCommand("log", "Get the bot logs"),
            BotCommand("getvar", "Get a specific environment variable"),
            BotCommand("delvar", "Delete a specific environment variable"),
            BotCommand("setvar", "Set a specific environment variable"),
            BotCommand("usage", "Get dyno usage information"),
            BotCommand("maintenance", "Enable or disable maintenance mode"),
            BotCommand("logger", "Enable or disable logging"),
            BotCommand("block", "Block a user"),
            BotCommand("unblock", "Unblock a user"),
            BotCommand("blacklist", "Blacklist a chat"),
            BotCommand("whitelist", "Whitelist a chat"),
            BotCommand("blacklisted", "List all blacklisted chats"),
            BotCommand("autoend", "Enable or disable auto end for streams"),
            BotCommand("reboot", "Reboot the bot"),
            BotCommand("restart", "Restart the bot"),
        ]

        await self.set_bot_commands(private_commands, scope=BotCommandScopeAllPrivateChats())
        await self.set_bot_commands(group_commands, scope=BotCommandScopeAllGroupChats())
        await self.set_bot_commands(admin_commands, scope=BotCommandScopeAllChatAdministrators())

        LOG_GROUP_ID = f"@{config.LOG_GROUP_ID}" if isinstance(config.LOG_GROUP_ID, str) and not config.LOG_GROUP_ID.startswith("@") else config.LOG_GROUP_ID

        for owner_id in config.OWNER_ID:
            try:
                await self.set_bot_commands(owner_commands, scope=BotCommandScopeChatMember(chat_id=LOG_GROUP_ID, user_id=owner_id))
                await self.set_bot_commands(owner_commands, scope=BotCommandScopeChat(chat_id=owner_id))
            except Exception as e:
                LOGGER(__name__).warning("Failed to set owner commands for user %s:", owner_id, exc_info=True)

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
