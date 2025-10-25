import requests
import pandas as pd
from io import StringIO

def fetch_wildfires(map_key, dataset, bbox=None, days=1):
    """
    Fetches wildfire data from NASA FIRMS (as CSV) and return it as a DataFrame.
    """
    print("[INFO] Fetching live wildfire data from NASA FIRMS...")

    base_url = "https://firms.modaps.eosdis.nasa.gov/api/area/csv"
    area = "world" if bbox is None else ",".join(map(str, bbox))
    url = f"{base_url}/{map_key}/{dataset}/{area}/{days}"

    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        csv_data = StringIO(response.text)
        df = pd.read_csv(csv_data)
        print(f"[INFO] Retrieved {len(df)} fire points from FIRMS.")
        return df
    except Exception as e:
        print("[ERROR] Failed to fetch wildfire data:", e)
        return pd.DataFrame()
