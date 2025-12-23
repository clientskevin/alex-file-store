import asyncio
import logging

import httpx
from flask import Flask, jsonify

from config import WEB_URL

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/")
def home():
    """Simple homepage with ping history"""
    return jsonify({"status": "ok"})


async def ping_self():
    """Background task that pings the server every 3 minutes"""
    # Wait a bit for the server to start
    await asyncio.sleep(5)
    
    base_url = WEB_URL or "http://127.0.0.1:8000"
    
    async with httpx.AsyncClient() as client:
        while True:
            try:
                await client.get(f"{base_url}/", timeout=10.0)
            except Exception as e:
                logger.error(f"❌ Ping failed: {e}")
            await asyncio.sleep(180)

async def start_webapp():
    """Start Flask app in a separate thread and ping task in asyncio"""
    if not WEB_URL:
        return
    import threading

    # Start Flask in a daemon thread so it doesn't block asyncio
    flask_thread = threading.Thread(
        target=lambda: app.run(host="0.0.0.0", port=8000, debug=False, use_reloader=False),
        daemon=True
    )
    flask_thread.start()
    
    # Start the ping task in asyncio (non-blocking)
    asyncio.create_task(ping_self())
