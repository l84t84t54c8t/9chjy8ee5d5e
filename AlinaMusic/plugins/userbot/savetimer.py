import logging
import os

from pyrogram import Client, filters
from pyrogram.types import Message

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Define the handler for self-destroying media messages
@Client.on_message(filters.media & filters.incoming, group=6)
async def save_timer_media(client: Client, message: Message):
    """
    Saves self-destructing media messages to the 'Saved Messages' chat.
    Deletes the local file after sending it.
    """
    try:
        if message.media:
            # Download the media file locally
            file_path = await message.download()
            logger.info(f"Media downloaded: {file_path}")

            # Send the file to the user's "Saved Messages" chat
            await client.send_document(
                "me",
                document=file_path,
                caption=message.caption or "Saved timer media",
            )
            logger.info("Media sent to 'Saved Messages'.")

            # Delete the local file
            os.remove(file_path)
            logger.info(f"Temporary file removed: {file_path}")

    except Exception as e:
        # Log the error and send an error message to the user
        logger.error(f"Failed to process message: {e}", exc_info=True)
        await message.reply_text(
            "An error occurred while saving the media. Please try again."
        )
