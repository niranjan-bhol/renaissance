import os
import sys
import json
import pandas as pd
from pathlib import Path
from datetime import datetime
from config_upstox import ETF_VOLUME_FILES

def fetch_volumes_at_open(file_path):
    if not os.path.exists(file_path):
        return []
    
    df = pd.read_csv(file_path)
    filtered_df = df[df['datetime'].str.contains("09:15:00", na=False)]
    
    filtered_df = filtered_df.tail(60)
    
    return filtered_df['volume'].tolist()

def calculate_average_volume(volumes):
    if not volumes:
        return 0
    
    valid_volumes = [v for v in volumes if v > 0]
    return sum(valid_volumes) / len(valid_volumes) if valid_volumes else 0

def calculate_and_export_safe_volumes():
    volume_data = {}
    
    for etf_name, filename in ETF_VOLUME_FILES.items():
        file_path = os.path.join("historical_data", filename)
        volumes = fetch_volumes_at_open(file_path)
        average_volume = calculate_average_volume(volumes)
        safe_volume = average_volume / 5
        
        volume_data[etf_name] = {
            "average_volume": average_volume,
            "safe_volume": safe_volume
        }
    
    directory = "calculated_predicted_data"
    Path(directory).mkdir(exist_ok=True)
    output_file = "safe_volumes.json"
    
    with open(f"{directory}/{output_file}", 'w') as f:
        json.dump(volume_data, f, indent=2)
    
    print(f"{datetime.now()} - Safe volumes saved to {directory}/{output_file}")
    
    return volume_data

if __name__ == "__main__":
    try:
        print(f"{datetime.now()} - Started safe volume calculation")
        calculate_and_export_safe_volumes()
        print(f"{datetime.now()} - Completed calculating & exporting safe volumes")
        sys.exit(0)
    except Exception as e:
        print(f"{datetime.now()} - Error occurred: {e}")
        sys.exit(1)
