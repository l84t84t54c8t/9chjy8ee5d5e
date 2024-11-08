import json
import os

YOUTUBE = {
    "access_token": "ya29.a0AeDClZC5lpbqLqxhI70VdgIlGXphu-hPCUoRhrW57Q78bkcT9d4G2jsJQZynELsNGJsX8A0mmz9xsnsIOdCu_7fLuQXlNvBGF9IAfedD7pAnyBhlOknNyBO871VZ3WRoslquQeSBW0WWSHqO3c9G3h61wQnpzpHf0ZAR68XYfkLoaTbg5A31aCgYKAeoSARASFQHGX2MiUlfn2CIjsGyKBEKRs8VvzQ0187",
    "expires": 1731137232.650379,
    "token_type": "Bearer",
    "refresh_token": "1//0fbby8SYuk8GdCgYIARAAGA8SNwF-L9IrwHpzOOiV0fxgR050Gmr2KoPI3jC0PxxowFMp8s1_kHzoSbYh6mXJdnotsMTookbc-3M"
}


def alinatk():
    TOKEN_DATA = os.getenv("TOKEN_DATA")
    if not TOKEN_DATA:
        os.environ["TOKEN_DATA"] = json.dumps(YOUTUBE)
