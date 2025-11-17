import sys
import json
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime

def fetch_margin_data():
    url = "https://zerodha.com/margin-calculator/Equity/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    header_container = soup.find('div', {'id': 'header-container'})
    last_updated = header_container.find('span', {'class': 'modified'}).text.strip()
    
    table = soup.find('table', {'id': 'table', 'class': 'data equity'})
    rows = table.find('tbody').find_all('tr')
    
    margin_list = []
    for row in rows:
        data = {
            'scrip': row.get('data-scrip'),
            'mis': {
                'margin_percent': float(row.get('data-mis_margin')),
                'leverage': float(row.get('data-mis_multiplier'))
            },
            'co': {
                'margin_percent': float(row.get('data-co_margin')),
                'leverage': float(row.get('data-co_multiplier'))
            }
        }
        margin_list.append(data)
    
    margin_data = {
        "timestamp": datetime.now().isoformat(),
        "last_updated": last_updated,
        "total_scrips": len(margin_list),
        "margin_list": margin_list
    }
    
    directory = "todays_data"
    Path(directory).mkdir(exist_ok=True)
    output_file = "margin_list.json"
    
    with open(f"{directory}/{output_file}", 'w') as f:
        json.dump(margin_data, f, indent=2)
    
    print(f"{datetime.now()} - Margin list saved to {directory}/{output_file}")

if __name__ == "__main__":
    try:
        print(f"{datetime.now()} - Started margin list fetching equity")
        fetch_margin_data()
        print(f"{datetime.now()} - Completed fetching & exporting margin list equity")
        sys.exit(0)
    except Exception as e:
        print(f"{datetime.now()} - Error occurred: {e}")
        sys.exit(1)
