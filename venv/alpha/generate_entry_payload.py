import sys
import json
from pathlib import Path
from datetime import datetime

def generate_entry_payload():
    with open("order_data/volumes.json", 'r') as f:
        volumes = json.load(f)
    
    with open("order_data/prices.json", 'r') as f:
        prices = json.load(f)
    
    payloads = []
    for symbol in volumes.keys():
        quantity = volumes[symbol]["quantity"]
        buy_price = prices[symbol]["buy_price"]
        sell_price = prices[symbol]["sell_price"]
        
        # BUY order
        payloads.append({
            "tradingsymbol": symbol,
            "exchange": "NSE",
            "transaction_type": "BUY",
            "order_type": "LIMIT",
            "quantity": quantity,
            "price": buy_price,
            "product": "MIS",
            "validity": "DAY",
            "tag": "beta"
        })
        
        # SELL order
        payloads.append({
            "tradingsymbol": symbol,
            "exchange": "NSE",
            "transaction_type": "SELL",
            "order_type": "LIMIT",
            "quantity": quantity,
            "price": sell_price,
            "product": "MIS",
            "validity": "DAY",
            "tag": "beta"
        })
    
    output_dir = "payloads"
    Path(output_dir).mkdir(exist_ok=True)
    output_file = "entry_payload.py"
    
    with open(f"{output_dir}/{output_file}", 'w') as f:
        f.write("payloads = [\n")
        for i, payload in enumerate(payloads):
            f.write(json.dumps(payload))
            if i < len(payloads) - 1:
                f.write(",")
            f.write("\n")
        f.write("]\n")
    
    print(f"{datetime.now()} - Generated {len(payloads)} orders & saved to {output_dir}/{output_file}")

if __name__ == "__main__":
    try:
        print(f"{datetime.now()} - Starting entry payload generation")
        generate_entry_payload()
        print(f"{datetime.now()} - Completed entry payload generation successfully")
        sys.exit(0)
    except Exception as e:
        print(f"{datetime.now()} - Error occurred: {e}")
        sys.exit(1)
