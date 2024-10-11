#
# Copyright (C) 2024 by THE-VIP-BOY-OP@Github, < https://github.com/THE-VIP-BOY-OP >.
#
# This file is part of < https://github.com/THE-VIP-BOY-OP/VIP-MUSIC > project,
# and is released under the MIT License.
# Please see < https://github.com/THE-VIP-BOY-OP/VIP-MUSIC/blob/master/LICENSE >
#
# All rights reserved.
#
import asyncio

from pyrogram import filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message
from strings import get_command

from AlinaMusic import app
from AlinaMusic.misc import SUDOERS
from AlinaMusic.utils import get_readable_time
from AlinaMusic.utils.database import (
    add_banned_user,
    get_banned_count,
    get_banned_users,
    get_served_chats,
    is_banned_user,
    remove_banned_user,
)
from AlinaMusic.utils.decorators.language import language
from AlinaMusic.utils.extraction import extract_user
from config import BANNED_USERS

# Command
GBAN_COMMAND = get_command("GBAN_COMMAND")
UNGBAN_COMMAND = get_command("UNGBAN_COMMAND")
GBANNED_COMMAND = get_command("GBANNED_COMMAND")


@app.on_message(filters.command(GBAN_COMMAND) & SUDOERS)
@language
async def global_ban(client, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
    user = await extract_user(message)
    if user.id == message.from_user.id:
        return await message.reply_text(_["gban_1"])
    elif user.id == app.id:
        return await message.reply_text(_["gban_2"])
    elif user.id in SUDOERS:
        return await message.reply_text(_["gban_3"])
    is_gbanned = await is_banned_user(user.id)
    if is_gbanned:
        return await message.reply_text(_["gban_4"].format(user.mention))
    if user.id not in BANNED_USERS:
        BANNED_USERS.add(user.id)
    served_chats = []
    chats = await get_served_chats()
    for chat in chats:
        served_chats.append(int(chat["chat_id"]))
    time_expected = get_readable_time(len(served_chats))
    mystic = await message.reply_text(_["gban_5"].format(user.mention, time_expected))
    number_of_chats = 0
    for chat_id in served_chats:
        try:
            await app.ban_chat_member(chat_id, user.id)
            number_of_chats += 1
        except FloodWait as fw:
            await asyncio.sleep(int(fw.value))
        except:
            continue
    await add_banned_user(user.id)
    await message.reply_text(
        _["gban_6"].format(
            app.mention,
            message.chat.title,
            message.chat.id,
            user.mention,
            user.id,
            message.from_user.mention,
            number_of_chats,
        )
    )
    await mystic.delete()


@app.on_message(filters.command(UNGBAN_COMMAND) & SUDOERS)
@language
async def global_un(client, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
    user = await extract_user(message)
    is_gbanned = await is_banned_user(user.id)
    if not is_gbanned:
        return await message.reply_text(_["gban_7"].format(user.mention))
    if user.id in BANNED_USERS:
        BANNED_USERS.remove(user.id)
    served_chats = []
    chats = await get_served_chats()
    for chat in chats:
        served_chats.append(int(chat["chat_id"]))
    time_expected = get_readable_time(len(served_chats))
    mystic = await message.reply_text(_["gban_8"].format(user.mention, time_expected))
    number_of_chats = 0
    for chat_id in served_chats:
        try:
            await app.unban_chat_member(chat_id, user.id)
            number_of_chats += 1
        except FloodWait as fw:
            await asyncio.sleep(int(fw.value))
        except:
            continue
    await remove_banned_user(user.id)
    await message.reply_text(_["gban_9"].format(user.mention, number_of_chats))
    await mystic.delete()


@app.on_message(filters.command(GBANNED_COMMAND) & SUDOERS)
@language
async def gbanned_list(client, message: Message, _):
    counts = await get_banned_count()
    if counts == 0:
        return await message.reply_text(_["gban_10"])
    mystic = await message.reply_text(_["gban_11"])
    msg = _["gban_12"]
    count = 0
    users = await get_banned_users()
    for user_id in users:
        count += 1
        try:
            user = await app.get_users(user_id)
            user = user.first_name if not user.mention else user.mention
            msg += f"{count}➤ {user}\n"
        except Exception:
            msg += f"{count}➤ {user_id}\n"
            continue
    if count == 0:
        return await mystic.edit_text(_["gban_10"])
    else:
        return await mystic.edit_text(msg)


###############


@app.on_message(
    filters.command(["دەرکردنی گشتی", "باندکردنی گشتی", "باندی گشتی"], "") & SUDOERS
)
@language
async def global_ban(client, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
    user = await extract_user(message)
    if user.id == message.from_user.id:
        return await message.reply_text(_["gban_1"])
    elif user.id == app.id:
        return await message.reply_text(_["gban_2"])
    elif user.id in SUDOERS:
        return await message.reply_text(_["gban_3"])
    is_gbanned = await is_banned_user(user.id)
    if is_gbanned:
        return await message.reply_text(_["gban_4"].format(user.mention))
    if user.id not in BANNED_USERS:
        BANNED_USERS.add(user.id)
    served_chats = []
    chats = await get_served_chats()
    for chat in chats:
        served_chats.append(int(chat["chat_id"]))
    time_expected = get_readable_time(len(served_chats))
    mystic = await message.reply_text(_["gban_5"].format(user.mention, time_expected))
    number_of_chats = 0
    for chat_id in served_chats:
        try:
            await app.ban_chat_member(chat_id, user.id)
            number_of_chats += 1
        except FloodWait as fw:
            await asyncio.sleep(int(fw.value))
        except:
            continue
    await add_banned_user(user.id)
    await message.reply_text(
        _["gban_6"].format(
            app.mention,
            message.chat.title,
            message.chat.id,
            user.mention,
            user.id,
            message.from_user.mention,
            number_of_chats,
        )
    )
    await mystic.delete()


@app.on_message(
    filters.command(
        ["لادانی دەرکردنی گشتی", "لادانی باندکردنی گشتی", "لادانی باندی گشتی"], ""
    )
    & SUDOERS
)
@language
async def global_un(client, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
    user = await extract_user(message)
    is_gbanned = await is_banned_user(user.id)
    if not is_gbanned:
        return await message.reply_text(_["gban_7"].format(user.mention))
    if user.id in BANNED_USERS:
        BANNED_USERS.remove(user.id)
    served_chats = []
    chats = await get_served_chats()
    for chat in chats:
        served_chats.append(int(chat["chat_id"]))
    time_expected = get_readable_time(len(served_chats))
    mystic = await message.reply_text(_["gban_8"].format(user.mention, time_expected))
    number_of_chats = 0
    for chat_id in served_chats:
        try:
            await app.unban_chat_member(chat_id, user.id)
            number_of_chats += 1
        except FloodWait as fw:
            await asyncio.sleep(int(fw.value))
        except:
            continue
    await remove_banned_user(user.id)
    await message.reply_text(_["gban_9"].format(user.mention, number_of_chats))
    await mystic.delete()


@app.on_message(
    filters.command(["دەرکراوەکان", "دەرکراوەکانی گشتی", "باندکراوەکان"], "") & SUDOERS
)
@language
async def gbanned_list(client, message: Message, _):
    counts = await get_banned_count()
    if counts == 0:
        return await message.reply_text(_["gban_10"])
    mystic = await message.reply_text(_["gban_11"])
    msg = _["gban_12"]
    count = 0
    users = await get_banned_users()
    for user_id in users:
        count += 1
        try:
            user = await app.get_users(user_id)
            user = user.first_name if not user.mention else user.mention
            msg += f"{count}➤ {user}\n"
        except Exception:
            msg += f"{count}➤ {user_id}\n"
            continue
    if count == 0:
        return await mystic.edit_text(_["gban_10"])
    else:
        return await mystic.edit_text(msg)


# ==========================================================HARD GBAN=============================================


from datetime import datetime

from pyrogram import filters
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message, User

from AlinaMusic import app
from AlinaMusic.misc import SUDOERS
from AlinaMusic.utils.database import (
    add_banned_user,
    is_banned_user,
    remove_banned_user,
)
from config import BANNED_USERS


async def extract_user(m: Message) -> User:
    if m.reply_to_message:
        return m.reply_to_message.from_user
    msg_entities = m.entities[1] if m.text.startswith("/") else m.entities[0]
    return await app.get_users(
        msg_entities.user.id
        if msg_entities.type == MessageEntityType.TEXT_MENTION
        else int(m.command[1]) if m.command[1].isdecimal() else m.command[1]
    )


@app.on_message(filters.command("rgban") & SUDOERS)
async def sgban(client, message: Message):
    await message.delete()
    chat_id = message.chat.id
    msg = await message.reply("**زیادکرا بۆ دەرکراوە گشتییەکان**")
    await global_ban(client, message)


@app.on_message(filters.command("rungban") & SUDOERS)
async def sungban(client, message: Message):
    await message.delete()
    chat_id = message.chat.id
    msg = await message.reply("**سڕدرایەوە لە دەرکراوە گشتییەکان**")
    await global_unban(client, message)


async def extract_user_info(client, user_id):
    try:
        if user_id.startswith("@"):
            user = await client.get_users(user_id)
            user_id = user.id
            mention = user.mention
            username = user.username if user.username else int(user.id)
        else:
            user = await client.get_users(int(user_id))
            first_name = user.first_name
            user_id = user.id
            username = user.username if user.username else int(user.id)
            mention = f"<a href='tg://user?id={user_id}'>{first_name}</a>"
        return user_id, mention, username
    except ValueError:
        raise ValueError("**یوزەر یان ئایدی کەسەکەم پێبدە**")
    except Exception as e:
        raise e


async def global_ban(client, message: Message):
    try:
        user_id, reason = message.text.split(maxsplit=2)[1:]
    except ValueError:
        return await message.reply_text("**یوزەر یان ئایدی کەسەکەم پێبدە لەگەڵ هۆکار**")

    try:
        user_id, mention, username = await extract_user_info(client, user_id)
    except ValueError:
        return await message.reply_text("**یوزەر یان ئایدی کەسەکەم پێبدە**")
    except Exception as e:
        return await message.reply_text(f"An error occurred: {str(e)}")

    if user_id == message.from_user.id:
        return await message.reply_text("**تۆ ناتوانی خۆت دەربکەیت**")
    elif user_id == app.id:
        return await message.reply_text("**تۆ ناتوانی من دەربکەیت**")
    elif user_id in SUDOERS:
        return await message.reply_text("**تۆ ناتوانی گەشەپێدەر دەربکەیت**")

    is_gbanned = await is_banned_user(user_id)
    if is_gbanned:
        return await message.reply_text(
            f"**بەکارهێنەر :{mention}\nدەرکردنی گشتی لەسەر ئەنجام نەدراوە**"
        )

    if user_id not in BANNED_USERS:
        BANNED_USERS.add(user_id)
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    gban_by = message.from_user.id
    await add_banned_user(user_id)
    await message.reply("**دەرکرا ✅**")


async def global_unban(client, message: Message):
    try:
        user_id, reason = message.text.split(maxsplit=2)[1:]
    except ValueError:
        return await message.reply_text("**یوزەر یان ئایدی کەسەکەم پێبدە لەگەڵ هۆکار**")

    try:
        user_id, mention, username = await extract_user_info(client, user_id)
    except ValueError:
        return await message.reply_text("**یوزەر یان ئایدی کەسەکەم پێبدە**")
    except Exception as e:
        return await message.reply_text(f"An error occurred: {str(e)}")

    is_gbanned = await is_banned_user(user_id)
    if not is_gbanned:
        return await message.reply_text(
            f"**بەکارهێنەر :{mention}\nدەرکردنی گشتی لەسەر ئەنجام نەدراوە**"
        )

    if user_id in BANNED_USERS:
        BANNED_USERS.remove(user_id)
    await remove_banned_user(user_id)
    await message.reply("** باندی لادرا ✅**")
