import sys
import json
from pathlib import Path
from datetime import datetime
from config_upstox import FILTER

def filter_instruments():
    with open('../instruments_upstox/complete.json', 'r') as f:
        instruments = json.load(f)
    
    filtered_instruments = []
    
    for filter_term in FILTER:
        for instrument in instruments:
            if instrument.get('trading_symbol') == filter_term:
                filtered_instruments.append(instrument)
    
    directory = "instruments_upstox"
    Path(directory).mkdir(exist_ok=True)
    filename = "filtered_instruments.json"
    
    with open(f"{directory}/{filename}", 'w') as f:
        json.dump(filtered_instruments, f, indent=2)
    
    print(f"{datetime.now()} - Filtered {len(filtered_instruments)} instruments to {directory}/{filename}")

if __name__ == "__main__":
    try:
        print(f"{datetime.now()} - Started instruments filtering")
        filter_instruments()
        print(f"{datetime.now()} - Completed filtering & exporting instruments")
        sys.exit(0)
    except Exception as e:
        print(f"{datetime.now()} - Error occurred: {e}")
        sys.exit(1)
