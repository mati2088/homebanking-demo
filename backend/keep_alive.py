import asyncio
import httpx
from datetime import datetime

async def keep_alive():
    """Background task to ping the service every 10 minutes to prevent sleep"""
    url = "https://homebanking-demo.onrender.com/docs"
    
    while True:
        try:
            await asyncio.sleep(600)  # 10 minutes
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=10.0)
                print(f"[{datetime.now()}] Keep-alive ping: {response.status_code}")
        except Exception as e:
            print(f"[{datetime.now()}] Keep-alive error: {e}")
