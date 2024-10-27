import json
import os

YOUTUBE = {
    "access_token": "ya29.a0AeDClZAMpHtY48rDo0TGIkfSQfhW20PgR-drAYYX5cSCIdBsgXJ8XLMHPP5PDiiBs-Hj-OxbyYe6PwF_n0m23b9775vCD7kWhA6CSfiYbZcJ50s8rTTKDKwuDPPy_NhrYQfRsian9BIYXentbeuQdmZNm084sQFgk5bswbPbZac5kpFEO2ERaCgYKAZUSARASFQHGX2MiEv_pLZ7yfwd2yC4aJAVIsA0187",
    "expires": 1730003253.679578,
    "refresh_token": "1//0fbby8SYuk8GdCgYIARAAGA8SNwF-L9IrwHpzOOiV0fxgR050Gmr2KoPI3jC0PxxowFMp8s1_kHzoSbYh6mXJdnotsMTookbc-3M",
    "token_type": "Bearer",
}


def alinabot():
    TOKEN_DATA = os.getenv("TOKEN_DATA")
    if not TOKEN_DATA:
        os.environ["TOKEN_DATA"] = json.dumps(YOUTUBE)
