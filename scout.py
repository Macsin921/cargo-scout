import requests

TG_TOKEN = "8260211449:AAGtYQ5roe6Heu40hYnh_WSaiL0RndD3f-c"
CHAT_ID = "-1003604954550"
CARGO_RATE = 450

HEADERS = {"User-Agent": "Mozilla/5.0", "Accept-Language": "ru"}

CHINA = [
    {"name": "powerbank 30000", "price_cny": 85, "weight": 0.4},
    {"name": "powerbank 20000", "price_cny": 55, "weight": 0.3},
    {"name": "tws наушники", "price_cny": 45, "weight": 0.1},
]

def search_wb(query):
    try:
        r = requests.get(
            f"https://search.wb.ru/exactmatch/ru/common/v4/search?query={query}&resultset=catalog&limit=5",
            headers=HEADERS, timeout=30
        )
        data = r.json()
        prods = data.get("data", {}).get("products", [])
        return prods
    except Exception as e:
        return []

def send_tg(text):
    requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": text})

def main():
    debug = []
    opps = []

    for item in CHINA:
        landed = item["price_cny"] * 13 + item["weight"] * CARGO_RATE
        prods = search_wb(item["name"])
        debug.append(f"{item['name']}: {len(prods)} шт, landed={landed:.0f}р")

        for p in prods[:3]:
            price = p.get("salePriceU", 0) / 100
            name = p.get("name", "?")[:40]

            if price > 0:
                margin = (price - landed) / price * 100
                profit = price - landed
                debug.append(f"  {name}: {price:.0f}р, margin={margin:.0f}%")

                if margin > 25 and profit > 200:
                    opps.append(f"{name}: {price:.0f}р, маржа {margin:.0f}%, профит {profit:.0f}р")

    msg = "🔍 DEBUG:\n" + "\n".join(debug[:15])
    if opps:
        msg += "\n\n🚀 OPPORTUNITIES:\n" + "\n".join(opps[:5])

    send_tg(msg)
    print(msg)

if __name__ == "__main__":
    main()
