import os
import sys
import json
import pandas as pd
from pathlib import Path
from datetime import datetime, time
from config_upstox import PAIRS

HISTORICAL_FOLDER = "historical_data"
TODAYS_FOLDER = "todays_data"
PREDICTED_FOLDER = "calculated_predicted_data"

def load_historical(etf_file, underlying_file):
    etf_path = os.path.join(HISTORICAL_FOLDER, etf_file)
    underlying_path = os.path.join(HISTORICAL_FOLDER, underlying_file)
    
    etf_df = pd.read_csv(etf_path, parse_dates=["datetime"])
    underlying_df = pd.read_csv(underlying_path, parse_dates=["datetime"])
    
    """
    etf_df = etf_df[~etf_df["datetime"].dt.strftime("%H:%M:%S").str.contains("09:15:00")]
    underlying_df = underlying_df[~underlying_df["datetime"].dt.strftime("%H:%M:%S").str.contains("09:15:00")]
    """
    
    etf_df = etf_df[~((etf_df["datetime"].dt.time >= time(9, 15, 0)) & 
                      (etf_df["datetime"].dt.time <= time(10, 0, 0)))]
    underlying_df = underlying_df[~((underlying_df["datetime"].dt.time >= time(9, 15, 0)) & 
                                    (underlying_df["datetime"].dt.time <= time(10, 0, 0)))]
    
    etf_df = etf_df[~((etf_df["datetime"].dt.time >= time(14, 40, 0)) & 
                      (etf_df["datetime"].dt.time <= time(15, 30, 0)))]
    underlying_df = underlying_df[~((underlying_df["datetime"].dt.time >= time(14, 40, 0)) & 
                                    (underlying_df["datetime"].dt.time <= time(15, 30, 0)))]
    
    return etf_df, underlying_df

def load_todays_open():
    file = "open_prices.json"
    path = os.path.join(TODAYS_FOLDER, file)
    
    with open(path, "r") as f:
        return json.load(f)

def predict_open_ratio(etf_df, underlying_df, underlying_open_price, window=1400):
    merged = pd.merge(
        underlying_df[["datetime", "close"]], 
        etf_df[["datetime", "close"]],
        on="datetime",
        suffixes=("_underlying", "_etf"),
        how="inner"
    )
    
    merged["ratio"] = merged["close_underlying"] / merged["close_etf"]
    avg_ratio = merged["ratio"].tail(window).mean()
    
    return float(underlying_open_price / avg_ratio)

def save_predictions(predictions):
    Path(PREDICTED_FOLDER).mkdir(exist_ok=True)
    output_file = "predicted_prices.json"
    
    with open(f"{PREDICTED_FOLDER}/{output_file}", 'w') as f:
        json.dump(predictions, f, indent=2)
    
    print(f"{datetime.now()} - Saved all calculated/predicted open prices for ETFs to {PREDICTED_FOLDER}/{output_file}")

if __name__ == "__main__":
    try:
        print(f"{datetime.now()} - Started fair price calculation")
        
        todays_open = load_todays_open()
        predictions = {}
        
        for etf, underlying in PAIRS.items():
            etf_df, underlying_df = load_historical(f"{etf}.csv", f"{underlying}.csv")
            predictions[etf] = predict_open_ratio(
                etf_df, underlying_df, todays_open[underlying], window=1400
            )
        
        save_predictions(predictions)
        print(f"{datetime.now()} - Completed calculating & exporting fair prices")
        sys.exit(0)
    
    except Exception as e:
        print(f"{datetime.now()} - Error occurred: {e}")
        sys.exit(1)
