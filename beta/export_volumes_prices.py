import sys
import json
from pathlib import Path
from datetime import datetime

output_dir = "order_data"
Path(output_dir).mkdir(exist_ok=True)

def generate_prices():
    input_file = "calculated_predicted_data/predicted_prices.json"
    output_file = "prices.json"
    
    with open(input_file, 'r') as f:
        predicted_data = json.load(f)
    
    prices_data = {}
    
    for symbol, price in predicted_data.items():
        prices_data[symbol] = {
            "buy_price": round(price * 0.995, 2),  # 0.5% less
            "sell_price": round(price * 1.005, 2)  # 0.5% more
        }
    
    with open(f"{output_dir}/{output_file}", 'w') as f:
        json.dump(prices_data, f, indent=2)
    
    print(f"{datetime.now()} - Prices exported successfully to {output_dir}/{output_file}")

def calculate_adjusted_volumes(safe_volumes, prices, discounted_margin):
    total_required_margin = sum(volume * prices[etf]["sell_price"] for etf, volume in safe_volumes.items())
    adjusted = {}
    for etf, volume in safe_volumes.items():
        calc_vol = (volume * discounted_margin) / total_required_margin
        adjusted[etf] = min(int(round(calc_vol)), int(volume))
    return adjusted

def generate_volumes():
    margin_file = "todays_data/margin_processed.json"
    with open(margin_file, 'r') as f:
        margin_data = json.load(f)
    
    discounted_margin = margin_data["discounted_margin"]
    
    volumes_file = "calculated_predicted_data/safe_volumes.json"
    with open(volumes_file, 'r') as f:
        volumes_data = json.load(f)
    
    prices_file = "order_data/prices.json"
    with open(prices_file, 'r') as f:
        prices_data = json.load(f)
    
    output_file = "volumes.json"
    
    safe_volumes = {symbol: data["safe_volume"] for symbol, data in volumes_data.items()}
    
    adjusted_volumes = calculate_adjusted_volumes(safe_volumes, prices_data, discounted_margin)
    
    quantities_data = {}
    for symbol, quantity in adjusted_volumes.items():
        quantities_data[symbol] = {
            "quantity": max(1, quantity)
        }
    
    with open(f"{output_dir}/{output_file}", 'w') as f:
        json.dump(quantities_data, f, indent=2)
    
    print(f"{datetime.now()} - Adjusted volume data calculated and saved to {output_dir}/{output_file}")

if __name__ == "__main__":
    try:
        print(f"{datetime.now()} - Started exporting prices & volumes")
        generate_prices()
        generate_volumes()
        print(f"{datetime.now()} - Completed exporting prices & volumes")
        sys.exit(0)
    except Exception as e:
        print(f"{datetime.now()} - Error occurred: {e}")
        sys.exit(1)
