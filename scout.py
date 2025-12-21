import requests

TG_TOKEN = "8260211449:AAGtYQ5roe6Heu40hYnh_WSaiL0RndD3f-c"
CHAT_ID = "-1003604954550"
CARGO_RATE = 450

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
    "Accept-Language": "ru-RU,ru;q=0.9"
}

CHINA = [
    {"name": "Power Bank 30000", "price_cny": 85, "weight": 0.4},
    {"name": "Power Bank 20000", "price_cny": 55, "weight": 0.3},
    {"name": "TWS наушники", "price_cny": 45, "weight": 0.1},
    {"name": "USB Hub", "price_cny": 35, "weight": 0.15},
]

def search_wb(query):
    try:
        r = requests.get(
            f"https://search.wb.ru/exactmatch/ru/common/v4/search?query={query}&resultset=catalog&limit=10",
            headers=HEADERS, timeout=30
        )
        return r.json().get("data", {}).get("products", [])
    except Exception as e:
        print(f"WB error for {query}: {e}")
        return []

def send_tg(text):
    r = requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"})
    print(f"TG response: {r.status_code}")

def main():
    opps = []

    for item in CHINA:
        landed = item["price_cny"] * 13 + item["weight"] * CARGO_RATE
        prods = search_wb(item["name"])
        print(f"{item['name']}: {len(prods)} products")

        for p in prods[:5]:
            price = p.get("salePriceU", 0) / 100
            if price > landed:
                margin = (price - landed) / price * 100
                if margin > 25:
                    opps.append({
                        "name": p.get("name", "")[:50],
                        "price": price,
                        "landed": landed,
                        "margin": margin,
                        "profit": price - landed
                    })

    if opps:
        opps.sort(key=lambda x: x["margin"], reverse=True)
        lines = [f"*{o['name']}*\nWB: {o['price']:.0f}₽ → {o['margin']:.0f}% ({o['profit']:.0f}₽)" for o in opps[:5]]
        send_tg("🚀 *CARGO SCOUT*\n\n" + "\n\n".join(lines))
    else:
        send_tg("🔍 CARGO: поиск завершён, маржинальных нет")

if __name__ == "__main__":
    main()
