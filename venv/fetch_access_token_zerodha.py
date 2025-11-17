import os
import sys
import pyotp
import requests
from kiteconnect import KiteConnect
from urllib.parse import urlparse, parse_qs
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(".env.zerodha")

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
USER_ID = os.getenv("USER_ID")
USER_PASSWORD = os.getenv("USER_PASSWORD")
TOTP_KEY = os.getenv("TOTP_KEY")

ACCESS_TOKEN_FILE = "access_token_zerodha.txt"

def get_request_token(session):
    login_url = f"https://kite.trade/connect/login?v=3&api_key={API_KEY}"
    session.get(url=login_url)
    
    response = session.post(
        url="https://kite.zerodha.com/api/login",
        data={"user_id": USER_ID, "password": USER_PASSWORD}
    )
    resp_dict = response.json()
    
    session.post(
        url="https://kite.zerodha.com/api/twofa",
        data={
            "user_id": USER_ID,
            "request_id": resp_dict["data"]["request_id"],
            "twofa_value": pyotp.TOTP(TOTP_KEY).now()
        }
    )
    
    final_url = f"{login_url}&skip_session=true"
    redirected_url = session.get(final_url, allow_redirects=True).url
    request_token = parse_qs(urlparse(redirected_url).query)["request_token"][0]
    
    return request_token

def save_access_token(token):
    with open(ACCESS_TOKEN_FILE, "w") as f:
        f.write(token)

def login():
    session = requests.Session()
    request_token = get_request_token(session)
    
    kite = KiteConnect(api_key=API_KEY)
    data = kite.generate_session(request_token, api_secret=API_SECRET)
    kite.set_access_token(data["access_token"])
    
    save_access_token(data["access_token"])
    
    return kite

if __name__ == "__main__":
    try:
        print(f"{datetime.now()} - Fetching access token")
        kite = login()
        print(f"{datetime.now()} - Access token fetched and stored successfully")
        sys.exit(0)
    except Exception as e:
        print(f"{datetime.now()} - Error occurred: {e}")
        sys.exit(1)
