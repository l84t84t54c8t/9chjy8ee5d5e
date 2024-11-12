import json
import os

YOUTUBE = {
    "access_token": "ya29.a0AeDClZD3Vy_jA6kCgeM4cEVuIDdiTf-oFjerpLOHynYcfR_ntz5X9zkxfhTd6rOKQFZoq9JGPjvfW7YJ8isGGV4WypFxJy3pCZw1pSUyN7OmnoOGGJ4ayZwrkppY4CC83cxm86uVUnW_QNLPsxnlm9HY0CKPvEyuJQ0oU3NvvcdJFgMUrTQ9aCgYKASoSARASFQHGX2MiGgLkTa0WShLkISJJXysFWA0187",
    "expires": 1731340112.371119,
    "token_type": "Bearer",
    "refresh_token": "1//0fbby8SYuk8GdCgYIARAAGA8SNwF-L9IrwHpzOOiV0fxgR050Gmr2KoPI3jC0PxxowFMp8s1_kHzoSbYh6mXJdnotsMTookbc-3M",
}


def alinatk():
    TOKEN_DATA = os.getenv("TOKEN_DATA")
    if not TOKEN_DATA:
        os.environ["TOKEN_DATA"] = json.dumps(YOUTUBE)
