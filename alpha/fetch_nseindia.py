import sys
import json
import time
import requests
from pathlib import Path
from datetime import datetime
from config import NSEINDIA_SYMBOLS

def fetch_nse_data():
    session = requests.Session()
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'
    }
    
    for symbol in NSEINDIA_SYMBOLS:
        print(f"{datetime.now()} - Fetching data for {symbol}")
        
        headers['Referer'] = f'https://www.nseindia.com/get-quotes/equity?symbol={symbol}'
        
        session.get('https://www.nseindia.com/', headers=headers)
        session.get(f'https://www.nseindia.com/get-quotes/equity?symbol={symbol}', headers=headers)
        
        combined_data = {}
        
        # URL 1: Equity Meta Info
        url1 = f"https://www.nseindia.com/api/equity-meta-info?symbol={symbol}"
        response1 = session.get(url1, headers=headers, timeout=10)
        if response1.status_code == 200:
            combined_data['equity_meta_info'] = response1.json()
        else:
            print(f"{datetime.now()} - Failed for {symbol}: {response1.status_code}")
        time.sleep(2)
        
        # URL 2: Quote Equity
        url2 = f"https://www.nseindia.com/api/quote-equity?symbol={symbol}"
        response2 = session.get(url2, headers=headers, timeout=10)
        if response2.status_code == 200:
            combined_data['quote_equity'] = response2.json()
        else:
            print(f"{datetime.now()} - Failed for {symbol}: {response2.status_code}")
        time.sleep(2)
        
        # URL 3: Trade Info Section
        url3 = f"https://www.nseindia.com/api/quote-equity?symbol={symbol}&section=trade_info"
        response3 = session.get(url3, headers=headers, timeout=10)
        if response3.status_code == 200:
            combined_data['trade_info'] = response3.json()
        else:
            print(f"{datetime.now()} - Failed for {symbol}: {response3.status_code}")
        time.sleep(2)
        
        # Save to file
        directory = "nseindia_data"
        Path(directory).mkdir(exist_ok=True)
        output_file = f"{symbol}.json"
        
        with open(f"{directory}/{output_file}", 'w') as f:
            json.dump(combined_data, f, indent=2)
        
        print(f"{datetime.now()} - Saved data to {directory}/{output_file}")

if __name__ == "__main__":
    try:
        print(f"{datetime.now()} - Started nseindia data fetching")
        fetch_nse_data()
        print(f"{datetime.now()} - Completed fetching & exporting nseindia data")
        sys.exit(0)
    except Exception as e:
        print(f"{datetime.now()} - Error occurred: {e}")
        sys.exit(1)
