import asyncio
import logging
import httpx
from fastapi import FastAPI


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Simple WebApp")

# Store ping history
ping_history = []


@app.get("/")
async def home():
    """Simple homepage with ping history"""

    return {"status": "ok"}



async def ping_self():
    """Background task that pings the server every 3 minutes"""
    # Wait a bit for the server to start
    await asyncio.sleep(5)
    
    base_url = "http://127.0.0.1:8000"
    
    async with httpx.AsyncClient() as client:
        while True:
            try:
                await client.get(f"{base_url}/ping", timeout=10.0)
            except Exception as e:
                logger.error(f"❌ Ping failed: {e}")
            await asyncio.sleep(180)


@app.on_event("startup")
async def startup_event():
    """Start background tasks on application startup"""
    asyncio.create_task(ping_self())



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
