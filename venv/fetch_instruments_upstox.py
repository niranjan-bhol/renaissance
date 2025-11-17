import sys
import json
import gzip
import requests
from pathlib import Path
from datetime import datetime

def download_instruments():
    urls = [
        "https://assets.upstox.com/market-quote/instruments/exchange/complete.json.gz",
        "https://assets.upstox.com/market-quote/instruments/exchange/NSE.json.gz",
        "https://assets.upstox.com/market-quote/instruments/exchange/BSE.json.gz",
        "https://assets.upstox.com/market-quote/instruments/exchange/MCX.json.gz",
        "https://assets.upstox.com/market-quote/instruments/exchange/NSE_MIS.json.gz",
        "https://assets.upstox.com/market-quote/instruments/exchange/BSE_MIS.json.gz"
    ]
    
    directory = "instruments_upstox"
    Path(directory).mkdir(exist_ok=True)
    
    for url in urls:
        filename = url.split('/')[-1].replace('.gz', '')
        response = requests.get(url)
        data = gzip.decompress(response.content)
        instruments = json.loads(data.decode('utf-8'))
        
        with open(f"{directory}/{filename}", 'w') as f:
            json.dump(instruments, f, indent=2)
        
        print(f"{datetime.now()} - Downloaded {len(instruments)} instruments to {directory}/{filename}")

if __name__ == "__main__":
    try:
        print(f"{datetime.now()} - Started instruments fetching")
        download_instruments()
        print(f"{datetime.now()} - Completed fetching & exporting instruments")
        sys.exit(0)
    except Exception as e:
        print(f"{datetime.now()} - Error occurred: {e}")
        sys.exit(1)
