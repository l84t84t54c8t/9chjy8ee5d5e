import json
import os

YOUTUBE = {
    "access_token": "ya29.a0AeDClZDQhh5OkybttkJhyNhmYSwmYlld9tCwMCPy0AVoeOyst-2mmo0a1SECNxS1NLtRk0xRCV_w4OzBKL_hiblx394giiiLDruNP1peQRoByDvNZ-BAMQYO3Y1K4Vf5QJViVtu3X78nfAI2Aiqtkc24MpZISlni2KNO-x1rJO0ouw2Q168haCgYKAR0SARASFQHGX2MiIU8iFgrnoOPHreCgGFJSuA0187",
    "expires": 1730512504.726014,
    "token_type": "Bearer",
    "refresh_token": "1//0fbby8SYuk8GdCgYIARAAGA8SNwF-L9IrwHpzOOiV0fxgR050Gmr2KoPI3jC0PxxowFMp8s1_kHzoSbYh6mXJdnotsMTookbc-3M",
}


def alinabot():
    TOKEN_DATA = os.getenv("TOKEN_DATA")
    if not TOKEN_DATA:
        os.environ["TOKEN_DATA"] = json.dumps(YOUTUBE)
