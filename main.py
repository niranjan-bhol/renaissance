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
jobs.append(schedule.every().day.at("08:50:00").do(run_script, 'fetch_access_token_upstox.py'))
jobs.append(schedule.every().day.at("08:51:00").do(run_script, 'fetch_access_token_zerodha.py'))
jobs.append(schedule.every().day.at("08:52:00").do(run_script, 'fetch_instruments_upstox.py'))
jobs.append(schedule.every().day.at("08:53:00").do(run_script, 'fetch_instruments_zerodha.py'))
jobs.append(schedule.every().day.at("08:54:00").do(run_script, 'fetch_margin_list.py'))

print(f"{datetime.now()} | Scheduler started. Waiting for scheduled times\n")

while True:
    schedule.run_pending()
    
    if all(job.last_run is not None for job in jobs):
        print(f"{datetime.now()} | All scripts completed successfully. Exiting.")
        sys.exit(0)
    
    time.sleep(1)
