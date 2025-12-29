import requests
import time
import random

TG = "8260211449:AAGtYQ5roe6Heu40hYnh_WSaiL0RndD3f-c"
CHAT = "-1003604954550"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36",
    "Accept": "*/*",
    "Origin": "https://www.wildberries.ru",
    "Referer": "https://www.wildberries.ru/"
}

ITEMS = [
    ("powerbank 30000", 85, 0.4),
    ("powerbank 20000", 55, 0.3),
    ("tws наушники", 45, 0.1),
]

def search(q):
    url = f"https://search.wb.ru/exactmatch/ru/common/v5/search?appType=1&curr=rub&dest=-1257786&query={q}&resultset=catalog&sort=popular&spp=30"
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code == 429:
            return "429"
        return r.json().get("data", {}).get("products", [])
    except Exception as e:
        return str(e)

def main():
    out = []
    for name, cny, kg in ITEMS:
        landed = cny * 13.5 + kg * 450
        time.sleep(random.uniform(2, 4))
        res = search(name)

        if res == "429":
            out.append(f"{name}: 429 BANNED")
        elif isinstance(res, str):
            out.append(f"{name}: ERROR {res}")
        else:
            out.append(f"{name}: {len(res)} шт, landed={landed:.0f}р")
            for p in res[:2]:
                price = p.get("salePriceU", 0) / 100
                if price > 0:
                    margin = (price - landed) / price * 100
                    out.append(f"  └ {price:.0f}р, маржа {margin:.0f}%")

    msg = "🔍 SCOUT v2:\n" + "\n".join(out)
    requests.post(f"https://api.telegram.org/bot{TG}/sendMessage", json={"chat_id": CHAT, "text": msg})
    print(msg)

if __name__ == "__main__":
    main()
