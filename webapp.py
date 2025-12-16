import asyncio
import logging
from datetime import datetime

import httpx
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Simple WebApp")

# Store ping history
ping_history = []


@app.get("/", response_class=HTMLResponse)
async def home():
    """Simple homepage with ping history"""
    history_html = ""
    for entry in ping_history[-10:]:  # Show last 10 pings
        history_html += f"<li>{entry['timestamp']} - Status: {entry['status']}</li>"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Simple WebApp</title>

    </head>
    <body>
        <div class="container">
            <h1> FastAPI WebApp</h1>
            <div class="status">
                <strong>Status:</strong> Running<br>
                <strong>Current Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </div>
            
            <div class="endpoint">
                <strong>Available Endpoints:</strong><br>
                • GET / - This page<br>
                • GET /ping - Health check endpoint<br>
                • GET /docs - API documentation
            </div>
            
            <div class="ping-history">
                <h2>Recent Ping History</h2>
                <ul>
                    {history_html if history_html else "<li>No pings yet...</li>"}
                </ul>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content


@app.get("/ping")
async def ping():
    """Health check endpoint"""
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "message": "Pong! 🏓"
    }


async def ping_self():
    """Background task that pings the server every 3 minutes"""
    # Wait a bit for the server to start
    await asyncio.sleep(5)
    
    base_url = "http://127.0.0.1:8000"
    
    async with httpx.AsyncClient() as client:
        while True:
            try:
                logger.info("🔔 Pinging server...")
                response = await client.get(f"{base_url}/ping", timeout=10.0)
                
                ping_entry = {
                    "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "status": f"✅ {response.status_code}"
                }
                ping_history.append(ping_entry)
                
                logger.info(f"✅ Ping successful: {response.json()}")
                
            except Exception as e:
                ping_entry = {
                    "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "status": f"❌ Error: {str(e)[:50]}"
                }
                ping_history.append(ping_entry)
                logger.error(f"❌ Ping failed: {e}")
            
            # Keep only last 50 pings in memory
            if len(ping_history) > 50:
                ping_history.pop(0)
            
            # Wait for 3 minutes (180 seconds)
            await asyncio.sleep(180)


@app.on_event("startup")
async def startup_event():
    """Start background tasks on application startup"""
    asyncio.create_task(ping_self())


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("👋 Shutting down application...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
