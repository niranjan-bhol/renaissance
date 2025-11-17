import os
import sys
import json
from kiteconnect import KiteConnect
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv("../.env.zerodha")

API_KEY = os.getenv("API_KEY")

def load_access_token():
    with open("../access_token_zerodha.txt", "r") as f:
        return f.read().strip()

def fetch_margins():
    access_token = load_access_token()
    kite = KiteConnect(api_key=API_KEY)
    kite.set_access_token(access_token)
    margins = kite.margins()
    return margins

def save_margins_to_json(margins):
    directory = "todays_data"
    Path(directory).mkdir(exist_ok=True)
    output_file = "margin_raw.json"
    
    data_with_timestamp = {
        "timestamp": datetime.now().isoformat(),
        "margins": margins
    }
    
    with open(f"{directory}/{output_file}", 'w') as f:
        json.dump(data_with_timestamp, f, indent=2)
    
    print(f"{datetime.now()} - Margin data saved to {directory}/{output_file}")

if __name__ == "__main__":
    try:
        print(f"{datetime.now()} - Started margin data fetching")
        margins = fetch_margins()
        if margins:
            save_margins_to_json(margins)
        print(f"{datetime.now()} - Completed fetching & exporting margin data")
        sys.exit(0)
    except Exception as e:
        print(f"{datetime.now()} - Error occurred: {e}")
        sys.exit(1)
