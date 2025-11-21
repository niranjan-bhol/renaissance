import os
import sys
import requests
import asyncio
import aiohttp
from datetime import datetime
from dotenv import load_dotenv

load_dotenv("../.env.zerodha")

API_KEY = os.getenv("API_KEY")

with open("../access_token_zerodha.txt", "r") as f:
    ACCESS_TOKEN = f.read().strip()

headers = {
        "X-Kite-Version": "3",
        "Authorization": f"token {API_KEY}:{ACCESS_TOKEN}",
    }

def get_orders(api_key, access_token):
    url = "https://api.kite.trade/orders"
    headers = {
        "X-Kite-Version": "3",
        "Authorization": f"token {api_key}:{access_token}",
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["data"]

async def cancel_order(session, api_key, access_token, order_id):
    url = f"https://api.kite.trade/orders/regular/{order_id}"
    async with session.delete(url, headers=headers) as resp:
        await resp.text()

async def cancel_orders_async(api_key, access_token, order_ids):
    async with aiohttp.ClientSession() as session:
        tasks = [cancel_order(session, api_key, access_token, oid) for oid in order_ids]
        await asyncio.gather(*tasks)

def filter_and_cancel(api_key, access_token, orders):
    order_ids = [
        order["order_id"]
        for order in orders
        if "beta" in (order.get("tag") or "") and order.get("status") == "OPEN"
    ]
    if order_ids:
        asyncio.run(cancel_orders_async(api_key, access_token, order_ids))
    print(f"{datetime.now()} - {len(order_ids)} entry orders cancelled")

if __name__ == "__main__":
    try:
        print(f"{datetime.now()} - Cancelling open entry orders")
        orders = get_orders(API_KEY, ACCESS_TOKEN)
        filter_and_cancel(API_KEY, ACCESS_TOKEN, orders)
        print(f"{datetime.now()} - All open entry orders are cancelled")
        sys.exit(0)
    except Exception as e:
        print(f"{datetime.now()} - Error occurred: {e}")
        sys.exit(1)
