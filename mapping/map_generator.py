import folium
import pandas as pd

def generate_map(df, output_file="wildfires_map.html"):
    """
    Generate an interactive global wildfire map (no infinite world wrap).
    """
    if df.empty:
        print("[WARN] No wildfire data available to map.")
        return

    # 🌍 Center on the world with wrapping disabled
    m = folium.Map(
    location=[0, 0],
    zoom_start=2,
    worldCopyJump=False,       # disables infinite wrap-around
    no_wrap=True               # ensures only one world copy
)

    for _, row in df.iterrows():
        lat, lon = row.get("latitude"), row.get("longitude")
        if pd.isna(lat) or pd.isna(lon):
            continue

        popup_text = (
            f"<b>Date:</b> {row.get('acq_date', '?')}<br>"
            f"<b>Time:</b> {row.get('acq_time', '?')}<br>"
            f"<b>Confidence:</b> {row.get('confidence', '?')}<br>"
            f"<b>Brightness:</b> {row.get('brightness', '?')}"
        )

        folium.CircleMarker(
            location=[lat, lon],
            radius=4,
            color="red",
            fill=True,
            fill_color="orange",
            fill_opacity=0.7,
            popup=popup_text
        ).add_to(m)
    # Fit map to bounds of all fire points
    m.fit_bounds(df[["latitude", "longitude"]].values.tolist())

    m.save(output_file)
    print(f"[INFO] Map saved as {output_file}")
