import folium

def generate_map(df, output_file="wildfires_map.html"):
    """
    Generate an interactive wildfire map using folium.
    """
    if df.empty:
        print("[WARN] No wildfire data available to map.")
        return

    lat_col, lon_col = "latitude", "longitude"
    center = [df[lat_col].mean(), df[lon_col].mean()]
    m = folium.Map(location=center, zoom_start=5)

    for _, row in df.iterrows():
        popup_text = (
            f"<b>Date:</b> {row.get('acq_date', '?')}<br>"
            f"<b>Time:</b> {row.get('acq_time', '?')}<br>"
            f"<b>Confidence:</b> {row.get('confidence', '?')}<br>"
            f"<b>Brightness:</b> {row.get('brightness', '?')}"
        )
        folium.CircleMarker(
            location=[row[lat_col], row[lon_col]],
            radius=4,
            color="red",
            fill=True,
            fill_color="orange",
            popup=popup_text
        ).add_to(m)

    m.save(output_file)
    print(f"[INFO] Map saved as {output_file}")
