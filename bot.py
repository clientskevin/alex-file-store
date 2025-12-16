
import logging
import logging.config
import threading
import time

from pyrogram.client import Client
from pyromod import listen  # type: ignore

from config import API_HASH, API_ID, BOT_TOKEN

# Get logging configurations
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

def start_webapp():
    """Start the FastAPI webapp in a separate thread"""
    import asyncio

    import uvicorn

    from webapp import app

    # Create a new event loop for this thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # Run uvicorn server
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

def main():
    # Start webapp in background thread
    webapp_thread = threading.Thread(target=start_webapp, daemon=True)
    webapp_thread.start()
    

    time.sleep(3)


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