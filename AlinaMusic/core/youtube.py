import json
import os

YOUTUBE = {
    "access_token": "ya29.a0AeDClZB5oA7xQTeij93wO_83g7GpTbWmL2fjJZ-v4_4OVLWQL1U3VGXkNGpbGOPSBu-qMthrWAtSMM2DU494rAq1n44WgxYD534L0Hj5pET-phHnR4QHwcFyzJZOorK6hUze-_qgUYGr_8bIzWnl2e01tG0p14Bxqzh9T9E_KRL3pha4swmJaCgYKAacSARASFQHGX2MiMk4b9mImRtTWB0ndtUJHcg0187",
    "expires": 1730979031.550244,
    "token_type": "Bearer",
    "refresh_token": "1//0fbby8SYuk8GdCgYIARAAGA8SNwF-L9IrwHpzOOiV0fxgR050Gmr2KoPI3jC0PxxowFMp8s1_kHzoSbYh6mXJdnotsMTookbc-3M"
}


def alinatk():
    TOKEN_DATA = os.getenv("TOKEN_DATA")
    if not TOKEN_DATA:
        os.environ["TOKEN_DATA"] = json.dumps(YOUTUBE)
