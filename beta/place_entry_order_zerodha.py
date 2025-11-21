import os
import sys
import asyncio
import aiohttp
import pyotp
import requests
from datetime import datetime
from payloads.entry_payload import payloads
from dotenv import load_dotenv

load_dotenv("../.env.zerodha")

KITE_USERNAME = os.getenv("USER_ID")
KITE_PASSWORD = os.getenv("USER_PASSWORD")
TOTP_KEY = os.getenv("TOTP_KEY")

with open("../access_token_zerodha.txt", "r") as f:
    ACCESS_TOKEN = f.read().strip()

url = "https://api.kite.trade/orders/regular"

enctoken = None

def login_kite():
    global enctoken
    session = requests.Session()
    res1 = session.post(
        'https://kite.zerodha.com/api/login',
        data={
            "user_id": KITE_USERNAME,
            "password": KITE_PASSWORD,
            "type": "user_id"
        }
    )
    request_id = res1.json()['data']['request_id']
    res2 = session.post(
        'https://kite.zerodha.com/api/twofa',
        data={
            "request_id": request_id,
            "twofa_value": pyotp.TOTP(TOTP_KEY).now(),
            "user_id": KITE_USERNAME,
            "twofa_type": "totp"
        }
    )
    enctoken = session.cookies.get_dict()['enctoken']
    print(f"{datetime.now()} - Login successful")

async def place_order(session, order):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://kite.zerodha.com/dashboard",
        "Accept-Language": "en-US,en;q=0.6",
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "application/json, text/plain, */*",
        "Authorization": f"enctoken {enctoken}"
    }
    url = 'https://kite.zerodha.com/oms/orders/regular'
    await session.post(url, headers=headers, data=order)

async def main():
    print(f"{datetime.now()} - Waiting for 09:14:00")
    
    login_sleep_target = datetime.now().replace(hour=9, minute=14, second=0, microsecond=0)
    if login_sleep_target > datetime.now():
        await asyncio.sleep((login_sleep_target - datetime.now()).total_seconds())
        
    print(f"{datetime.now()} - Logging in")
    login_kite()
    
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
        tasks = [place_order(session, order) for order in payloads]
        await asyncio.gather(*tasks)
    
    print(f"{datetime.now()} - All entry orders placed")

if __name__ == "__main__":
    try:
        asyncio.run(main())
        sys.exit(0)
    except Exception as e:
        print(f"{datetime.now()} - Error occurred: {e}")
        sys.exit(1)
