import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", None)
BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
DB_CHANNEL_ID = os.environ.get("DB_CHANNEL_ID", "")
IS_PRIVATE = os.environ.get("IS_PRIVATE", False)  # any input is ok But True preferable
OWNER_ID = os.environ.get("OWNER_ID")

if OWNER_ID.isdigit():
    OWNER_ID = int(OWNER_ID)

PROTECT_CONTENT = True
UPDATE_CHANNEL = os.environ.get("UPDATE_CHANNEL", "")
AUTH_USERS = (
    list(int(i) for i in os.environ.get("AUTH_USERS", "").split(" "))
    if os.environ.get("AUTH_USERS")
    else []
)

if OWNER_ID not in AUTH_USERS:
    AUTH_USERS.append(OWNER_ID)

MONGO_URL= os.environ.get("MONGO_URL", "mongodb://localhost:27017/")

if UPDATE_CHANNEL.isdigit():
    UPDATE_CHANNEL = int(UPDATE_CHANNEL)

if DB_CHANNEL_ID.isdigit():
    DB_CHANNEL_ID = int(DB_CHANNEL_ID)
