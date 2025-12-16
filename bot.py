import asyncio
import logging

from pyrogram.client import Client
from pyromod import listen

from config import API_HASH, API_ID, BOT_TOKEN
from webapp import start_webapp

# Get logging configurations
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


class Bot(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def start(self, *args, **kwargs):
        await super().start(*args, **kwargs)
        asyncio.create_task(start_webapp())

    async def stop(self, *args, **kwargs):
        await super().stop(*args, **kwargs)



def main():
    plugins = dict(root="plugins")
    app = Bot(
        "FileStore",
        bot_token=BOT_TOKEN,
        api_id=API_ID,
        api_hash=API_HASH,
        plugins=plugins,
        workers=100,
    )

    app.run()


if __name__ == "__main__":
    main()
