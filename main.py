import yaml
from api.wildfire_api import fetch_wildfires
from mapping.map_generator import generate_map
from utils.filters import filter_by_confidence
from alert_manager import check_new_alerts
output_map = "wildfires_map.html"

def main():
    # Load configuration
    with open("config.yaml", "r") as f:
        cfg = yaml.safe_load(f)["firms"]

    map_key = cfg["map_key"]
    dataset = cfg["dataset"]
    bbox = cfg.get("bbox")
    days = cfg.get("days", 1)
    min_conf = cfg.get("min_confidence", 30)
    output_map = cfg.get("output_map", "wildfires_map.html")

    # Fetch data
    df = fetch_wildfires(map_key, dataset, bbox, days)
    if df.empty:
        print("No wildfire data available.")
        return

    # Filter and generate map
    df_filtered = filter_by_confidence(df, min_conf)
    if df_filtered.empty:
        print("No high-confidence wildfires found.")
        return
    check_new_alerts(df_filtered)
    generate_map(df_filtered, output_map)

    print(f"🔥 {len(df_filtered)} wildfires plotted successfully.")

if __name__ == "__main__":
    main()
