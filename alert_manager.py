import json
import firebase_admin
from firebase_admin import credentials, messaging
import os

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("wildfire-alert-d7468-firebase-adminsdk-fbsvc-1ee196f02c.json")
    firebase_admin.initialize_app(cred)
    print("[INFO] Firebase initialized for web push notifications.")

TOKENS_FILE = "tokens.json"
SENT_ALERTS_FILE = "sent_alerts.json"

def load_tokens():
    if os.path.exists(TOKENS_FILE):
        with open(TOKENS_FILE, "r") as f:
            return json.load(f)
    return []

def load_sent_alerts():
    if os.path.exists(SENT_ALERTS_FILE):
        with open(SENT_ALERTS_FILE, "r") as f:
            return json.load(f)
    return []

def save_sent_alerts(alert_ids):
    with open(SENT_ALERTS_FILE, "w") as f:
        json.dump(alert_ids, f, indent=2)

def send_push_notification(message):
    tokens = load_tokens()
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

def check_new_alerts(df):
    if df.empty:
        print("[INFO] No wildfire data to check.")
        return

    sent_alerts = load_sent_alerts()
    new_alerts = []

    for _, row in df.iterrows():
        alert_id = f"{row.get('latitude')}_{row.get('longitude')}_{row.get('acq_date')}_{row.get('acq_time')}"
        if alert_id not in sent_alerts:
            confidence = row.get('confidence')
            if isinstance(confidence, (int, float)) and confidence >= 30:
                msg = f"🔥 Wildfire detected!\nDate: {row.get('acq_date')} Time: {row.get('acq_time')}\nLat: {row.get('latitude')}, Lon: {row.get('longitude')}\nConfidence: {confidence}"
                send_push_notification(msg)
                new_alerts.append(alert_id)

    if new_alerts:
        sent_alerts.extend(new_alerts)
        save_sent_alerts(sent_alerts)
        print(f"[INFO] {len(new_alerts)} new alerts sent.")
    else:
        print("[INFO] No new alerts to send.")
