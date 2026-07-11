import os
import time
import requests

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
    "japan historics"
]

seen = set()


def notify(message):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={
            "chat_id": CHAT_ID,
            "text": message
        }
    )


while True:
    try:
        response = requests.post(
            URL,
            headers=HEADERS,
            json={},
            timeout=10
        )

        data = response.json()

        snippets = data.get("response", {}).get("snippets", [])

        for item in snippets:
            item_text = str(item).lower()

            if not any(keyword in item_text for keyword in PREMIUM_KEYWORDS):
                continue

            title = "Unknown Premium"
            inventory = 0

            try:
                title = item["tracking"]["widget_meta"]["widget_title"]
            except:
                pass

            try:
                inventory = item["tracking"]["impression_map"]["inventory"]
            except:
                pass

            if inventory and title not in seen:
                notify(
                    f"🚨 HOT WHEELS PREMIUM ALERT 🚨\n\n"
                    f"{title}\n"
                    f"Inventory: {inventory}\n\n"
                    f"Open Blinkit now."
                )

                seen.add(title)

        time.sleep(15)

    except Exception as e:
        print(e)
        time.sleep(30)
