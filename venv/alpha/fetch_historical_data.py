import sys
import csv
import requests
from pathlib import Path
from datetime import datetime, date, timedelta
from config_upstox import ETF_TOKENS, UNDERLYING_TOKENS

def get_access_token():
    with open('../access_token_upstox.txt', 'r') as f:
        return f.read().strip()

def fetch_data_chunk(token_encoded, start_date, end_date, headers):
    url = f'https://api.upstox.com/v3/historical-candle/{token_encoded}/minutes/1/{end_date}/{start_date}'
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if 'data' in data and 'candles' in data['data']:
            return data['data']['candles'][::-1]
    else:
        print(f"{datetime.now()} - Error fetching chunk {start_date} to {end_date}: {response.status_code} - {response.text}")
    
    return []

def fetch_data(tokens):
    access_token = get_access_token()
    
    today = date.today()
    total_start_date = today - timedelta(days=182)
    end_date_dt = today - timedelta(days=1)
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    
    directory = "historical_data"
    Path(directory).mkdir(exist_ok=True)
    
    for name, token in tokens.items():
        token_encoded = token.replace('|', '%7C')
        csv_file_path = f'{directory}/{name}.csv'
        all_candles = []
        
        start_date_str = total_start_date.strftime('%Y-%m-%d')
        end_date_str = end_date_dt.strftime('%Y-%m-%d')
        print(f"{datetime.now()} - Fetching {name} data from {start_date_str} to {end_date_str}")
        
        current_start = total_start_date
        
        while current_start <= end_date_dt:
            current_end = min(current_start + timedelta(days=29), end_date_dt)
            
            chunk_start_str = current_start.strftime('%Y-%m-%d')
            chunk_end_str = current_end.strftime('%Y-%m-%d')
            
            chunk_candles = fetch_data_chunk(token_encoded, chunk_start_str, chunk_end_str, headers)
            all_candles.extend(chunk_candles)
            
            current_start = current_end + timedelta(days=1)
        
        with open(csv_file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['datetime', 'open', 'high', 'low', 'close', 'volume', 'null'])
            
            for candle in all_candles:
                writer.writerow(candle)
            
            print(f"{datetime.now()} - Saved {len(all_candles)} rows for {name} to {csv_file_path}")

if __name__ == "__main__":
    try:
        print(f"{datetime.now()} - Started historical data fetching (1 minute timeframe)")
        fetch_data(ETF_TOKENS)
        fetch_data(UNDERLYING_TOKENS)
        print(f"{datetime.now()} - Completed fetching & exporting all data")
        sys.exit(0)
    except Exception as e:
        print(f"{datetime.now()} - Error occurred: {e}")
        sys.exit(1)
