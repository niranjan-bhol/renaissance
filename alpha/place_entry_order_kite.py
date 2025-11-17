import os
import sys
import asyncio
import aiohttp
from datetime import datetime
from payloads.entry_payload import payloads
from dotenv import load_dotenv

load_dotenv("../.env.zerodha")

API_KEY = os.getenv("API_KEY")

with open("../access_token_zerodha.txt", "r") as f:
    ACCESS_TOKEN = f.read().strip()

url = "https://api.kite.trade/orders/regular"

headers = {
    "X-Kite-Version": "3",
    "Authorization": f"token {API_KEY}:{ACCESS_TOKEN}"
}

async def post_order(session, payload):
    await session.post(url, headers=headers, data=payload)

async def main():
    print(f"{datetime.now()} - Waiting for 09:15:00")
    
    sleep_target = datetime.now().replace(hour=9, minute=14, second=50, microsecond=0)
    if sleep_target > datetime.now():
        await asyncio.sleep((sleep_target - datetime.now()).total_seconds())
    
    print(f"{datetime.now()} - Starting busy wait loop for 09:15:00")
    
    print_target = datetime.now().replace(hour=9, minute=14, second=59, microsecond=0)
    while datetime.now() < print_target:
        pass
    
    print(f"{datetime.now()} - Placing entry orders")
    
    target = datetime.now().replace(hour=9, minute=15, second=0, microsecond=0)
    while datetime.now() < target:
        pass
    
    async with aiohttp.ClientSession() as session:
        tasks = [post_order(session, payload) for payload in payloads]
        await asyncio.gather(*tasks)
    
    print(f"{datetime.now()} - All entry orders placed")

if __name__ == "__main__":
    try:
        asyncio.run(main())
        sys.exit(0)
    except Exception as e:
        print(f"{datetime.now()} - Error occurred: {e}")
        sys.exit(1)
