import folium
import pandas as pd

def generate_map(df, output_file="wildfires_map.html"):
    if df.empty:
        print("[WARN] No wildfire data available to map.")
        return

    m = folium.Map(
    location=[0, 0],
    zoom_start=1,
    worldCopyJump=False,               
)

    for _, row in df.iterrows():
        lat, lon = row.get("latitude"), row.get("longitude")
        if pd.isna(lat) or pd.isna(lon):
            continue
        popup_text = (
            f"<div style='font-size: 1rem;'>"
            f"<b>Date:</b> {row.get('acq_date', '?')}<br>"
            f"<b>Time:</b> {row.get('acq_time', '?')}<br>"
            f"<b>Confidence:</b> {row.get('confidence', '?')}"
            f"<b><br>Latitude:</b> {lat}"
            f"<b><br>Longitude:</b> {lon}"
            f"</div>"
        )
        folium.CircleMarker(
            location=[lat, lon],
            radius=3,
            color="red",
            fill=True,
            fill_color="orange",
            fill_opacity=1.5,
            popup=popup_text
        ).add_to(m)
    m.fit_bounds(df[["latitude", "longitude"]].values.tolist())

    m.save(output_file)
    print(f"[INFO] Map saved as {output_file}")
