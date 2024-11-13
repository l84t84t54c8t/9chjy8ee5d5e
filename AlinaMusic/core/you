import json
import os

YOUTUBE = {
    "access_token": "ya29.a0AeDClZApUX8aDi-ZZa4c-1DbeNsAHtBpEBiV53GpaUt-sAALmcP-5fyHzLFYLQ58vAw_VLtEIdd8iMAe6pxtmS2WLIqfecYSwYVMGD6ZZrPmz2KQBbHFZkg-Q3eY595lCUSl42_uw4iHMjOMG6RnY9ZBXNPMlrZvPH9rLpQBcDqtxi2v2BEBaCgYKAfUSARASFQHGX2MiJh7MdOQGiCBpH89itiJTuQ0187",
    "expires": 1731498856.498369,
    "token_type": "Bearer",
    "refresh_token": "1//0fbby8SYuk8GdCgYIARAAGA8SNwF-L9IrwHpzOOiV0fxgR050Gmr2KoPI3jC0PxxowFMp8s1_kHzoSbYh6mXJdnotsMTookbc-3M",
}


def alinatk():
    TOKEN_DATA = os.getenv("TOKEN_DATA")
    if not TOKEN_DATA:
        os.environ["TOKEN_DATA"] = json.dumps(YOUTUBE)
