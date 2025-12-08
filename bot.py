
import logging
import logging.config

from pyromod import listen # type: ignore
from pyrogram.client import Client
from config import BOT_TOKEN, API_ID, API_HASH

# Get logging configurations
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

def main():
    plugins = dict(root="plugins")
    app = Client("FileStore",
                 bot_token=BOT_TOKEN,
                 api_id=API_ID,
                 api_hash=API_HASH,
                 plugins=plugins,
                 workers=100)

    app.run()


if __name__ == "__main__":
    main()