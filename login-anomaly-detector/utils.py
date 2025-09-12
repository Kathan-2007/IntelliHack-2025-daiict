import pandas as pd
from datetime import datetime
import os

DATA_FILE = "data/users.csv"

def load_users():
    """Load CSV file into DataFrame"""
    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(f"{DATA_FILE} not found. Please create it first.")
    return pd.read_csv(DATA_FILE)

def log_attempt(username, ip, device_id, location, result):
    """Append login attempt into CSV"""
    df = pd.read_csv(DATA_FILE)
    new_entry = {
        "user_id": len(df) + 1,
        "username": username,
        "password": "-",  # don’t log passwords
        "ip_address": ip,
        "login_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "device_id": device_id,
        "geo_location": location,
        "login_result": result
    }
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
