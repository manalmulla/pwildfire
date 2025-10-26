import time
from alert_manager import send_push_notification

INTERVAL_MINUTES = 1  # send test alert every 1 minute

def main_loop():
    print("[INFO] Starting test alert loop...")
    counter = 1
    while True:
        message = f"🚨 Test wildfire alert #{counter}!"
        print(f"[INFO] Sending: {message}")
        send_push_notification(message)
        counter += 1
        time.sleep(INTERVAL_MINUTES * 60)

if __name__ == "__main__":
    main_loop()
