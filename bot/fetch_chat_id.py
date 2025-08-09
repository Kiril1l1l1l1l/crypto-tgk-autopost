import os
import requests

BOT_TOKEN = os.environ["BOT_TOKEN"]
TG_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

r = requests.get(f"{TG_API}/getUpdates")
r.raise_for_status()
updates = r.json()["result"]
for u in updates:
    ch = (u.get("channel_post") or u.get("edited_channel_post") or {}).get("chat")
    if ch:
        print("CHAT_ID:", ch["id"])
