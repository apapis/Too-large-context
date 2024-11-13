import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

def load_file():
    app_url = os.getenv('APP_URL')
    
    if not app_url:
        print("Error: APP_URL not found in .env file")
        return None
    
    url = f"{app_url}"
    
    try:
        print("Downloading file...")
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        test_data = data.get('test-data')
        
        if test_data is None:
            print("Error: 'test-data' section not found in file")
            return None
            
        print("Test data successfully extracted")
        return test_data
        
    except requests.exceptions.RequestException as e:
        print(f"Error while downloading file: {e}")
        return None
        
    except json.JSONDecodeError as e:
        print(f"Error while parsing JSON: {e}")
        return None

def display_test_data(test_data, limit=100):
    if not test_data:
        return
        
    print(f"\nFirst {limit} elements from test-data:")
    for i, item in enumerate(test_data[:limit]):
        print(json.dumps(item, indent=2, ensure_ascii=False))
    
    print(f"\nTotal number of test elements found: {len(test_data)}")

if __name__ == "__main__":
    test_data = load_file()
    
    if test_data:
        display_test_data(test_data)