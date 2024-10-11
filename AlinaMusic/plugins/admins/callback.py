#
# Copyright (C) 2024 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the MIT License.
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved.
#
import random

from pyrogram import filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from AlinaMusic import YouTube, app
from AlinaMusic.core.call import Alina
from AlinaMusic.misc import SUDOERS, db
from AlinaMusic.utils.database import (
    is_active_chat,
    is_music_playing,
    is_muted,
    is_nonadmin_chat,
    music_off,
    music_on,
    mute_off,
    mute_on,
    set_loop,
)
from AlinaMusic.utils.decorators.language import languageCB
from AlinaMusic.utils.formatters import seconds_to_min
from AlinaMusic.utils.inline import close_markup
from AlinaMusic.utils.inline.play import (
    panel_markup_1,
    panel_markup_2,
    panel_markup_3,
    stream_markup,
    telegram_markup,
)
from AlinaMusic.utils.stream.autoclear import auto_clean
from AlinaMusic.utils.thumbnails import gen_thumb
from config import (
    BANNED_USERS,
    SOUNCLOUD_IMG_URL,
    STREAM_IMG_URL,
    SUPPORT_GROUP,
    TELEGRAM_AUDIO_URL,
    TELEGRAM_VIDEO_URL,
    adminlist,
)

wrong = {}
downvote = {}
downvoters = {}

# =============================FUNCTIONS==============================#


@app.on_callback_query(filters.regex("unban_assistant"))
async def unban_assistant(_, callback: CallbackQuery):
    chat_id = callback.message.chat.id
    userbot = await get_assistant(chat_id)

    try:
        await app.unban_chat_member(chat_id, userbot.id)
        await callback.answer(
            "⇜ بە سەرکەوتوویی باندی ئەکاونتی یاریدەدەر لادرا♥\n\n⇜ ئێستا دەتوانی گۆرانی لێ بدەیت🎻\n\n⇜ لێدانی گۆرانی : /play + ناوی گۆرانی ⎋",
            show_alert=True,
        )
    except Exception as e:
        await callback.answer(
            f"⇜ شکستی هێنا لە لادانی باندی ئەکاونتی یاریدەدەر ڕۆڵم نییە\n\n⇜ ڕۆڵم پێبدە بۆ لادانی باندی ئەکاونتی یاریدەدەر ⎋",
            show_alert=True,
        )


@app.on_callback_query(filters.regex("PanelMarkup") & ~BANNED_USERS)
@languageCB
async def markup_panel(client, CallbackQuery: CallbackQuery, _):
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    videoid, chat_id = callback_request.split("|")
    chat_id = CallbackQuery.message.chat.id
    buttons = panel_markup_1(_, videoid, chat_id)
    try:
        await CallbackQuery.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except:
        return
    if chat_id not in wrong:
        wrong[chat_id] = {}
    wrong[chat_id][CallbackQuery.message.id] = False


@app.on_callback_query(filters.regex("MainMarkup") & ~BANNED_USERS)
@languageCB
async def del_back_playlist(client, CallbackQuery, _):
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    videoid, chat_id = callback_request.split("|")
    if videoid == str(None):
        buttons = telegram_markup(_, chat_id)
    else:
        buttons = stream_markup(_, videoid, chat_id)
    chat_id = CallbackQuery.message.chat.id
    try:
        await CallbackQuery.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except:
        return
    if chat_id not in wrong:
        wrong[chat_id] = {}
    wrong[chat_id][CallbackQuery.message.id] = True


@app.on_callback_query(filters.regex("Pages") & ~BANNED_USERS)
@languageCB
async def del_back_playlist(client, CallbackQuery, _):
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    state, pages, videoid, chat = callback_request.split("|")
    chat_id = int(chat)
    pages = int(pages)
    if state == "Forw":
        if pages == 0:
            buttons = panel_markup_2(_, videoid, chat_id)
        if pages == 2:
            buttons = panel_markup_1(_, videoid, chat_id)
        if pages == 1:
            buttons = panel_markup_3(_, videoid, chat_id)
    if state == "Back":
        if pages == 2:
            buttons = panel_markup_2(_, videoid, chat_id)
        if pages == 1:
            buttons = panel_markup_1(_, videoid, chat_id)
        if pages == 0:
            buttons = panel_markup_3(_, videoid, chat_id)
    try:
        await CallbackQuery.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except:
        return


