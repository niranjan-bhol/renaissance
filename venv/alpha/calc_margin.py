import sys
import json
from pathlib import Path
from datetime import datetime

def calculate_margins():
    with open('todays_data/margin_raw.json', 'r') as f:
        margin_data = json.load(f)
    
    net = margin_data['margins']['equity']['net']
    
    available_margin = net
    leveraged_margin = net * 5
    discounted_margin = leveraged_margin * 0.95  # 5% discount
    
    processed_data = {
        "available_margin": available_margin,
        "leveraged_margin": leveraged_margin,
        "discounted_margin": discounted_margin
    }
    
    directory = "todays_data"
    Path(directory).mkdir(exist_ok=True)
    output_file = "margin_processed.json"
    
    with open(f"{directory}/{output_file}", 'w') as f:
        json.dump(processed_data, f, indent=2)
    
    print(f"{datetime.now()} - Calculated margins saved to {directory}/{output_file}")

if __name__ == "__main__":
    try:
        print(f"{datetime.now()} - Started margin calculation")
        calculate_margins()
        print(f"{datetime.now()} - Completed calculating & exporting margin data")
        sys.exit(0)
    except Exception as e:
        print(f"{datetime.now()} - Error occurred: {e}")
        sys.exit(1)
