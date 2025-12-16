
import asyncio
import logging
import logging.config

from pyrogram.client import Client
from pyromod import listen  # type: ignore

from config import API_HASH, API_ID, BOT_TOKEN

# Get logging configurations
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


async def start_webapp():
    """Start the FastAPI webapp using uvicorn in the same event loop"""
    import uvicorn

    from webapp import app
    
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


async def start_bot():
    """Start the Pyrogram bot"""
    plugins = dict(root="plugins")
    app = Client(
        "FileStore",
        bot_token=BOT_TOKEN,
        api_id=API_ID,
        api_hash=API_HASH,
        plugins=plugins,
        workers=100
    )
    
    await app.start()
    print("✅ Bot started successfully!")
    await asyncio.Event().wait()  # Keep running forever


async def main():
    """Run both webapp and bot concurrently in the same event loop"""
    print("🚀 Starting FastAPI webapp and Pyrogram bot...")
    
    # Run both tasks concurrently
    await asyncio.gather(
        start_webapp(),
        start_bot(),
        return_exceptions=True
    )


if __name__ == "__main__":
    asyncio.run(main())