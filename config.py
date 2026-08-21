# © 2026 DragonByte Network | @flexyy

from os import getenv
import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(getenv("API_ID", 0))
API_HASH = getenv("API_HASH", "")
BOT_TOKEN = getenv("BOT_TOKEN", "")
OWNER_ID = int(getenv("OWNER_ID", 8681820826))
MONGO_URL = getenv("MONGO_URL", "")
TMDB_API_KEY = getenv("TMDB_API_KEY", "")

AUTH_CHANNEL = int(getenv("AUTH_CHANNEL", 0) or 0)
FSUB = getenv("FSUB", "False").lower() in ("true", "1", "yes")
LOGGER_GROUP_ID = int(getenv("LOGGER_GROUP_ID", -1003913785429))

SUPPORT_GROUP = os.environ.get("SUPPORT_GROUP", "DragonByte_Network")
UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", "DragonByte_Network")
SUPPORT_CHAT_LINK = "https://t.me/+CZCfHr3AHKUwNTJk"

IMG = [
    "https://i.postimg.cc/C5S3QfJc/1d0300acfabedc863eab4afef882d1b7.jpg",
    "https://i.postimg.cc/SRkBvzVD/2befbd2f3bd0f85603fc5d5aebe6385e.jpg",
    "https://i.postimg.cc/4ysDShBG/3d97e409b1f9d6c652b348d130f80053.jpg",
    "https://i.postimg.cc/0jPTBJZC/488a8f7133e3805d899e3e5e31d81f77.jpg",
    "https://i.postimg.cc/rsMBPtgG/7f6368d685a6aba19c587c83f159e032.jpg",
    "https://i.postimg.cc/QCh2yWS2/8f17c75bae2151dcd8d9f3df9b9ed852.jpg",
    "https://i.postimg.cc/MHqCFjt3/99006e210025b0f324f8427bf523b429.jpg",
    "https://i.postimg.cc/fyDGr05H/9a74c37232588ad6dabe789bb7c18360.jpg",
    "https://i.postimg.cc/PJTgR82s/a68457b89722ece1f5de6b548423c306.jpg",
    "https://i.postimg.cc/tJpKMVD8/a88a53762fcbe485239881542fa95532.jpg",
    "https://i.postimg.cc/Y0M5sm8Z/a925728b14e92382e52ffff3225680d0.jpg",
    "https://i.postimg.cc/rsMBPtQk/bb2f2fda96cac9c77e76538ff8381fd6.jpg",
    "https://i.postimg.cc/prRw6nqt/c721f620e5a6092f3afbcdc91b01f917.jpg",
    "https://i.postimg.cc/rsMBPtQ2/ddca5cc9c19d9f4ea8452f7b054a3809.jpg",
]
