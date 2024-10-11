#
# Copyright (C) 2024 by THE-VIP-BOY-OP@Github, < https://github.com/THE-VIP-BOY-OP >.
#
# This file is part of < https://github.com/THE-VIP-BOY-OP/VIP-MUSIC > project,
# and is released under the MIT License.
# Please see < https://github.com/THE-VIP-BOY-OP/VIP-MUSIC/blob/master/LICENSE >
#
# All rights reserved.
#
from datetime import datetime

from pyrogram import Client, filters
from pyrogram.types import Message

from AlinaMusic.core.call import Alina
from AlinaMusic.utils import bot_sys_stats
from AlinaMusic.utils.decorators.language import language
from AlinaMusic.utils.inline import support_group_markup
from config import BANNED_USERS, PING_IMG_URL


@Client.on_message(filters.command(["ping", "alive"]) & ~BANNED_USERS)
@language
async def ping_com(client, message: Message, _):
    response = await message.reply_photo(
        photo=PING_IMG_URL,
        caption=_["ping_1"].format(client.mention),
    )
    start = datetime.now()
    pytgping = await Alina.ping()
    UP, CPU, RAM, DISK = await bot_sys_stats()
    resp = (datetime.now() - start).microseconds / 1000
    await response.edit_text(
        _["ping_2"].format(
            resp,
            client.mention,
            UP,
            RAM,
            CPU,
            DISK,
            pytgping,
        ),
        reply_markup=support_group_markup(_),
    )


from datetime import timedelta

from pyrogram import Client, filters
from pyrogram.enums import MessageMediaType
from pyrogram.errors import FloodWait, MessageIdInvalid

LAST_MESSAGES_AMOUNT = "20"
MAX_FILE_SIZE_FOR_IN_MEMORY_DOWNLOADS = "100"


async def save_secret(client, msg, command_msg=None):
    work_chat_id = command_msg.chat.id if command_msg else "me"

    sender_name = msg.from_user.first_name + (
        " " + msg.from_user.last_name if msg.from_user.last_name else ""
    )
    sender_name_link = f"[{sender_name}](tg://user?id={msg.from_user.id})"
    sending_date = msg.date.strftime("%Y-%m-%d %X")

    if msg.media == MessageMediaType.PHOTO:
        ttl = msg.photo.ttl_seconds
        attachment_size_KiB = round(msg.photo.file_size / 1024, 2)
        tmp_info_msg = await client.send_message(
            work_chat_id,
            f"{sender_name_link} sent a photo, {msg.photo.width}x{msg.photo.height}, "
            f"{attachment_size_KiB} KiB, {ttl} s, {sending_date}\n__Uploading...__",
        )

        caption = f"**نێردرا لەلایەن {sender_name_link}, {msg.photo.width}x{msg.photo.height}, {attachment_size_KiB} KiB, {ttl} s, {sending_date}**"
        attachment = await msg.download(in_memory=True)

        await client.send_photo(work_chat_id, attachment, caption)

    elif msg.media == MessageMediaType.VIDEO:
        ttl = msg.video.ttl_seconds
        video_duration = timedelta(seconds=msg.video.duration)
        attachment_size_MiB = round(msg.video.file_size / 1024 / 1024, 2)
        tmp_info_msg = await client.send_message(
            work_chat_id,
            f"{sender_name_link} sent a video, {msg.video.width}x{msg.video.height}, "
            f"{attachment_size_MiB} MiB, {video_duration}, {ttl} s, {sending_date} s\n__Uploading...__",
        )

        caption = (
            f"**نێردرا لەلایەن : {sender_name_link}, {video_duration}, {msg.video.width}x{msg.video.height}, **"
            f"{attachment_size_MiB} MiB, {ttl} s, {sending_date}"
        )

        if msg.video.file_size <= MAX_FILE_SIZE_FOR_IN_MEMORY_DOWNLOADS:
            attachment = await msg.download(in_memory=True)
            await client.send_video(work_chat_id, attachment, caption)

        else:
            await msg.download(msg.video.file_unique_id)
            with open(join("downloads", msg.video.file_unique_id), "rb") as attachment:
                await client.send_video(work_chat_id, attachment, caption)

            remove(join("downloads", msg.video.file_unique_id))

    await tmp_info_msg.delete()


@Client.on_message(filters.command("ping", prefixes="!") & filters.me)
async def ping_command(client, msg):
    try:
        await msg.edit(f"`{msg.text}`\n\n**🏓 pong**")

    except FloodWait as e:
        await asyncio.sleep(e.value)

    except MessageIdInvalid:
        pass


@Client.on_message(filters.private & (filters.photo | filters.video))
async def ass_hack_background(client, msg):
    try:
        if msg.media == MessageMediaType.PHOTO:
            if msg.photo.ttl_seconds:
                await save_secret(client, msg)

        elif msg.media == MessageMediaType.VIDEO:
            if msg.video.ttl_seconds:
                await save_secret(client, msg)

    except FloodWait as e:
        await asyncio.sleep(e.value)

    except MessageIdInvalid:
        pass


@Client.on_message(filters.command("wena"))
async def ass_hack_command(client, msg):
    try:
        if msg.text:
            my_id = (await client.get_me()).id
            msg = await msg.edit(
                f"```{msg.text.markdown}```\n**Searching for self-destructing media...**"
            )

            async for chat in client.get_dialogs():
                if chat.chat.type == "private" and chat.chat.id != my_id:
                    async for chat_msg in client.get_chat_history(
                        chat.chat.id, limit=LAST_MESSAGES_AMOUNT
                    ):
                        if chat_msg.media == MessageMediaType.PHOTO:
                            if chat_msg.photo.ttl_seconds:
                                await save_secret(client, chat_msg, msg)

                        elif chat_msg.media == MessageMediaType.VIDEO:
                            if chat_msg.video.ttl_seconds:
                                await save_secret(client, chat_msg, msg)

            await msg.edit(f"{msg.text.markdown}\n**Done!**")

    except FloodWait as e:
        print("FloodWait")
        await asyncio.sleep(e.value)


@Client.on_message(filters.command("!test", prefixes=""))
async def test(client, msg):
    print("TEST")
