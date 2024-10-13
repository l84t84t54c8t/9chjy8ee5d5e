import asyncio
from datetime import datetime
import pyrogram
from pytz import timezone

from AlinaMusic import userbot

# Set your timezone
target_timezone = timezone("Asia/Baghdad")


async def change_profile_name():
    all = client.get_me()
    firstNmae = all.first_name if all.first_name else ""
    lastName = all.last_name if all.last_name else ""
    allName = firstNmae + " " + lastName
    current_time = datetime.now(target_timezone).strftime("%I:%M %p")
    new_name = f"{allName} - {current_time}"
    await client.update_profile(first_name=new_name)



with userbot:
    while True:
        change_profile_name(userbot)
        pyrogram.idle()
