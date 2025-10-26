from flask import Flask, render_template, send_from_directory, jsonify, request
import os, json, webbrowser, threading, time
from alert_manager import send_push_notification, check_new_alerts
from api.wildfire_api import fetch_wildfires

app = Flask(__name__)

# ---------------------
# Flask routes
# ---------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/map")
def serve_map():
    return send_from_directory(".", "wildfires_map.html")

@app.route("/firebase-messaging-sw.js")
def service_worker():
    return send_from_directory("static", "firebase-messaging-sw.js")

@app.route("/latest_alerts")
def latest_alerts():
    if os.path.exists("latest_alerts.json"):
        with open("latest_alerts.json", "r") as f:
            alerts = json.load(f)
    else:
        alerts = []
    return {"alerts": alerts}


@app.route("/register_token", methods=["POST"])
def register_token():
    data = request.get_json()
    token = data.get("token")
    if not token:
        return jsonify({"error": "No token provided"}), 400

    # Save token
    tokens = []
    if os.path.exists("tokens.json"):
        with open("tokens.json", "r") as f:
            tokens = json.load(f)

    if token not in tokens:
        tokens.append(token)
        with open("tokens.json", "w") as f:
            json.dump(tokens, f, indent=2)

    return jsonify({"status": "success", "token_saved": token})

# ---------------------
# Background alert thread
# ---------------------
def background_alert_checker():
    MAP_KEY = "53b0fcf7bea04cca38d1e3b5f03359d8"
    DATASET = "VIIRS_NOAA20_NRT"
    DAYS = 1
    BBOX = None
    INTERVAL_MINUTES = 1

    print("[INFO] Starting background wildfire alert checker...")
    while True:
        print("[INFO] Fetching latest wildfire data...")
        df = fetch_wildfires(MAP_KEY, DATASET, BBOX, DAYS)
        check_new_alerts(df)
        print(f"[INFO] Sleeping for {INTERVAL_MINUTES} minutes...\n")
        time.sleep(INTERVAL_MINUTES * 60)

# ---------------------
# Run Flask + background thread
# ---------------------
if __name__ == "__main__":
    import threading
import webbrowser

    # Start background thread
t = threading.Thread(target=background_alert_checker, daemon=True)
t.start()

    # Open browser **only once**
webbrowser.open(f"http://127.0.0.1:5000")

    # Run Flask with debug=True but **disable reloader**
app.run(debug=True, use_reloader=False, port=5000)