@app.on_callback_query(filters.regex("ADMIN") & ~BANNED_USERS)
@languageCB
async def del_back_playlist(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    command, chat = callback_request.split("|")
    chat_id = int(chat)
    if not await is_active_chat(chat_id):
        return await CallbackQuery.answer(_["general_6"], show_alert=True)
    mention = CallbackQuery.from_user.mention
    if command == "UpVote":
        if chat_id not in votemode:
            votemode[chat_id] = {}
        if chat_id not in upvoters:
            upvoters[chat_id] = {}

        voters = (upvoters[chat_id]).get(CallbackQuery.message.id)
        if not voters:
            upvoters[chat_id][CallbackQuery.message.id] = []

        vote = (votemode[chat_id]).get(CallbackQuery.message.id)
        if not vote:
            votemode[chat_id][CallbackQuery.message.id] = 0

        if CallbackQuery.from_user.id in upvoters[chat_id][CallbackQuery.message.id]:
            (upvoters[chat_id][CallbackQuery.message.id]).remove(
                CallbackQuery.from_user.id
            )
            votemode[chat_id][CallbackQuery.message.id] -= 1
        else:
            (upvoters[chat_id][CallbackQuery.message.id]).append(
                CallbackQuery.from_user.id
            )
            votemode[chat_id][CallbackQuery.message.id] += 1
        upvote = await get_upvote_count(chat_id)
        get_upvotes = int(votemode[chat_id][CallbackQuery.message.id])
        if get_upvotes >= upvote:
            votemode[chat_id][CallbackQuery.message.id] = upvote
            try:
                exists = confirmer[chat_id][CallbackQuery.message.id]
                current = db[chat_id][0]
            except:
                return await CallbackQuery.edit_message_text(f"ғᴀɪʟᴇᴅ.")
            try:
                if current["vidid"] != exists["vidid"]:
                    return await CallbackQuery.edit_message.text(_["admin_35"])
                if current["file"] != exists["file"]:
                    return await CallbackQuery.edit_message.text(_["admin_35"])
            except:
                return await CallbackQuery.edit_message_text(_["admin_36"])
            try:
                await CallbackQuery.edit_message_text(_["admin_37"].format(upvote))
            except:
                pass
            command = counter
            mention = "ᴜᴘᴠᴏᴛᴇs"
        else:
            if (
                CallbackQuery.from_user.id
                in upvoters[chat_id][CallbackQuery.message.id]
            ):
                await CallbackQuery.answer(_["admin_38"], show_alert=True)
            else:
                await CallbackQuery.answer(_["admin_39"], show_alert=True)
            upl = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text=f"❤ {get_upvotes}",
                            callback_data=f"ADMIN  UpVote|{chat_id}_{counter}",
                        )
                    ]
                ]
            )
            await CallbackQuery.answer(_["admin_40"], show_alert=True)
            return await CallbackQuery.edit_message_reply_markup(reply_markup=upl)
    else:
        is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
        if not is_non_admin:
            if CallbackQuery.from_user.id not in SUDOERS:
                admins = adminlist.get(CallbackQuery.message.chat.id)
                if not admins:
                    return await CallbackQuery.answer(_["admin_18"], show_alert=True)
                else:
                    if CallbackQuery.from_user.id not in admins:
                        return await CallbackQuery.answer(
                            _["admin_19"], show_alert=True
                        )
    if command == "Pause":
        if not await is_music_playing(chat_id):
            return await CallbackQuery.answer(_["admin_1"], show_alert=True)
        await CallbackQuery.answer()
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
        await CallbackQuery.message.reply_text(
            _["admin_2"].format(mention), reply_markup=InlineKeyboardMarkup(buttons)
        )
    elif command == "Resume":
        if await is_music_playing(chat_id):
            return await CallbackQuery.answer(_["admin_3"], show_alert=True)
        await CallbackQuery.answer()
        await music_on(chat_id)
        await Alina.resume_stream(chat_id)
        buttons_resume = [
            [
                InlineKeyboardButton(
                    text="‣‣I 𝖲𝗄𝗂𝗉", callback_data=f"ADMIN Skip|{chat_id}"
                ),
                InlineKeyboardButton(
                    text="▢ 𝖲𝗍𝗈𝗉", callback_data=f"ADMIN Stop|{chat_id}"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="II 𝖯𝖺𝗎𝗌𝖾",
                    callback_data=f"ADMIN Pause|{chat_id}",
                ),
            ],
        ]

        await CallbackQuery.message.reply_text(
            _["admin_4"].format(mention),
            reply_markup=InlineKeyboardMarkup(buttons_resume),
        )
    elif command == "Stop" or command == "End":
        await CallbackQuery.answer()
        await Alina.stop_stream(chat_id)
        await set_loop(chat_id, 0)
        await CallbackQuery.message.reply_text(
            _["admin_9"].format(mention), reply_markup=close_markup(_)
        )
        await CallbackQuery.message.delete()
    elif command == "Mute":
        if await is_muted(chat_id):
            return await CallbackQuery.answer(_["admin_5"], show_alert=True)
        await CallbackQuery.answer()
        await mute_on(chat_id)
        await Alina.mute_stream(chat_id)
        await CallbackQuery.message.reply_text(_["admin_6"].format(mention))
    elif command == "Unmute":
        if not await is_muted(chat_id):
            return await CallbackQuery.answer(_["admin_7"], show_alert=True)
        await CallbackQuery.answer()
        await mute_off(chat_id)
        await Alina.unmute_stream(chat_id)
        await CallbackQuery.message.reply_text(_["admin_8"].format(mention))
    elif command == "Loop":
        await CallbackQuery.answer()
        await set_loop(chat_id, 3)
        await CallbackQuery.message.reply_text(_["admin_25"].format(mention, 3))
    elif command == "Shuffle":
        check = db.get(chat_id)
        if not check:
            return await CallbackQuery.answer(_["admin_21"], show_alert=True)
        try:
            popped = check.pop(0)
        except:
            return await CallbackQuery.answer(_["admin_22"], show_alert=True)
        check = db.get(chat_id)
        if not check:
            check.insert(0, popped)
            return await CallbackQuery.answer(_["admin_22"], show_alert=True)
        await CallbackQuery.answer()
        random.shuffle(check)
        check.insert(0, popped)
        await CallbackQuery.message.reply_text(_["admin_23"].format(mention))
    elif command == "Skip" or command == "Replay":
        check = db.get(chat_id)
        if command == "Skip":
            txt = f"<b>●꒐ پەخشکردن تێپەڕێندرا♥•\n●꒐ لەلایەن : {mention} ⎋</b>"
            popped = None
            try:
                popped = check.pop(0)
                if popped:
                    await auto_clean(popped)
                if not check:
                    await CallbackQuery.edit_message_text(
                        f"<b>●꒐ پەخشکردن تێپەڕێندرا♥•\n●꒐ لەلایەن : {mention} ⎋</b>"
                    )
                    await CallbackQuery.message.reply_text(
                        text=_["admin_10"].format(
                            mention, CallbackQuery.message.chat.title
                        ),
                        reply_markup=close_markup(_),
                    )
                    try:
                        return await Alina.stop_stream(chat_id)
                    except:
                        return
            except:
                try:
                    await CallbackQuery.edit_message_text(
                        f"<b>●꒐ پەخشکردن تێپەڕێندرا♥•\n●꒐ لەلایەن : {mention} ⎋</b>"
                    )
                    await CallbackQuery.message.reply_text(
                        text=_["admin_6"].format(
                            mention, CallbackQuery.message.chat.title
                        ),
                        reply_markup=close_markup(_),
                    )
                    return await Alina.st_stream(chat_id)
                except:
                    return
        else:
            txt = f"<b>●꒐ پەخشکردن دووبارەکرایەوە ♥•\n●꒐ لەلایەن : {mention} ⎋</b>"
        await CallbackQuery.answer()
        queued = check[0]["file"]
        title = (check[0]["title"]).title()
        user = check[0]["by"]
        duration = check[0]["dur"]
        streamtype = check[0]["streamtype"]
        videoid = check[0]["vidid"]
        status = True if str(streamtype) == "video" else None
        db[chat_id][0]["played"] = 0
        exis = (check[0]).get("old_dur")
        if exis:
            db[chat_id][0]["dur"] = exis
            db[chat_id][0]["seconds"] = check[0]["old_second"]
            db[chat_id][0]["speed_path"] = None
            db[chat_id][0]["speed"] = 1.0
        if "live_" in queued:
            n, link = await YouTube.video(videoid, True)
            if n == 0:
                return await CallbackQuery.message.reply_text(
                    text=_["admin_11"].format(title),
                    reply_markup=close_markup(_),
                )
            try:
                image = await YouTube.thumbnail(videoid, True)
            except:
                image = None
            try:
                await Alina.skip_stream(chat_id, link, video=status, image=image)
            except:
                return await CallbackQuery.message.reply_text(_["call_7"])
            button = telegram_markup(_, chat_id)
            img = await gen_thumb(videoid)
            run = await CallbackQuery.message.reply_photo(
                photo=img,
                caption=_["stream_1"].format(
                    f"https://t.me/{app.username}?start=info_{videoid}",
                    title[:23],
                    duration,
                    user,
                ),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
            await CallbackQuery.edit_message_text(txt, reply_markup=close_markup(_))
        elif "vid_" in queued:
            mystic = await CallbackQuery.message.reply_text(
                _["call_8"], disable_web_page_preview=True
            )
            try:
                file_path, direct = await YouTube.download(
                    videoid,
                    mystic,
                    videoid=True,
                    video=status,
                )
            except:
                return await mystic.edit_text(_["call_7"])
            try:
                image = await YouTube.thumbnail(videoid, True)
            except:
                image = None
            try:
                await Alina.skip_stream(chat_id, file_path, video=status, image=image)
            except Exception:
                return await mystic.edit_text(_["call_7"])
            button = stream_markup(_, videoid, chat_id)
            img = await gen_thumb(videoid)
            run = await CallbackQuery.message.reply_photo(
                photo=img,
                caption=_["stream_1"].format(
                    f"https://t.me/{app.username}?start=info_{videoid}",
                    title[:23],
                    duration,
                    user,
                ),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "stream"
            await CallbackQuery.edit_message_text(txt, reply_markup=close_markup(_))
            await mystic.delete()
        elif "index_" in queued:
            try:
                await Alina.skip_stream(chat_id, videoid, video=status)
            except Exception:
                return await CallbackQuery.message.reply_text(_["call_7"])
            button = telegram_markup(_, chat_id)
            run = await CallbackQuery.message.reply_photo(
                photo=STREAM_IMG_URL,
                caption=_["stream_2"].format(user),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
            await CallbackQuery.edit_message_text(txt, reply_markup=close_markup(_))
        else:
            if videoid == "telegram":
                image = None
            elif videoid == "soundcloud":
                image = None
            else:
                try:
                    image = await YouTube.thumbnail(videoid, True)
                except:
                    image = None
            try:
                await Alina.skip_stream(chat_id, queued, video=status, image=image)
            except Exception:
                return await CallbackQuery.message.reply_text(_["call_7"])
            if videoid == "telegram":
                button = telegram_markup(_, chat_id)
                run = await CallbackQuery.message.reply_photo(
                    photo=(
                        TELEGRAM_AUDIO_URL
                        if str(streamtype) == "audio"
                        else TELEGRAM_VIDEO_URL
                    ),
                    caption=_["stream_1"].format(
                        SUPPORT_GROUP, title[:23], duration, user
                    ),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "tg"
            elif videoid == "soundcloud":
                button = telegram_markup(_, chat_id)
                run = await CallbackQuery.message.reply_photo(
                    photo=(
                        SOUNCLOUD_IMG_URL
                        if str(streamtype) == "audio"
                        else TELEGRAM_VIDEO_URL
                    ),
                    caption=_["stream_1"].format(
                        SUPPORT_GROUP, title[:23], duration, user
                    ),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "tg"
            else:
                button = stream_markup(_, videoid, chat_id)
                img = await gen_thumb(videoid)
                run = await CallbackQuery.message.reply_photo(
                    photo=img,
                    caption=_["stream_1"].format(
                        f"https://t.me/{app.username}?start=info_{videoid}",
                        title[:23],
                        duration,
                        user,
                    ),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "stream"
            await CallbackQuery.edit_message_text(txt, reply_markup=close_markup(_))

    else:
        playing = db.get(chat_id)
        if not playing:
            return await CallbackQuery.answer(_["queue_2"], show_alert=True)
        duration_seconds = int(playing[0]["seconds"])
        if duration_seconds == 0:
            return await CallbackQuery.answer(_["admin_30"], show_alert=True)
        file_path = playing[0]["file"]
        if "index_" in file_path or "live_" in file_path:
            return await CallbackQuery.answer(_["admin_30"], show_alert=True)
        duration_played = int(playing[0]["played"])
        if int(command) in [1, 2]:
            duration_to_skip = 10
        else:
            duration_to_skip = 30
        duration = playing[0]["dur"]
        if int(command) in [1, 3]:
            if (duration_played - duration_to_skip) <= 10:
                bet = seconds_to_min(duration_played)
                return await CallbackQuery.answer(
                    f"<b>» بۆت ناتوانێت گۆرانی بباتە پێش چونکە ماوەی پەخشکردن تێپەڕیوە\n\nپەخشدەکرێت : {bet} لە خولەکی {duration} ⎋</b>",
                    show_alert=True,
                )
            to_seek = duration_played - duration_to_skip + 1
        else:
            if (duration_seconds - (duration_played + duration_to_skip)) <= 10:
                bet = seconds_to_min(duration_played)
                return await CallbackQuery.answer(
                    f"<b>» بۆت ناتوانێت گۆرانی بباتە پێش چونکە ماوەی پەخشکردن تێپەڕیوە\n\nپەخشدەکرێت : {bet} لە خولەکی {duration} ⎋</b>",
                    show_alert=True,
                )
            to_seek = duration_played + duration_to_skip + 1
        await CallbackQuery.answer()
        mystic = await CallbackQuery.message.reply_text(_["admin_32"])
        if "vid_" in file_path:
            n, file_path = await YouTube.video(playing[0]["vidid"], True)
            if n == 0:
                return await mystic.edit_text(_["admin_30"])
        try:
            await Alina.seek_stream(
                chat_id,
                file_path,
                seconds_to_min(to_seek),
                duration,
                playing[0]["streamtype"],
            )
        except:
            return await mystic.edit_text(_["admin_34"])
        if int(command) in [1, 3]:
            db[chat_id][0]["played"] -= duration_to_skip
        else:
            db[chat_id][0]["played"] += duration_to_skip
        string = _["admin_33"].format(seconds_to_min(to_seek))
        await mystic.edit_text(f"{string}\n\nᴄʜᴀɴɢᴇs ᴅᴏɴᴇ ʙʏ : {mention} !")


__MODULE__ = "Adᴍɪɴ"
__HELP__ = """

<b>c sᴛᴀɴᴅs ғᴏʀ ᴄʜᴀɴɴᴇʟ ᴘʟᴀʏ.</b>

<b>✧ /pause</b> ᴏʀ <b>/cpause</b> - Pᴀᴜsᴇ ᴛʜᴇ ᴘʟᴀʏɪɴɢ ᴍᴜsɪᴄ.
<b>✧ /resume</b> ᴏʀ <b>/cresume</b> - Rᴇsᴜᴍᴇ ᴛʜᴇ ᴘᴀᴜsᴇᴅ ᴍᴜsɪᴄ.
<b>✧ /mute</b> ᴏʀ <b>/cmute</b> - Mᴜᴛᴇ ᴛʜᴇ ᴘʟᴀʏɪɴɢ ᴍᴜsɪᴄ.
<b>✧ /unmute</b> ᴏʀ <b>/cunmute</b> - Uɴᴍᴜᴛᴇ ᴛʜᴇ ᴍᴜᴛᴇᴅ ᴍᴜsɪᴄ.
<b>✧ /skip</b> ᴏʀ <b>/cskip</b> - Sᴋɪᴘ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴘʟᴀʏɪɴɢ ᴍᴜsɪᴄ.
<b>✧ /stop</b> ᴏʀ <b>/cstop</b> - Sᴛᴏᴘ ᴛʜᴇ ᴘʟᴀʏɪɴɢ ᴍᴜsɪᴄ.
<b>✧ /shuffle</b> ᴏʀ <b>/cshuffle</b> - Rᴀɴᴅᴏᴍʟʏ sʜᴜғғʟᴇs ᴛʜᴇ ǫᴜᴇᴜᴇᴅ ᴘʟᴀʏʟɪsᴛ.
<b>✧ /seek</b> ᴏʀ <b>/cseek</b> - Fᴏʀᴡᴀʀᴅ Sᴇᴇᴋ ᴛʜᴇ ᴍᴜsɪᴄ ᴛᴏ ʏᴏᴜʀ ᴅᴜʀᴀᴛɪᴏɴ.
<b>✧ /seekback</b> ᴏʀ <b>/cseekback</b> - Bᴀᴄᴋᴡᴀʀᴅ Sᴇᴇᴋ ᴛʜᴇ ᴍᴜsɪᴄ ᴛᴏ ʏᴏᴜʀ ᴅᴜʀᴀᴛɪᴏɴ.
<b>✧ /reboot</b> - Rᴇʙᴏᴏᴛ ʙᴏᴛ ғᴏʀ ʏᴏᴜʀ ᴄʜᴀᴛ.

<b>✧ /skip</b> ᴏʀ <b>/cskip</b> [Nᴜᴍʙᴇʀ (ᴇxᴀᴍᴘʟᴇ: 𝟹)] - Sᴋɪᴘs ᴍᴜsɪᴄ ᴛᴏ ᴀ ᴛʜᴇ sᴘᴇᴄɪғɪᴇᴅ ǫᴜᴇᴜᴇᴅ ɴᴜᴍʙᴇʀ. Exᴀᴍᴘʟᴇ: <b>/skip 𝟹</b> ᴡɪʟʟ sᴋɪᴘ ᴍᴜsɪᴄ ᴛᴏ ᴛʜɪʀᴅ ǫᴜᴇᴜᴇᴅ ᴍᴜsɪᴄ ᴀɴᴅ ᴡɪʟʟ ɪɢɴᴏʀᴇ 𝟷 ᴀɴᴅ 𝟸 ᴍᴜsɪᴄ ɪɴ ǫᴜᴇᴜᴇ.

<b>✧ /loop</b> ᴏʀ <b>/cloop</b> [ᴇɴᴀʙʟᴇ/ᴅɪsᴀʙʟᴇ] ᴏʀ [Nᴜᴍʙᴇʀs ʙᴇᴛᴡᴇᴇɴ 𝟷-𝟷𝟶] - Wʜᴇɴ ᴀᴄᴛɪᴠᴀᴛᴇᴅ, ʙᴏᴛ ʟᴏᴏᴘs ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴘʟᴀʏɪɴɢ ᴍᴜsɪᴄ ᴛᴏ 𝟷-𝟷𝟶 ᴛɪᴍᴇs ᴏɴ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ. Dᴇғᴀᴜʟᴛ ᴛᴏ 𝟷𝟶 ᴛɪᴍᴇs."""
