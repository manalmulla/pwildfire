# fetchers/firs_fetcher.py
import requests, datetime, pandas as pd
from io import StringIO

FIRMS_BASE = "https://firms.modaps.eosdis.nasa.gov/api/"

def fetch_firms(map_key, dataset="viirs_nrt", bbox=None, days=1):
    """Fetch wildfire hotspots from NASA FIRMS API (CSV format)."""
    end = datetime.datetime.utcnow()
    start = end - datetime.timedelta(days=days)

    params = {
        "map_key": map_key,
        "start": start.strftime("%Y-%m-%d"),
        "end": end.strftime("%Y-%m-%d"),
        "dataset": dataset,
    }
    if bbox:
        params["bbox"] = ",".join(map(str, bbox))

    url = FIRMS_BASE + "area/csv"
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()

    df = pd.read_csv(StringIO(resp.text))
    return df
