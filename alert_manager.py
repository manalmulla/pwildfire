import os
import json
import pandas as pd
import firebase_admin
from firebase_admin import credentials, messaging

# -----------------------------
# 🔥 Firebase Initialization
# -----------------------------
FIREBASE_KEY_PATH = os.path.join(
    os.path.dirname(__file__),
    "wildfire-alert-d7468-firebase-adminsdk-fbsvc-1ee196f02c.json"
)

if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_KEY_PATH)
    firebase_admin.initialize_app(cred)
    print("[INFO] Firebase initialized for web push notifications.")


# -----------------------------
# 🔔 Send Push Notification
# -----------------------------
def send_push_notification(message):
    """
    Sends a web push notification to all subscribed users (from tokens.json)
    """
    try:
        with open("tokens.json", "r") as f:
            tokens = json.load(f)
    except FileNotFoundError:
        print("[WARN] tokens.json not found — no subscribers yet.")
        return
    except json.JSONDecodeError:
        print("[ERROR] tokens.json is invalid — please check formatting.")
        return

    if not tokens:
        print("[INFO] No subscribed users to alert yet.")
        return

    notification = messaging.MulticastMessage(
        notification=messaging.Notification(
            title="🔥 Wildfire Alert",
            body=message
        ),
        tokens=tokens
    )

    response = messaging.send_multicast(notification)
    print(f"[PUSH SENT] {response.success_count} users notified, {response.failure_count} failed.")


# -----------------------------
# 🚨 Detect New Wildfires
# -----------------------------
_last_alerts = set()

def check_new_alerts(df):
    """
    Detects new wildfire events (based on lat/lon/date) and sends alerts.
    """
    global _last_alerts

    if df.empty:
        print("[INFO] No wildfire data to check for alerts.")
        return

    # Create a set of unique identifiers for new data
    current_alerts = {
        f"{row['latitude']}-{row['longitude']}-{row['acq_date']}"
        for _, row in df.iterrows()
        if not pd.isna(row.get("latitude")) and not pd.isna(row.get("longitude"))
    }

    # Find new wildfire hotspots
    new_alerts = current_alerts - _last_alerts

    if not new_alerts:
        print("[INFO] No new wildfire alerts detected.")
        return

    _last_alerts = current_alerts  # Update record
    print(f"[ALERT] {len(new_alerts)} new wildfire hotspots detected!")

    # Send a push notification to subscribers
    alert_message = f"{len(new_alerts)} new wildfire hotspots detected. Check dashboard for details."
    send_push_notification(alert_message)
