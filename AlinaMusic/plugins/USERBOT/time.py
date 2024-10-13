import asyncio
from datetime import datetime

from pytz import timezone

from AlinaMusic import userbot

# Set your timezone
target_timezone = timezone("Asia/Baghdad")


# Define the function to change the profile name
async def change_profile_name(client):
    # Fetch the current user details (await the coroutine)
    all = await client.get_me()
    firstName = all.first_name if all.first_name else ""
    lastName = all.last_name if all.last_name else ""
    allName = (
        f"{firstName} {lastName}".strip()
    )  # Combine first and last name, avoid extra space

    # Get the current time in the target timezone
    current_time = datetime.now(target_timezone).strftime("%I:%M %p")

    # Update the profile name with the current time
    new_name = f"{allName} - {current_time}"
    await client.update_profile(first_name=new_name)


# Start the client and run the profile name change
async def main():
    async with userbot:
        await change_profile_name(userbot)


# Run the main function
asyncio.run(main())
