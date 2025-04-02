import requests
import time
import datetime
from discord_webhook import DiscordWebhook
from Config import PRODUCT_URL, webhook_url, users

# Check every hour
CHECK_INTERVAL = 3600

def check_stock():
    try:
        #Send request and get product data
        response = requests.get(PRODUCT_URL)
        response.raise_for_status()
        product_data = response.json()

        #Webhook settings
        allowed_mentions = {
            "parse": ["everyone"],
            "users": [users]
        }

        variants = product_data.get("variants", [])
        for variant in variants:
            title = variant.get("title", "Unknown Variant")
            available = variant.get("available", False)
            if available:
                message = f"[{datetime.datetime.now()}] {title}: {'In Stock ✅'}"
                id = variant.get("id")
                discord_message = f"[{datetime.datetime.now()}] {title}: {f'In Stock ✅ [[ATC](https://cp-e.com/cart/add?id={id})]'}"
                webhook = DiscordWebhook(url=webhook_url, content=discord_message)
            else:
                message = f"[{datetime.datetime.now()}] {title}: {'Out of Stock ❌'}"
                webhook = DiscordWebhook(url=webhook_url, content=message)

            webhook.execute()
            print(message)

        # Notify if any variant is in stock
        if any(v["available"] for v in variants):
            message = f"🚨 One or more variants are IN STOCK! <@{users}>"
            webhook = DiscordWebhook(url=webhook_url, content=message, allowed_mentions=allowed_mentions)
            response = webhook.execute()

            print(message)

    except Exception as e:
        print(f"Error checking stock: {e}")

if __name__ == "__main__":
    while True:
        check_stock()
        time.sleep(CHECK_INTERVAL)