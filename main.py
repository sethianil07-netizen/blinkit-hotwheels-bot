import os
import time
import requests
import json

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://blinkit.com/v1/layout/search?q=hotwheels&search_type=type_to_search"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "auth_key": os.getenv("AUTH_KEY"),
    "app_client": "consumer_web",
    "device_id": os.getenv("DEVICE_ID"),
    "session_uuid": os.getenv("SESSION_UUID"),
    "lat": os.getenv("LAT"),
    "lon": os.getenv("LON"),
    "Content-Type": "application/json",
    "Origin": "https://blinkit.com",
    "Referer": "https://blinkit.com/s/?q=hotwheels"
}

PREMIUM_KEYWORDS = [
    "premium",
    "boulevard",
    "car culture",
    "team transport",
    "fast & furious",
    "pop culture",
    "race day",
    "modern classics",
    "japan historics",
    "speed machines",
    "ronin run",
    "slide street",
    "canyon warriors"
]

seen = set()


def send_telegram(message):
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={
                "chat_id": CHAT_ID,
                "text": message
            },
            timeout=10
        )
    except Exception as e:
        print("Telegram error:", e)


while True:
    try:
        print("Checking Blinkit...")

        response = requests.post(
            URL,
            headers=HEADERS,
            json={},
            timeout=20
        )

        print("Status Code:", response.status_code)

        if response.status_code != 200:
            print("Response:")
            print(response.text[:1000])
            time.sleep(60)
            continue

        try:
            data = response.json()
        except Exception:
            print("Failed to parse JSON")
            print(response.text[:1000])
            time.sleep(60)
            continue

        snippets = data.get("response", {}).get("snippets", [])

        print(f"Found {len(snippets)} snippets")

        for item in snippets:
            text_blob = json.dumps(item).lower()

            if not any(keyword in text_blob for keyword in PREMIUM_KEYWORDS):
                continue

            title = None
            inventory = 0

            try:
                title = item["tracking"]["widget_meta"]["widget_title"]
            except:
                pass

            try:
                inventory = item["tracking"]["impression_map"]["inventory"]
            except:
                pass

            if not title:
                continue

            print(f"Premium found: {title} | Inventory: {inventory}")

            if inventory and title not in seen:
                send_telegram(
                    f"🚨 HOT WHEELS PREMIUM ALERT 🚨\n\n"
                    f"{title}\n"
                    f"Inventory: {inventory}\n\n"
                    f"Open Blinkit NOW!"
                )

                seen.add(title)

        time.sleep(15)

    except Exception as e:
        print("Runtime error:", e)
        time.sleep(30)
