import os
import sys
import json
import pandas as pd
from kiteconnect import KiteConnect
from config_zerodha import FILTER
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(".env.zerodha")

API_KEY = os.getenv("API_KEY")

ACCESS_TOKEN_FILE = "access_token_zerodha.txt"
OUTPUT_FOLDER = "instruments_zerodha"

def init_kite(api_key=API_KEY, access_token_file=ACCESS_TOKEN_FILE):
    with open(f"../{access_token_file}", "r") as f:
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

def filter_symbols(df, symbols_list, folder=OUTPUT_FOLDER):
    folder = ensure_folder(folder)
    json_file = os.path.join(folder, "filtered_symbols.json")
    df_filtered = df[df["tradingsymbol"].isin(symbols_list)]
    
    with open(json_file, "w") as f:
        json.dump(df_filtered.to_dict(orient="records"), f, indent=2)
    
    print(f"{datetime.now()} - Exported filtered symbols to {json_file}")
    return df_filtered

if __name__ == "__main__":
    try:
        print(f"{datetime.now()} - Started instruments filtering")
        kite = init_kite()
        df_instruments = fetch_instruments(kite)
        filter_symbols(df_instruments, FILTER)
        print(f"{datetime.now()} - Completed filtering & exporting instruments")
        sys.exit(0)
    except Exception as e:
        print(f"{datetime.now()} - Error occurred: {e}")
        sys.exit(1)
