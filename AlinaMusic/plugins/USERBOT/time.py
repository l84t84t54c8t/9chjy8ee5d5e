import pyrogram
from pytz import timezone
from datetime import datetime

target_timezone = timezone('Asia/Baghdad')

def change_profile_name():
    all = client.get_me()
    firstNmae = all.first_name if all.first_name else ""
    lastName = all.last_name if all.last_name else ""
    allName = firstNmae + " " + lastName
    current_time = datetime.now(target_timezone).strftime("%I:%M %p")
    new_name = f"{allName} - {current_time}"
    client.update_profile(first_name=new_name)
  
        change_profile_name()
        pyrogram.idle()
