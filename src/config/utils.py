import requests
from time import sleep

def fetch_data_with_retry(url, retries=3, delay=5):
    """Fetch data from API with retry logic."""
    for _ in range(retries):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error fetching data: {e}")
        sleep(delay)
    raise Exception(f"Failed to fetch data from {url} after retries.")

def send_transaction_with_retry(transaction_fn, retries=3, delay=10):
    """Send transaction with retry logic."""
    for _ in range(retries):
        try:
            transaction_fn()
            return True
        except Exception as e:
            print(f"Transaction failed: {e}")
        sleep(delay)
    raise Exception("Transaction failed after retries.")
