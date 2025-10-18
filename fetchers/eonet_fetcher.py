# fetchers/eonet_fetcher.py
import requests, datetime, pandas as pd

EONET_BASE = "https://eonet.gsfc.nasa.gov/api/v3/events"

def fetch_eonet_wildfires(days=1):
    """Fetch recent wildfire events from NASA EONET API."""
    params = {"status": "open", "category": "wildfires", "limit": 1000}
    resp = requests.get(EONET_BASE, params=params, timeout=20)
    resp.raise_for_status()

    data = resp.json()
    events = []
    for ev in data.get("events", []):
        geom = ev.get("geometry", [])
        if not geom:
            continue
        latest = geom[-1]
        coords = latest.get("coordinates")
        if not coords:
            continue
        events.append({
            "id": ev.get("id"),
            "title": ev.get("title"),
            "date": latest.get("date"),
            "lat": coords[1],
            "lon": coords[0],
            "link": ev.get("links")[0].get("href") if ev.get("links") else None
        })
    return pd.DataFrame(events)
