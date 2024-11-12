#
# Copyright (C) 2024 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the MIT License.
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved.

from AlinaMusic.core.bot import AlinaBot
from AlinaMusic.core.dir import dirr
from AlinaMusic.core.git import git
from AlinaMusic.core.userbot import Userbot
from AlinaMusic.core.youtube import alinatk
from AlinaMusic.misc import dbb, heroku, sudo

from .logging import LOGGER

# Directories
dirr()

# Check Git Updates
git()

# Initialize Memory DB
dbb()

# Heroku APP
heroku()

#youtube
alinatk()

# Load Sudo Users from DB
sudo()
# Bot Client
app = AlinaBot()

# Assistant Client
userbot = Userbot()

from .platforms import PlaTForms

Platform = PlaTForms()
HELPABLE = {}
