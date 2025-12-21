import requests, json, os

TG_TOKEN = os.environ.get("TG_TOKEN", "8260211449:AAGtYQ5roe6Heu40hYnh_WSaiL0RndD3f-c")
CHAT_ID = "-1003604954550"
CARGO_RATE = 450

# Китайские товары (база)
CHINA = [
    {"name": "Power Bank 30000mAh", "price_cny": 85, "weight": 0.4},
    {"name": "Power Bank 20000mAh", "price_cny": 55, "weight": 0.3},
    {"name": "TWS Earbuds ANC", "price_cny": 45, "weight": 0.1},
    {"name": "USB Hub 7in1", "price_cny": 35, "weight": 0.15},
]

def landed_cost(item):
    return item["price_cny"] * 13 + item["weight"] * CARGO_RATE

def search_wb(query, limit=5):
    r = requests.get(f"https://search.wb.ru/exactmatch/ru/common/v4/search?query={query}&limit={limit}", timeout=15)
    return r.json().get("data", {}).get("products", [])

def send_tg(text):
    requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"})

def main():
    opps = []

    for item in CHINA:
        landed = landed_cost(item)
        prods = search_wb(item["name"].split()[0] + " " + item["name"].split()[1])

        for p in prods[:3]:
            price_ru = p.get("salePriceU", 0) / 100
            if price_ru > landed:
                margin = (price_ru - landed) / price_ru * 100
                profit = price_ru - landed
                if margin > 25:
                    opps.append(f"*{item['name']}*\nWB: {price_ru:.0f}₽ | CN: {landed:.0f}₽\nМаржа: {margin:.0f}% | Профит: {profit:.0f}₽")

    if opps:
        msg = "🚀 *CARGO SWARM*\n\n" + "\n\n".join(opps[:5])
        send_tg(msg)
        print("Sent", len(opps), "opportunities")
    else:
        print("No opportunities found")

if __name__ == "__main__":
    main()
