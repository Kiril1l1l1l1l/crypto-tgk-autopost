import os
import requests
from datetime import datetime, timezone
from dateutil import tz

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
POST_TYPE = os.environ.get("POST_TYPE", "morning")

TG_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

def tg_send_message(text):
    r = requests.post(f"{TG_API}/sendMessage",
                      json={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"})
    r.raise_for_status()

def gecko_prices(ids=("bitcoin","ethereum"), vs="usd"):
    ids_str = ",".join(ids)
    url = "https://api.coingecko.com/api/v3/simple/price"
    r = requests.get(url, params={"ids": ids_str, "vs_currencies": vs, "include_24hr_change": "true"})
    r.raise_for_status()
    return r.json()

def fmt_pct(x):
    sign = "▲" if x >= 0 else "▼"
    return f"{sign}{abs(x):.2f}%"

def now_local():
    tz_msk = tz.gettz("Europe/Moscow")
    return datetime.now(timezone.utc).astimezone(tz_msk)

def build_post():
    now = now_local().strftime("%d.%m.%Y %H:%M")
    prices = gecko_prices()
    btc = prices["bitcoin"]
    eth = prices["ethereum"]
    if POST_TYPE == "morning":
        return f"🌅 Утренний обзор\nBTC: ${btc['usd']} ({fmt_pct(btc['usd_24h_change'])})\nETH: ${eth['usd']} ({fmt_pct(eth['usd_24h_change'])})\n🕒 {now}"
    elif POST_TYPE == "midday":
        return f"🏙 Дневной апдейт\nBTC {fmt_pct(btc['usd_24h_change'])}, ETH {fmt_pct(eth['usd_24h_change'])}\n🕒 {now}"
    else:
        return f"🌙 Вечерний итог\nBTC: ${btc['usd']} ({fmt_pct(btc['usd_24h_change'])}), ETH: ${eth['usd']} ({fmt_pct(eth['usd_24h_change'])})\n🕒 {now}"

def main():
    tg_send_message(build_post())

if __name__ == "__main__":
    main()
