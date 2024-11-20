import asyncio

from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import FloodWait
from pyrogram.types import Message

from AlinaMusic import app
from AlinaMusic.core.mongo import mongodb
from AlinaMusic.misc import SUDOERS
from AlinaMusic.utils import get_readable_time

chatsdb = mongodb.chats
usersdb = mongodb.tgusersdb


async def get_served_chats() -> list:
    return [chat async for chat in chatsdb.find({"chat_id": {"$lt": 0}})]


async def delete_served_chat(chat_id: int):
    await chatsdb.delete_one({"chat_id": chat_id})


async def get_served_users() -> list:
    return [user async for user in usersdb.find({"user_id": {"$gt": 0}})]


async def delete_served_user(user_id: int):
    await usersdb.delete_one({"user_id": user_id})


@app.on_message(filters.command(["rstats", "allstats"]) & SUDOERS)
async def all_stats(client, message: Message):
    chats = await get_served_chats()
    served_chats = [int(chat["chat_id"]) for chat in chats]
    time_expected = get_readable_time(len(served_chats))
    SKY = await message.reply_text(
        f"Getting all real stats of {app.mention}\n\nEstimated time: {time_expected}"
    )

    admin_chats = 0
    admin_not = 0
    chat_not = 0

    async def process_chat(chat_id):
        nonlocal admin_chats, admin_not, chat_not
        try:
            member = await app.get_chat_member(chat_id, app.me.id)
            if member.status == ChatMemberStatus.ADMINISTRATOR:
                admin_chats += 1
            else:
                admin_not += 1
        except FloodWait as fw:
            await asyncio.sleep(fw.value)
        except Exception:
            chat_not += 1
            await delete_served_chat(chat_id)  # Delete inaccessible chats

    await asyncio.gather(*(process_chat(chat_id) for chat_id in served_chats))

    await SKY.edit(
        f"Real stats of {app.mention}\n\n"
        f"Admin in chats: {admin_chats}\n"
        f"Not admin in chats: {admin_not}\n"
        f"Chats not accessible (deleted): {chat_not}"
    )


@app.on_message(filters.command(["ustats", "userstats"]) & SUDOERS)
async def user_stats(client, message: Message):
    users = await get_served_users()
    served_users = [int(user["user_id"]) for user in users]
    time_expected = get_readable_time(len(served_users))
    SKY = await message.reply_text(
        f"Getting all real user stats of {app.mention}\n\nEstimated time: {time_expected}"
    )

    active_users = 0
    inactive_users = 0
    user_not_found = 0

    async def process_user(user_id):
        nonlocal active_users, inactive_users, user_not_found
        try:
            user = await app.get_users(user_id)
            if user.is_bot:
                inactive_users += 1
            else:
                active_users += 1
        except FloodWait as fw:
            await asyncio.sleep(fw.value)
        except Exception:
            user_not_found += 1
            await delete_served_user(user_id)  # Delete inaccessible users

    await asyncio.gather(*(process_user(user_id) for user_id in served_users))

    await SKY.edit(
        f"Real user stats of {app.mention}\n\n"
        f"Active users: {active_users}\n"
        f"Inactive users (bots): {inactive_users}\n"
        f"Users not accessible (deleted): {user_not_found}"
    )
