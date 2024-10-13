from datetime import datetime

import pyrogram
from pytz import timezone

from AlinaMusic import userbot

target_timezone = timezone("Asia/Baghdad")


def change_profile_name():
    # Fetch the current user details
    all = client.get_me()
    firstName = all.first_name if all.first_name else ""
    lastName = all.last_name if all.last_name else ""
    allName = (
        f"{firstName} {lastName}".strip()
    )  # Combine first and last name, avoid extra space

    # Get the current time in the target timezone
    current_time = datetime.now(target_timezone).strftime("%I:%M %p")

    # Update the profile name with the current time
    new_name = f"{allName} - {current_time}"
    update_profile(first_name=new_name)


with userbot:
    while True:
        change_profile_name()
        pyrogram.idle()
