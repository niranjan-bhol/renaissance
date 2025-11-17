import os
import sys
import json
import pandas as pd
from kiteconnect import KiteConnect
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(".env.zerodha")

API_KEY = os.getenv("API_KEY")

ACCESS_TOKEN_FILE = "access_token_zerodha.txt"
OUTPUT_FOLDER = "instruments_zerodha"

def init_kite(api_key=API_KEY, access_token_file=ACCESS_TOKEN_FILE):
    with open(access_token_file, "r") as f:
        access_token = f.read().strip()
    kite = KiteConnect(api_key=api_key)
    kite.set_access_token(access_token)
    return kite

def fetch_instruments(kite):
    instruments = kite.instruments()
    for item in instruments:
        expiry = item.get("expiry")
        if expiry and not isinstance(expiry, str):
            item["expiry"] = expiry.strftime("%Y-%m-%d")
    return pd.DataFrame(instruments)

def ensure_folder(folder_name=OUTPUT_FOLDER):
    Path(folder_name).mkdir(exist_ok=True)
    return folder_name

def save_all_columns(df, folder=OUTPUT_FOLDER):
    folder = ensure_folder(folder)
    csv_file = os.path.join(folder, "zerodha_instruments_full.csv")
    json_file = os.path.join(folder, "zerodha_instruments_full.json")
    
    df.to_csv(csv_file, index=False)
    
    with open(json_file, "w") as f:
        json.dump(df.to_dict(orient="records"), f, indent=2)
    
    print(f"{datetime.now()} - Exported all columns to {csv_file} and {json_file}")
    return df

def save_selected_columns(df, folder=OUTPUT_FOLDER):
    csv_file = os.path.join(folder, "zerodha_instruments.csv")
    json_file = os.path.join(folder, "zerodha_instruments.json")
    df_small = df[["instrument_token", "exchange_token", "tradingsymbol", "exchange"]]
    
    df_small.to_csv(csv_file, index=False)
    
    with open(json_file, "w") as f:
        json.dump(df_small.to_dict(orient="records"), f, indent=2)
    
    print(f"{datetime.now()} - Exported selected columns to {csv_file} and {json_file}")
    return df_small

if __name__ == "__main__":
    try:
        print(f"{datetime.now()} - Started instrument data fetching")
        kite = init_kite()
        df_instruments = fetch_instruments(kite)
        save_all_columns(df_instruments)
        save_selected_columns(df_instruments)
        print(f"{datetime.now()} - Completed fetching & exporting instruments data")
        sys.exit(0)
    except Exception as e:
        print(f"{datetime.now()} - Error occurred: {e}")
        sys.exit(1)
