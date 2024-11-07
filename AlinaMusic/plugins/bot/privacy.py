from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

import config
from AlinaMusic import app
from AlinaMusic.misc import SUDOERS
from AlinaMusic.utils.database import (
    authuserdb,
    delete_playlist,
    delete_served_user,
    get_playlist_names,
    remove_sudo,
)
from config import BANNED_USERS
from strings import command

TEXT = f"""
🔒 **Privacy Policy for {app.mention} !**

Your privacy is important to us. To learn more about how we collect, use, and protect your data, please review our Privacy Policy here: [Privacy Policy](https://t.me/MGIMT).

If you have any questions or concerns, feel free to reach out to our [Support Team]({config.SUPPORT_GROUP}).
"""

PRIVACY_SECTIONS = {
    "collect": """
**What Information We Collect**

• Basic Telegram user data (ID, username)
• Chat/Group IDs where the bot is used
• Command usage and interactions
• Playlists and music preferences
• Voice chat participation data
• User settings and configurations
""",
    "why": """
**Why We Collect It**

• To provide music streaming services
• To maintain user playlists
• To process voice chat requests
• To manage user permissions
• To improve bot features
• To prevent abuse and spam
""",
    "do": """
**What We Do**

• Store data securely in encrypted databases
• Process music requests and streams
• Maintain user preferences
• Monitor for proper functionality
• Delete temporary files after use
• Implement security measures
""",
    "donot": """
**What We Don't Do**

• Share your data with third parties
• Store unnecessary personal information
• Keep data longer than needed
• Use data for marketing
• Track users across platforms
• Sell any user information
""",
    "rights": """
**Your Rights**

• Access your stored data
• Request data deletion
• Modify your settings
• Opt-out of data collection
• Report privacy concerns
• Contact support for help
""",
}


# New function to safely edit messages if content has changed
async def safe_edit_message_text(message, new_text, **kwargs):
    if message.text != new_text:
        await message.edit_text(new_text, **kwargs)
    else:
        print("Message content is the same; no edit performed.")


async def find_chat_ids_by_auth_user_id(auth_user_id):
    chat_ids = []
    async for document in authuserdb.find():
        for note_key, note_data in document.get("notes", {}).items():
            if note_data.get("auth_user_id") == auth_user_id:
                chat_ids.append(document["chat_id"])
    return chat_ids


async def delete_auth_user_data(auth_user_id):
    async for document in authuserdb.find():
        chat_id = document["chat_id"]
        notes = document.get("notes", {})
        keys_to_remove = [
            key
            for key, value in notes.items()
            if value.get("auth_user_id") == auth_user_id
        ]
        for key in keys_to_remove:
            notes.pop(key)
        if keys_to_remove:
            await authuserdb.update_one(
                {"chat_id": chat_id}, {"$set": {"notes": notes}}
            )


@app.on_message(command("PRIVACY_COMMAND") & ~BANNED_USERS)
async def privacy_menu(client, message: Message):
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Privacy Policy", callback_data="show_privacy_sections"
                )
            ],
            [
                InlineKeyboardButton("Retrieve Data", callback_data="retrieve_data"),
                InlineKeyboardButton("Delete Data", callback_data="delete_data"),
            ],
            [InlineKeyboardButton("Close", callback_data="close")],
        ]
    )
    await message.reply_text(TEXT, reply_markup=keyboard, disable_web_page_preview=True)


@app.on_callback_query(filters.regex("show_privacy_sections") & ~BANNED_USERS)
async def show_privacy_sections(client, callback_query):
    """Show detailed privacy policy sections"""
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("What We Collect", callback_data="privacy_collect")],
            [InlineKeyboardButton("Why We Collect", callback_data="privacy_why")],
            [InlineKeyboardButton("What We Do", callback_data="privacy_do")],
            [InlineKeyboardButton("What We Don't Do", callback_data="privacy_donot")],
            [InlineKeyboardButton("Your Rights", callback_data="privacy_rights")],
            [
                InlineKeyboardButton("Back", callback_data="privacy_back"),
                InlineKeyboardButton("Close", callback_data="close"),
            ],
        ]
    )
    await safe_edit_message_text(
        callback_query.message,
        f"{TEXT}\n\nSelect a section to learn more:",
        reply_markup=keyboard,
        disable_web_page_preview=True,
    )


@app.on_callback_query(filters.regex("privacy_") & ~BANNED_USERS)
async def privacy_section_callback(client, callback_query):
    """Handle privacy section callbacks"""
    section = callback_query.data.split("_")[1]

    if section == "back":
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Privacy Policy", callback_data="show_privacy_sections"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Retrieve Data", callback_data="retrieve_data"
                    ),
                    InlineKeyboardButton("Delete Data", callback_data="delete_data"),
                ],
                [InlineKeyboardButton("Close", callback_data="close")],
            ]
        )
        return await safe_edit_message_text(
            callback_query.message,
            TEXT,
            reply_markup=keyboard,
            disable_web_page_preview=True,
        )

    if section in PRIVACY_SECTIONS:
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Back", callback_data="show_privacy_sections"),
                    InlineKeyboardButton("Close", callback_data="close"),
                ],
            ]
        )
        await safe_edit_message_text(
            callback_query.message, PRIVACY_SECTIONS[section], reply_markup=keyboard
        )


@app.on_callback_query(filters.regex("retrieve_data"))
async def export_user_data(_, cq):
    await safe_edit_message_text(cq.message, "Please wait..")
    user_id = cq.from_user.id
    # Additional code for exporting user data


@app.on_callback_query(filters.regex("delete_data"))
async def retrieve_data(_, cq):
    await safe_edit_message_text(
        cq.message,
        "Are you sure you want to delete your data?",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Yes", callback_data="confirm_delete_data")],
                [InlineKeyboardButton("No", callback_data="privacy_back")],
            ]
        ),
    )


@app.on_callback_query(filters.regex("confirm_delete_data"))
async def delete_user_data(_, cq):
    await cq.answer("Please wait...", show_alert=True)

    user_id = cq.from_user.id
    # Additional code for deleting user data
    await safe_edit_message_text(cq.message, "Your data has been deleted from the bot.")


@app.on_callback_query(filters.regex("confirm_delete_data"))
async def delete_user_data(_, cq):
    await cq.answer("Please wait...", show_alert=True)

    user_id = cq.from_user.id

    try:
        _playlist = await get_playlist_names(user_id)
        for x in _playlist:
            await delete_playlist(user_id, x)
    except Exception:
        pass

    await delete_auth_user_data(user_id)
    await delete_served_user(user_id)

    if user_id in SUDOERS:
        SUDOERS.remove(user_id)
    try:
        await remove_sudo(user_id)
    except Exception:
        pass

    await delete_userss(user_id)
    await cq.edit_message_text("Your data has been deleted from the bot.")
