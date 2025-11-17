import os
import sys
import pyotp
import requests
from urllib.parse import urlparse, parse_qs, quote
from playwright.sync_api import sync_playwright
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(".env.upstox")

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
TOTP_KEY = os.getenv("TOTP_KEY")
MOBILE_NO = os.getenv("MOBILE_NO")
PIN = os.getenv("PIN")

ACCESS_TOKEN_FILE = "access_token_upstox.txt"
REDIRECT_URL = "https://127.0.0.1:5000/"

AUTH_URL = (
    f"https://api.upstox.com/v2/login/authorization/dialog?"
    f"response_type=code&client_id={API_KEY}&redirect_uri={quote(REDIRECT_URL, safe='')}"
)

def get_access_token(code):
    response = requests.post(
        "https://api.upstox.com/v2/login/authorization/token",
        headers={
            "accept": "application/json",
            "Api-Version": "2.0",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "code": code,
            "client_id": API_KEY,
            "client_secret": API_SECRET,
            "redirect_uri": REDIRECT_URL,
            "grant_type": "authorization_code",
        },
    )
    return response.json()["access_token"]

def save_access_token(token):
    with open(ACCESS_TOKEN_FILE, "w") as f:
        f.write(token)

def login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.set_default_timeout(30000)
        
        with page.expect_request(f"*{REDIRECT_URL}?code*") as req:
            page.goto(AUTH_URL)
            page.locator("#mobileNum").fill(MOBILE_NO)
            page.get_by_role("button", name="Get OTP").click()
            page.locator("#otpNum").fill(pyotp.TOTP(TOTP_KEY).now())
            page.get_by_role("button", name="Continue").click()
            page.get_by_label("Enter 6-digit PIN").fill(PIN)
            page.get_by_role("button", name="Continue").click()
            page.wait_for_load_state()
        
        code = parse_qs(urlparse(req.value.url).query)["code"][0]
        browser.close()
    
    token = get_access_token(code)
    save_access_token(token)
    return token

if __name__ == "__main__":
    try:
        print(f"{datetime.now()} - Fetching access token")
        token = login()
        print(f"{datetime.now()} - Access token fetched and stored successfully")
        sys.exit(0)
    except Exception as e:
        print(f"{datetime.now()} - Error occurred: {e}")
        sys.exit(1)
