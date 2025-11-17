import sys
import time
import schedule
import subprocess
from datetime import datetime

def run_script(script_name):
    print(f"{datetime.now()} = Running {script_name}")
    result = subprocess.run(['python3', script_name])
    
    if result.returncode != 0:
        print(f"\n{datetime.now()} | Error: {script_name} failed with exit code {result.returncode}")
        print(f"{datetime.now()} | Stopping execution")
        sys.exit(1)
    
    print(f"{datetime.now()} = {script_name} completed successfully\n")
    return result.returncode

jobs = []
jobs.append(schedule.every().day.at("08:56:00").do(run_script, 'fetch_nseindia.py'))
jobs.append(schedule.every().day.at("08:58:00").do(run_script, 'filter_instruments_upstox.py'))
jobs.append(schedule.every().day.at("08:59:00").do(run_script, 'filter_instruments_zerodha.py'))
jobs.append(schedule.every().day.at("09:00:00").do(run_script, 'fetch_historical_data.py'))
jobs.append(schedule.every().day.at("09:02:00").do(run_script, 'calc_safe_volume.py'))
jobs.append(schedule.every().day.at("09:05:00").do(run_script, 'fetch_margin.py'))
jobs.append(schedule.every().day.at("09:06:00").do(run_script, 'calc_margin.py'))
jobs.append(schedule.every().day.at("09:09:00").do(run_script, 'fetch_open_price.py'))
jobs.append(schedule.every().day.at("09:10:00").do(run_script, 'calc_etf_price.py'))
jobs.append(schedule.every().day.at("09:11:00").do(run_script, 'export_volumes_prices.py'))
jobs.append(schedule.every().day.at("09:12:00").do(run_script, 'generate_entry_payload.py'))
jobs.append(schedule.every().day.at("09:13:00").do(run_script, 'place_entry_order_kite.py')) # place_entry_order_zerodha.py
jobs.append(schedule.every().day.at("09:15:20").do(run_script, 'cancel_entry_order.py'))

print(f"{datetime.now()} | Scheduler started. Waiting for scheduled times\n")

while True:
    schedule.run_pending()
    
    if all(job.last_run is not None for job in jobs):
        print(f"{datetime.now()} | All scripts completed successfully. Exiting.")
        sys.exit(0)
    
    time.sleep(1)
