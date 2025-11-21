import sys
import json
import requests
from pathlib import Path
from datetime import datetime
from config_upstox import UNDERLYING_TOKENS

def get_access_token():
    with open('../access_token_upstox.txt', 'r') as f:
        return f.read().strip()

def fetch_open_prices():
    access_token = get_access_token()
    open_prices = {}
    
    for name, token in UNDERLYING_TOKENS.items():
        url = f'https://api.upstox.com/v3/market-quote/ohlc?instrument_key={token}&interval=1d'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data:
                for key, value in data['data'].items():
                    if 'live_ohlc' in value:
                        open_price = value['live_ohlc']['open']
                        open_prices[name] = open_price
                        break
        else:
            print(f"{datetime.now()} - Failed for {name}: {response.status_code}")
    
    directory = "todays_data"
    Path(directory).mkdir(exist_ok=True)
    output_file = "open_prices.json"
    
    with open(f"{directory}/{output_file}", 'w') as f:
        json.dump(open_prices, f, indent=2)
    
    print(f"{datetime.now()} - Open prices of underlying assets saved to {directory}/{output_file}")

if __name__ == "__main__":
    try:
        print(f"{datetime.now()} - Started open prices fetching")
        fetch_open_prices()
        print(f"{datetime.now()} - Completed fetching & exporting all open prices")
        sys.exit(0)
    except Exception as e:
        print(f"{datetime.now()} - Error occurred: {e}")
        sys.exit(1)
